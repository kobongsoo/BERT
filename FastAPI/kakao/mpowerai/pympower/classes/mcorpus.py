import pympower.classes.snf as snf
import io
from pympower.classes.mbase import MpowerException
from pympower.common.statuscode import StatusCode
from pympower.classes.mbase import *
from pympower.classes.mcrypt import *
global_val = global_val.load_global_val()

##############################################################################
# 텍스트 추출
##############################################################################

class _SNFTextFileBuilder:
    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def write(self, text:str):
        pass

    @abstractmethod
    def setFormat(self, formatCode:int):
        pass

    @abstractmethod
    def getFormat(self) -> int:
        pass

    @abstractmethod
    def setUnzipped(self):
        pass

    @abstractmethod
    def setAttachment(self):
        pass

class _SNFTextExtractingContext:
    @abstractmethod
    def pushInit(self, filename:str):
        pass

    @abstractmethod
    def popCommit(self):
        pass

    @abstractmethod
    def popError(self, errorCode:int, message:str, nativeErrorCode:int):
        pass

    @abstractmethod
    def peekFileBuilder(self) -> _SNFTextFileBuilder:
        pass

class _SNFTextExtractor:
    def _userFunc(self, buf:snf.SN3BUF, context:_SNFTextExtractingContext):
        text = buf.get_text()
        # clear 메소드를 호출하지 않으면 메모리가 무한정 늘어나는 문제가 있다.
        buf.clear()
        writer = context.peekFileBuilder()
        writer.write(text)

    def _markerFunc(self, buf:snf.SN3BUF, context:_SNFTextExtractingContext, marker:snf.SN3MARKER):
        if snf.SN3BUF_STATE_TYPE.FILE_START_STATE == marker.state:
            # 각 파일은 개별 텍스트 파일로 저장하기 때문에 파일 마커는 추출하지 않는다.
            buf.set_skip_command(snf.SN3BUF_SKIP_TYPE.MARKER_SKIP)
            context.pushInit(marker.marker)
        elif snf.SN3BUF_STATE_TYPE.FILE_END_STATE == marker.state:
            buf.set_skip_command(snf.SN3BUF_SKIP_TYPE.NO_SKIP)
            context.popCommit()
        elif snf.SN3BUF_STATE_TYPE.OLE_START_STATE == marker.state:
            # OLE는 marker.unzipMFI를 전달하지 않아 파일 유형(format)을 알 수 없기 때문에
            # OLE 텍스트는 추출하지 않는다.
            buf.set_skip_command(snf.SN3BUF_SKIP_TYPE.ALL_SKIP)
        elif snf.SN3BUF_STATE_TYPE.OLE_END_STATE == marker.state:
            buf.set_skip_command(snf.SN3BUF_SKIP_TYPE.NO_SKIP)
        elif snf.SN3BUF_STATE_TYPE.PAGE_START_STATE == marker.state:
            # 페이지별 추출을 지원하는 파일은, PDF, PPTX, XLSX이다.
            # 페이지는 개별 파일이 아닌 하나의 파일로 텍스트를 추출한다.
            # PDF는 페이지별 구분이 필요 없고, XLSX는 셀별 구분을 사용할 경우 페이지별 구분이 필요치 않다.
            # 반면에 PPTX는 페이지별 구분을 사용하는 것이 유리하기 때문에 페이지 마커는 추출한다.
            # 텍스트 전처리에서 ..PAGE:xxxx를 처리해야한다.
            buf.set_skip_command(snf.SN3BUF_SKIP_TYPE.NO_SKIP)
        elif snf.SN3BUF_STATE_TYPE.PAGE_END_STATE == marker.state:
            buf.set_skip_command(snf.SN3BUF_SKIP_TYPE.NO_SKIP)
        elif snf.SN3BUF_STATE_TYPE.UNZIP_FILE_STATE == marker.state:
            fileBuilder = context.peekFileBuilder()
            if marker.unzipMFI:
                formatCode = marker.unzipMFI.fmt_detect()
                fileBuilder.setFormat(formatCode)
            fileBuilder.setUnzipped()
        elif snf.SN3BUF_STATE_TYPE.ATTACHMENT_FILE_STATE == marker.state:
            fileBuilder = context.peekFileBuilder()
            if marker.unzipMFI:
                formatCode = marker.unzipMFI.fmt_detect()
                fileBuilder.setFormat(formatCode)
            fileBuilder.setAttachment()
        return snf.SN3USER_FUNC.CONTINUE

    @staticmethod
    def isExtractable(path:str) -> bool:
        return snf.snf_fmt_isFilterFormat(path)

    def extractText(self, context:_SNFTextExtractingContext, lFileName:str, path:str) -> None:
        context.pushInit(lFileName)

        fileBuilder = context.peekFileBuilder()

        try:
            formatCode = snf.snf_fmt_detect(path)
            fileBuilder.setFormat(formatCode)
            buf = snf.SN3BUF(callback_chunk_size=8192)
            buf.set_user_func(self._userFunc)
            buf.set_user_data(context)
            buf.set_marker_func(self._markerFunc)
            buf.set_marker_data(context)
            #buf.set_unknownfile_func(self._unknownfileFunc)
            buf.filter(path)
        except snf.SNFError as e:
            snfErrorFunc, snfErrorCode = e.args
            statusCode = StatusCode(snf.snf_error_code_to_status_code(snfErrorCode))
            message = f'snf function fail. {snfErrorFunc}({snfErrorCode})'
            context.popError(statusCode.value, message, snfErrorCode)
            raise MpowerException(message, statusCode.value, -1, statusCode.name, snfErrorCode)
        except MpowerException as e:
            context.popError(e.code, e.message, e.native if isinstance(e.native, int) else None)
            raise
        except Exception as e:
            context.popError(StatusCode.ERR_PI_EXTRACT_FATAL.value, str(e), None)
            raise
        else:
            context.popCommit()

##############################################################################
# 코퍼스 텍스트 추출
##############################################################################

_MAX_ERROR_LENGTH = 200

class _MCorpusFileBuilder(MBase, _SNFTextFileBuilder):
    def __init__(
        self,
        powerdb_con:MpowerDB2,
        rFileName:str,
        parentId:int,
        marker:str,
        status:int,
        volId:str,
        volPath:str,
        cFilePath:str,
        cFileName:str,
        encMode:int,
        zipMode:int,
        MRK:str
    ):
        MBase.__init__(self, powerdb_con)
        self.cFileId = None
        self.rFileName = rFileName
        self.parentId = parentId
        self.marker = marker
        self.status = status
        self.errorCode = None
        self.errorMessage = None
        self.nativeErrorCode = None

        self.charSize = None
        self.bytesSize = None

        self.formatCode = None
        self.formatName = None
        self.unzipped = False
        self.attachment = False

        self.volId = volId
        self.volPath = volPath
        self.cFilePath = cFilePath
        self.cFileName = cFileName
        self.cFileCDate = None

        self.encMode = encMode
        self.zipMode = zipMode
        self.MRK = MRK

        self.fileCreated = False
        self.file:io.BytesIO = None
        self.encryptor = MEncryptor(encMode, zipMode, MRK)

        self.utilClass = MClassFactory.getUtility()

    def _open(self):
        self.charSize = 0
        self.bytesSize = 0
        cFileFullPath = os.path.join(self.volPath, self.cFilePath, self.cFileName)
        self.file = open(cFileFullPath, 'wb')
        self.fileCreated = True
        self.cFileCDate = self.utilClass.getCurrentTime()

    def close(self):
        if None != self.file:
            self.file.close()
            self.file = None

    def write(self, text:str):
        if None == self.file:
            self._open()

        self.charSize += len(text)

        data = bytes(text, 'utf-8')
        self.bytesSize += len(data)

        data = self.encryptor.update(data)
        if data:
            self.file.write(data)

    def setFormat(self, formatCode:int):
        self.formatCode = formatCode
        self.formatName = snf.snf_fmt_format_name(formatCode)

    def getFormat(self) -> int:
        return self.formatCode

    def setUnzipped(self):
        self.unzipped = True

    def setAttachment(self):
        self.attachment = True

    def setSuccess(self):
        self.status = 1

    def setError(self, errorCode:int, message:str, nativeErrorCode:int):
        self.status = 0
        self.errorCode = errorCode
        self.errorMessage = message
        self.nativeErrorCode = nativeErrorCode

    def insertToDB(self):
        if None != self.cFileId:
            raise MpowerException(
                f'TODO error message',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )

        stmt = self.powerdb_con.createStatement()
        self.cFileId = self.utilClass.makeUniqueID('CF_', '')
        query = (
            'INSERT INTO CORPUS_FILE_INFO(CFILE_ID, RFILE_NAME, PARENT_ID, STATUS,'
            ' EXTRACTION_START_TIME, MARKER)'
            ' VALUES(%(CFILE_ID)s, %(RFILE_NAME)s, %(PARENT_ID)s, %(STATUS)s,'
            ' %(EXTRACTION_START_TIME)s, %(MARKER)s)'
        )
        self.powerdb_con.execute(stmt, query, {
            'CFILE_ID': self.cFileId,
            'RFILE_NAME': self.rFileName,
            'PARENT_ID': self.parentId,
            'STATUS': 2,
            'EXTRACTION_START_TIME': self.utilClass.getCurrentTime(),
            'MARKER': self.marker,
        })
        self.powerdb_con.commit()

    def updateToDB(self):
        stmt = self.powerdb_con.createStatement()
        if self.file:
            data = self.encryptor.final()
            if data:
                self.file.write(data)
            self.file.flush()
        query = (
            'UPDATE CORPUS_FILE_INFO'
            ' SET STATUS=%(STATUS)s,'
            ' EXTRACTION_END_TIME=%(EXTRACTION_END_TIME)s,'
            ' ERROR_CODE=%(ERROR_CODE)s,'
            ' ERROR_MESSAGE=%(ERROR_MESSAGE)s,'
            ' NATIVE_ERROR_CODE=%(NATIVE_ERROR_CODE)s,'
            ' SNF_FORMAT_CODE=%(SNF_FORMAT_CODE)s,'
            ' SNF_FORMAT_NAME=%(SNF_FORMAT_NAME)s,'
            ' UNZIPPED=%(UNZIPPED)s,'
            ' ATTACHMENT=%(ATTACHMENT)s,'
            ' CHAR_SIZE=%(CHAR_SIZE)s,'
            ' BYTE_SIZE=%(BYTE_SIZE)s,'
            ' VOL_ID=%(VOL_ID)s,'
            ' CFILE_PATH=%(CFILE_PATH)s,'
            ' CFILE_NAME=%(CFILE_NAME)s,'
            ' CFILE_CDATE=%(CFILE_CDATE)s,'
            ' CFILE_SIZE=%(CFILE_SIZE)s,'
            ' ENC_MODE=%(ENC_MODE)s,'
            ' ZIP_MODE=%(ZIP_MODE)s,'
            ' MRK=%(MRK)s'
            ' WHERE CFILE_ID=%(CFILE_ID)s'
            ' AND STATUS=%(STATUS_RUNNING)s'
        )
        stmt.execute(query, {
            'STATUS': self.status,
            'EXTRACTION_END_TIME': self.utilClass.getCurrentTime(),
            'ERROR_CODE': self.errorCode,
            'ERROR_MESSAGE': self.errorMessage[:_MAX_ERROR_LENGTH] if isinstance(self.errorMessage, str) else None,
            'NATIVE_ERROR_CODE': self.nativeErrorCode,
            'SNF_FORMAT_CODE': self.formatCode,
            'SNF_FORMAT_NAME': self.formatName,
            'UNZIPPED': 1 if self.unzipped else 0,
            'ATTACHMENT': 1 if self.attachment else 0,
            'CHAR_SIZE': self.charSize,
            'BYTE_SIZE': self.bytesSize,
            'VOL_ID': self.volId if self.fileCreated else None,
            'CFILE_PATH': self.cFilePath if self.fileCreated else None,
            'CFILE_NAME': self.cFileName if self.fileCreated else None,
            'CFILE_CDATE': self.cFileCDate if self.file else None,
            'CFILE_SIZE': self.file.tell() if self.file else None,
            'ENC_MODE': self.encMode if self.file else None,
            'ZIP_MODE': self.zipMode if self.file else None,
            'MRK': self.MRK if self.file else None,
            'CFILE_ID': self.cFileId,
            'STATUS_RUNNING': 2,
        })
        if self.file and self.file.tell():
            query = (
                'UPDATE STORAGE_INFO'
                ' SET USED_SPACE=USED_SPACE+%(CFILE_SIZE)s'
                ' WHERE VOL_ID=%(VOL_ID)s'
            )
            stmt.execute(query, {
                'CFILE_SIZE': self.file.tell(),
                'VOL_ID': self.volId,
            })
        self.powerdb_con.commit()
        self.close()

class _MCorpusBuildContext(MBase):
    def __init__(self, powerdb_con:MpowerDB2, rFileName:str, volId:str, volPath:str, encMode:int, zipMode:int):
        super().__init__(powerdb_con)
        self.powerdb_con = powerdb_con
        self.rFileName = rFileName
        self.volId = volId
        self.volPath = volPath
        self.encMode = encMode
        self.zipMode = zipMode

        self.utilClass = MClassFactory.getUtility()
        self.builderStack:list[_MCorpusFileBuilder] = []

    def close(self):
        pass

    def pushInit(self, marker:str):
        fileBuilder = _MCorpusFileBuilder(
            powerdb_con=self.powerdb_con,
            rFileName=self.rFileName,
            parentId=self.builderStack[-1].cFileId if len(self.builderStack) else None,
            marker=marker,
            status=2,
            volId=self.volId,
            volPath=self.volPath,
            cFilePath=self.utilClass.getRFilePath(),
            cFileName=self.utilClass.makeUniqueID('CF_', '.SMF'),
            encMode=self.encMode,
            zipMode=self.zipMode,
            MRK=self.utilClass.makeMRKUniqueID(),
        )
        fileBuilder.insertToDB()
        self.builderStack.append(fileBuilder)

    def popCommit(self) -> None:
        fileBuilder = self.builderStack.pop()
        fileBuilder.setSuccess()
        fileBuilder.updateToDB()

    def popError(self, errorCode:int, message:str, nativeErrorCode:int):
        fileBuilder = self.builderStack.pop()
        fileBuilder.setError(errorCode, message, nativeErrorCode)
        fileBuilder.updateToDB()
        self.powerdb_con.commit()

    def peekFileBuilder(self) -> _MCorpusFileBuilder:
        return self.builderStack[-1]

class MCorpusBuilder(MBase):
    def __init__(self, powerdb_con:MpowerDB2):
        super().__init__(powerdb_con)

        self.utilClass = MClassFactory.getUtility()
        self.crypt = MCrypt(self.powerdb_con)

    def close(self):
        pass

    def exists(self, rFileName:str) -> bool:
        stmt = self.powerdb_con.createStatement()
        query = (
            'SELECT RFILE_NAME'
            ' FROM CORPUS_FILE_INFO'
            ' WHERE PARENT_ID IS NULL'
            ' AND RFILE_NAME=%(RFILE_NAME)s'
        )
        self.powerdb_con.execute(stmt, query, {
            'RFILE_NAME': rFileName,
        })
        rs = self.powerdb_con.fetchAll(stmt)
        if 0 == len(rs):
            return False
        else:
            return True

    def remove(self, rFileName:str) -> None:
        stmt = self.powerdb_con.createStatement()
        query = (
            'SELECT C.CFILE_ID, S.VOL_PATH, C.CFILE_PATH, C.CFILE_NAME'
            ' FROM CORPUS_FILE_INFO C'
            ' LEFT OUTER JOIN STORAGE_INFO S'
            ' ON C.VOL_ID=S.VOL_ID'
            ' WHERE C.PARENT_ID IS NOT NULL'
            ' AND C.RFILE_NAME=%(RFILE_NAME)s'
        )
        self.powerdb_con.execute(stmt, query, {
            'RFILE_NAME': rFileName
        })
        for rs in self.powerdb_con.fetchAll(stmt):
            if rs['VOL_PATH']:
                path = os.path.join(rs['VOL_PATH'], rs['CFILE_PATH'], rs['CFILE_NAME'])
                if os.path.exists(path):
                    os.remove(path)
            query = (
                'DELETE FROM CORPUS_FILE_INFO'
                ' WHERE CFILE_ID=%(CFILE_ID)s'
            )
            self.powerdb_con.execute(stmt, query, {
                'CFILE_ID': rs['CFILE_ID'],
            })
            self.powerdb_con.commit()

        query = (
            'DELETE FROM CORPUS_FILE_INFO'
            ' WHERE PARENT_ID IS NULL'
            ' AND RFILE_NAME=%(RFILE_NAME)s'
        )
        self.powerdb_con.execute(stmt, query, {
            'RFILE_NAME': rFileName,
        })
        self.powerdb_con.commit()

    def build(self, rFileName:str) -> None:
        stmt = self.powerdb_con.createStatement()
        # rFileName은 주키가 아니라 여러 ROW가 리턴될 수 있어 GROUP BY로 묶었다.
        query = (
            'SELECT VOL_PATH, RFILE_PATH, RFILE_NAME, ENC_MODE, ZIP_MODE, MRK, LFILE_NAME, LFILE_SIZE'
            ' FROM SHARE_FILE_INFO F,'
            ' STORAGE_INFO S'
            ' WHERE S.VOL_ID=F.VOL_ID'
            ' AND RFILE_NAME=%(RFILE_NAME)s'
            ' AND F.STATUS=%(STATUS)s'
            ' GROUP BY VOL_PATH, RFILE_PATH, RFILE_NAME, ENC_MODE, ZIP_MODE, MRK, LFILE_NAME, LFILE_SIZE'
        )
        self.powerdb_con.execute(stmt, query, {
            'RFILE_NAME': rFileName,
            'STATUS': '1',
        })
        rsShareFileInfo = self.powerdb_con.fetchAll(stmt)
        if 1 != len(rsShareFileInfo):
            raise MpowerException(
                f"source file not found. RFILE_NAME: {rFileName}",
                StatusCode.ERR_PI_EXTRACT_FATAL.value, -1, StatusCode.ERR_PI_EXTRACT_FATAL.name,
            )
        rsShareFileInfo = rsShareFileInfo[0]

        # 이미 추출한 텍스트가 존재하는 경우
        if self.exists(rsShareFileInfo['RFILE_NAME']):
            raise MpowerException(
                f"corpus file already exists. RFILE_NAME: {rsShareFileInfo['RFILE_NAME']}",
                StatusCode.ERR_PI_EXTRACT_FATAL.value, -1, StatusCode.ERR_PI_EXTRACT_FATAL.name,
            )

        rFilePath = os.path.join(rsShareFileInfo['VOL_PATH'], rsShareFileInfo['RFILE_PATH'], rsShareFileInfo['RFILE_NAME'])
        decPath = os.path.join(global_val.MPOWER_TEMP_DIR, self.utilClass.makeUniqueID('', ''))

        try:
            self.crypt.mpowerDecrypt(
                rFilePath,
                decPath,
                rsShareFileInfo['ENC_MODE'],
                rsShareFileInfo['ZIP_MODE'],
                rsShareFileInfo['MRK'],
                rsShareFileInfo['LFILE_SIZE']
                )

            if False == _SNFTextExtractor.isExtractable(decPath):
                raise MpowerException('text extraction not supported format')

            # 추출할 텍스트를 저장할 볼륨 조회
            query = (
                'SELECT VOL_ID, VOL_PATH, TOTAL_SPACE, USED_SPACE, SAFE_SPACE'
                ' FROM STORAGE_INFO'
                ' WHERE VOL_TYPE=%(VOL_TYPE)s'
            )
            self.powerdb_con.execute(stmt, query, {
                'VOL_TYPE': global_val.CORPUS_DISK
            })
            fileSize = os.path.getsize(decPath)
            rsStorageInfo = None
            for rs in self.powerdb_con.fetchAll(stmt):
                availableSize = rs['TOTAL_SPACE'] - rs['USED_SPACE'] - rs['SAFE_SPACE']
                # 실제로 텍스트를 추출한 결과 파일의 크기는 fileSize와 동일하지는 않다.
                # 원문에 이미지 등을 포함하고 있다면 더 작을수도 있고, 원문이 텍스트 위주라면 더 클 수도 있다.
                # 텍스트 추출한 파일 크기가 더 크더라도 TOTAL_SPACE를 넘지 않도록 하려면 SAFE_SPACE를 적절히 설정한다.
                if availableSize > fileSize:
                    rsStorageInfo = rs
                    break
            if None == rsStorageInfo:
                raise MpowerException(
                    f'corpus storage does not exist',
                    StatusCode.SC_OVER_DISK_SIZE.value, -1, StatusCode.SC_OVER_DISK_SIZE.name
                )

            context = _MCorpusBuildContext(
                powerdb_con=self.powerdb_con,
                rFileName=rsShareFileInfo['RFILE_NAME'],
                volId=rsStorageInfo['VOL_ID'],
                volPath=rsStorageInfo['VOL_PATH'],
                encMode=rsShareFileInfo['ENC_MODE'],
                zipMode=rsShareFileInfo['ZIP_MODE'],
            )

            extractor = _SNFTextExtractor()

            extractor.extractText(context, rsShareFileInfo['LFILE_NAME'], decPath)
        finally:
            if os.path.exists(decPath):
                os.remove(decPath)

    def getPaths(self, rFileName:str) -> list[str]:
        stmt = self.powerdb_con.createStatement()
        query = (
            'WITH RECURSIVE CTE_FILE_INFO AS ('
            'SELECT N.NODE_ID, PARENT_ID, CONCAT(NODE_NAME, %(PATH_SEP)s, LFILE_NAME) FILE_PATH'
            ' FROM SHARE_FILE_INFO F,'
            ' SHARE_NODE_INFO N'
            ' WHERE F.NODE_ID=N.NODE_ID'
            ' AND F.STATUS=%(STATUS_1)s'
            ' AND N.STATUS=%(STATUS_1)s'
            ' AND RFILE_NAME=%(RFILE_NAME)s'
            ' UNION ALL'
            ' SELECT P.NODE_ID, P.PARENT_ID, CONCAT(P.NODE_NAME, %(PATH_SEP)s, C.FILE_PATH)'
            ' FROM SHARE_NODE_INFO P,'
            ' CTE_FILE_INFO C'
            ' WHERE P.NODE_ID=C.PARENT_ID'
            ' AND P.STATUS=%(STATUS_1)s'
            ')'
            ' SELECT DISTINCT FILE_PATH'
            ' FROM CTE_FILE_INFO'
            ' WHERE PARENT_ID=%(ROOT_PARENT_ID)s'
        )
        self.powerdb_con.execute(stmt, query, {
            'STATUS_1': '1',
            'RFILE_NAME': rFileName,
            'PATH_SEP': '/',
            'ROOT_PARENT_ID': '0',
        })
        return [rs['FILE_PATH'] for rs in self.powerdb_con.fetchAll(stmt)]

##############################################################################
# 로컬 파일 텍스트 추출
##############################################################################

class MExtractedTextInfo(MToFromConfigClass):
    def __init__(
        self,
        filename:str,
        exists:bool,
        markerPath:list[str],
        marker:str,
        formatCode:int,
        formatName:str,
        unzipped:bool,
        attachment:bool,
    ):
        self.filename = filename
        self.exists = exists
        self.markerPath = markerPath
        self.marker = marker
        self.formatCode = formatCode
        self.formatName = formatName
        self.unzipped = unzipped
        self.attachment = attachment

    @staticmethod
    def createFromConfig(config:dict) -> 'MExtractedTextInfo':
        return MExtractedTextInfo(
            filename=config['filename'],
            exists=config['exists'],
            markerPath=config['markerPath'],
            marker=config['marker'],
            formatCode=config['formatCode'],
            formatName=config['formatName'],
            unzipped=config['unzipped'],
            attachment=config['attachment'],
        )

    def exportToConfig(self) -> dict:
        return {
            'filename': self.filename,
            'exists': self.exists,
            'markerPath': self.markerPath,
            'marker': self.marker,
            'formatCode': self.formatCode,
            'formatName': self.formatName,
            'unzipped': self.unzipped,
            'attachment': self.attachment,
        }

class MExtractedTextIndex(MToFromConfigClass):
    def __init__(self, indexType:str, files:list[MExtractedTextInfo]):
        self.indexType = indexType
        self.files = files

        if _MExtractedTextDefinition.indexType != indexType:
            raise MpowerException(
                f'unrecognizable index file: expected: {_MExtractedTextDefinition.indexType}, given: {indexType}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )

    def createFromConfig(config:dict) -> 'MToFromConfigClass':
        return MExtractedTextIndex(
            indexType=config['indexType'],
            files=[MExtractedTextInfo.createFromConfig(fileInfo) for fileInfo in config['files']],
        )

    def exportToConfig(self) -> dict:
        return {
            'indexType': self.indexType,
            'files': [info.exportToConfig() for info in self.files]
        }

class _MExtractedTextDefinition:
    indexType = 'Extracted Text'
    indexFileName = 'index.json'

class MExtractedText:
    @staticmethod
    def loadIndex(dirPath:str) -> MExtractedTextIndex:
        indexPath = os.path.join(dirPath, _MExtractedTextDefinition.indexFileName)
        with open(indexPath, 'r', encoding='utf-8') as f:
            index = json.loads(f.read())
        return MExtractedTextIndex.createFromConfig(index)

class _MTextFileBuilder(_SNFTextFileBuilder):
    def __init__(self, markerPath:list[str], marker:str, dirPath:str, filename:str):
        self.info = MExtractedTextInfo(
            filename=filename,
            exists=False,
            markerPath=markerPath,
            marker=marker,
            formatCode=0,
            formatName='',
            unzipped=False,
            attachment=False,
        )
        self.dirPath = dirPath
        self.file = None

    def close(self):
        if None != self.file:
            self.file.close()

    def write(self, text:str):
        if None == self.file:
            self.file = open(os.path.join(self.dirPath, self.info.filename), 'w', encoding='utf-8')
            self.info.exists = True
        self.file.write(text)

    def setFormat(self, formatCode:int):
        self.info.formatCode = formatCode
        self.info.formatName = snf.snf_fmt_format_name(formatCode)

    def setUnzipped(self):
        self.info.unzipped = True

    def setAttachment(self):
        self.info.attachment = True

    def rollback(self):
        if self.file:
            self.file.close()
            os.remove(os.path.join(self.dirPath, self.info.filename))

class _MTextExtractingContext(_SNFTextExtractingContext):
    def __init__(self, dirPath:str):
        self.dirPath = dirPath

        self.textFileList:list[MExtractedTextInfo] = []
        self.builderStack:list[_MTextFileBuilder] = []

        self.utilClass = MClassFactory.getUtility()

    def pushInit(self, marker:str):
        markerPath = [builder.info.marker for builder in self.builderStack]
        fileBuilder = _MTextFileBuilder(
            markerPath,
            marker,
            self.dirPath,
            self.utilClass.makeUniqueID('', '.txt'),
        )
        self.builderStack.append(fileBuilder)

    def popCommit(self) -> None:
        fileBuilder = self.builderStack.pop()
        fileBuilder.close()
        self.textFileList.append(fileBuilder.info)

    def peekFileBuilder(self) -> _SNFTextFileBuilder:
        return self.builderStack[-1]

    def writeIndex(self):
        index = MExtractedTextIndex(_MExtractedTextDefinition.indexType, self.textFileList)
        with open(os.path.join(self.dirPath, _MExtractedTextDefinition.indexFileName), 'w', encoding='utf-8') as f:
            f.write(json.dumps(index.exportToConfig(), ensure_ascii=False, indent=4))

    def rollback(self):
        for textFile in self.textFileList:
            if textFile.exists:
                os.remove(os.path.join(self.dirPath, textFile.filename))

        for builder in self.builderStack:
            builder.rollback()

class MTextExtractor:
    def __init__(self, outputDir:str, keepFilesEvenFail:bool = False):
        self.outputDir = outputDir
        self.keepFilesEvenFail = keepFilesEvenFail

    def extractText(self, lFileName:str, path:str):
        try:
            # 이미 있는 경우 덮어 쓰기 불가
            # 삭제 후 다시 만들어야 함
            os.mkdir(self.outputDir)
        except:
            raise MpowerException(
                f'Failed to create output directory. outputDir: {self.outputDir}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )

        try:
            extractor = _SNFTextExtractor()
            context = _MTextExtractingContext(self.outputDir)
            extractor.extractText(context, lFileName, path)
            context.writeIndex()
        except:
            if False == self.keepFilesEvenFail:
                context.rollback()
                os.rmdir(self.outputDir)
            raise

##############################################################################
# __all__ 구성
##############################################################################

__all__ = [
    MCorpusBuilder.__name__,
    MExtractedText.__name__,
    MTextExtractor.__name__,
]
