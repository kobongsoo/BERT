from io import TextIOBase
import os
import json
from datetime import datetime
from dateutil import tz
from random import Random
from enum import IntEnum, Enum
from typing import Generator, Any, Optional, Union
from pympower.classes.mbase import *
from pympower.common.statuscode import StatusCode
from pympower.common.global_val import global_val
global_val = global_val.load_global_val()

##############################################################################
# MDataset
##############################################################################

class _MDatasetDefinition:
    lockFilePostfix = '.lock'
    metaFileName = 'dataset.json'
    eachFileLimitCount = 100_000

class _MDatasetFileInfo(MToFromConfigClass):
    def __init__(self, count:int, filename:str):
        self.count = count
        self.filename = filename

    @staticmethod
    def createFromConfig(config:dict) -> 'MToFromConfigClass':
        return _MDatasetFileInfo(
            count=config['count'],
            filename=config['filename'],
        )

    def exportToConfig(self) -> dict:
        return {
            'count': self.count,
            'filename': self.filename,
        }

class MDatasetEachFileFormat(Enum):
    JSON_ENCODED_TSV = '.tsv'
    BULK_JSON = '.bulkjson'

class MEachFileLimitType(Enum):
    LIMIT_BY_SIZE = 'size'
    LIMIT_BY_COUNT = 'count'

class _MEachFileWritingLimit:
    def __init__(self, type:MEachFileLimitType, limit:int):
        self.type = type
        self.limit = limit

    @staticmethod
    def createFromConfig(config:dict) -> '_MEachFileWritingLimit':
        return _MEachFileWritingLimit(
            type=MEachFileLimitType(config['type']),
            limit=config['limit'],
        )

    def exportToConfig(self) -> dict:
        return {
            'type': self.type.value,
            'limit': self.limit,
        }

class _MDatasetFileWritingStatus(IntEnum):
    SUCCESS = 1
    WRITING = 2

class _MDatasetWritingContext(MToFromConfigClass):
    def __init__(self, fileIndex:int, status:_MDatasetFileWritingStatus):
        self.fileIndex = fileIndex
        self.status = status

    @staticmethod
    def createFromConfig(config: dict) -> '_MDatasetWritingContext':
        return _MDatasetWritingContext(
            fileIndex=config['fileIndex'],
            status=_MDatasetFileWritingStatus(config['status']),
        )

    def exportToConfig(self) -> dict:
        return {
            'fileIndex': self.fileIndex,
            'status': self.status.value,
        }

class _MDatasetInfo(MToFromConfigClass):
    def __init__(self,
        # id:Optional[str],
        cdate:Optional[datetime],
        # udate:Optional[datetime],
        extraInfo:Optional[dict[str, Any]],
        subDatasets:Optional[dict[str, str]],
        eachFileFormat:MDatasetEachFileFormat,
        eachFileLimit:Optional[_MEachFileWritingLimit],
        writingContext:Optional[_MDatasetWritingContext],
        columns:Optional[list[str]],
        files:Optional[list[_MDatasetFileInfo]],
    ):
        # self.id = id
        self.cdate = cdate
        # self.udate = udate
        self.extraInfo = extraInfo
        self.subDatasets = subDatasets
        self.eachFileFormat = eachFileFormat
        self.eachFileLimit = eachFileLimit
        self.writingContext = writingContext
        self.columns = columns
        self.files = files

        self.utilClass = MClassFactory.getUtility()

    @staticmethod
    def createEmpty(
        columns:list[str],
        eachFileFormat:MDatasetEachFileFormat,
        eachFileLimitType:MEachFileLimitType,
        eachFileLimitValue:int,
        ) ->  '_MDatasetInfo':
        return _MDatasetInfo(
            # id=str(uuid.uuid4()),
            cdate=datetime.now(tz=tz.tzlocal()),
            # udate=datetime.now(tz=tz.tzlocal()),
            extraInfo=None,
            subDatasets=None,
            eachFileFormat=eachFileFormat,
            eachFileLimit=_MEachFileWritingLimit(eachFileLimitType, eachFileLimitValue),
            writingContext=None,
            columns=columns,
            files=None,
        )

    @staticmethod
    def createFromConfig(config:dict) -> '_MDatasetInfo':
        return _MDatasetInfo(
            # id=config['id'] if config['id'] else None,
            cdate=datetime.fromisoformat(config['cdate']) if 'cdate' in config else None,
            # udate=datetime.fromisoformat(config['udate']) if 'udate' in config else None,
            extraInfo=config['extraInfo'] if 'extraInfo' in config else None,
            subDatasets=config['subDatasets'] if 'subDatasets' in config else None,
            eachFileFormat=MDatasetEachFileFormat(config['eachFileFormat']),
            eachFileLimit=_MEachFileWritingLimit.createFromConfig(config['eachFileLimit']) if 'eachFileLimit' in config else None,
            writingContext=_MDatasetWritingContext.createFromConfig(config['writingContext']) if 'writingContext' in config else None,
            columns=config['columns'] if 'columns' in config else None,
            files=[_MDatasetFileInfo.createFromConfig(fileInfo) for fileInfo in config['files']] if 'files' in config else None,
        )

    def exportToConfig(self) -> dict:
        config = {}

        # if None != self.id:
        #     config['id'] = self.id

        if None != self.cdate:
            config['cdate'] = self.cdate.isoformat()

        # if None != self.udate:
        #     config['udate']= self.udate.isoformat()

        if None != self.extraInfo:
            config['extraInfo'] = self.extraInfo

        if None != self.subDatasets:
            config['subDatasets'] = self.subDatasets

        config['eachFileFormat'] = self.eachFileFormat.value

        if None != self.eachFileLimit:
            config['eachFileLimit'] = self.eachFileLimit.exportToConfig()

        if None != self.writingContext:
            config['writingContext'] = self.writingContext.exportToConfig()

        if None != self.columns:
            config['columns'] = self.columns

        if None != self.files:
            config['files'] = [fileInfo.exportToConfig() for fileInfo in self.files]

        return config

    def hasSubDataset(self, subDatasetName:str) -> bool:
        return subDatasetName in self.subDatasets if None != self.subDatasets else False

    def setSubDataset(self, subDatasetName:str):
        if self.hasSubDataset(subDatasetName):
            raise MpowerException(
                f'SubDataset already exists. subDatasetName:{subDatasetName}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )
        if None == self.subDatasets:
            self.subDatasets = []
        self.subDatasets.append(subDatasetName)

    def removeSubDatast(self, subDatasetName:str):
        try:
            delIndex = self.subDatasets.index(subDatasetName)
        except:
            raise MpowerException(
                f'SubDataset does not exists. subDatasetName:{subDatasetName}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )
        del(self.subDatasets[delIndex])
        if 0 == len(self.subDatasets):
            self.subDatasets = None

    def getFirstWritingFileInfo(self) -> _MDatasetFileInfo:
        if None == self.writingContext:
            self.writingContext = _MDatasetWritingContext(None, _MDatasetFileWritingStatus.SUCCESS)
        if None == self.writingContext.fileIndex:
            return self.getNextWritingFileInfo()
        else:
            return self.files[self.writingContext.fileIndex]

    def getNextWritingFileInfo(self) -> _MDatasetFileInfo:
        if MDatasetEachFileFormat.JSON_ENCODED_TSV == self.eachFileFormat:
            prefix = ''
            postfix = '.tsv'
        elif MDatasetEachFileFormat.BULK_JSON == self.eachFileFormat:
            prefix = ''
            postfix = '.bulkjson'
        else:
            raise MpowerException(
                f'Unknown each file format. eachFileFormat:{self.eachFileFormat.value}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )
        filename = self.utilClass.makeUniqueID(
            prefix,
            postfix,
        )
        fileInfo = _MDatasetFileInfo(0, filename)
        if None == self.files:
            self.files = []
        self.files.append(fileInfo)
        self.writingContext.fileIndex = len(self.files) - 1
        return fileInfo

    def setWritingFileInfo(self, fileInfo:_MDatasetFileInfo) -> None:
        self.files[self.writingContext.fileIndex] = fileInfo

    def setWritingStatus(self, status:_MDatasetFileWritingStatus) -> None:
        self.writingContext.status = status

    def getWritingStatus(self) -> _MDatasetFileWritingStatus:
        return self.writingContext.status

    def getColumnNameList(self) -> Union[list[str], None]:
        return self.columns

    def getCount(self) -> int:
        return sum([fileInfo.count for fileInfo in self.files])

    def hasExtraInfo(self, name:str) -> bool:
        return name in self.extraInfo

    def getExtraInfo(self, name:str) -> dict:
        return self.extraInfo[name]

    def setExtraInfo(self, name:str, data:dict) -> None:
        self.extraInfo[name] = data

    def removeExtraInfo(self, name:str) -> None:
        self.extraInfo.pop(name, None)

class _MDatasetAccessHandler:
    def __init__(self, datasetDir:str):
        self.datasetDir = datasetDir
        self.locker = MFileLocker(os.path.abspath(self.datasetDir) + '.lock', useLockCount=True)

    def getDatasetInfoFilePath(self) -> str:
        return os.path.join(self.datasetDir, _MDatasetDefinition.metaFileName)

    def loadDatasetInfo(self) -> _MDatasetInfo:
        if False == self.locker.hasLockOwnership():
            raise MpowerException(
                f'dataset has not been locked. datasetDir:{self.datasetDir}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )

        with open(self.getDatasetInfoFilePath(), 'r', encoding='utf-8') as f:
            data = f.read()
        data = json.loads(data)
        return _MDatasetInfo.createFromConfig(data)

    def saveDatasetInfo(self, datasetInfo:_MDatasetInfo) -> None:
        if False == self.locker.hasLockOwnership():
            raise MpowerException(
                f'dataset has not been locked. datasetDir:{self.datasetDir}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )

        # datasetInfo.udate = datetime.now(tz=tz.tzlocal())
        metaData = datasetInfo.exportToConfig()
        metaData = json.dumps(metaData, ensure_ascii=False, indent=4)
        with open(self.getDatasetInfoFilePath(), 'w', encoding='utf-8') as f:
            f.write(metaData)

    def datasetInfoExists(self):
        if False == self.locker.hasLockOwnership():
            raise MpowerException(
                f'dataset has not been locked. datasetDir:{self.datasetDir}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )

        metaDataPath = self.getDatasetInfoFilePath()
        return os.path.exists(metaDataPath)

    def removeDatasetInfo(self):
        if False == self.locker.hasLockOwnership():
            raise MpowerException(
                f'dataset has not been locked. datasetDir:{self.datasetDir}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )

        metaDataPath = self.getDatasetInfoFilePath()
        if os.path.exists(metaDataPath):
            os.remove(metaDataPath)

class MDataset:
    def __init__(self, datasetDir:str):
        self.datasetDir = datasetDir
        self.access = _MDatasetAccessHandler(self.datasetDir)

    def exists(self) -> bool:
        with self.access.locker:
            return os.path.isdir(self.datasetDir)

    def remove(self) -> None:
        with self.access.locker:
            if self.access.datasetInfoExists():
                datasetInfo = self.access.loadDatasetInfo()
                if None != datasetInfo.subDatasets:
                    for subDatasetName in datasetInfo.subDatasets:
                        subDataset = self.getSubDataset(subDatasetName)
                        subDataset.remove()
                if None != datasetInfo.files:
                    for fileInfo in datasetInfo.files:
                        filePath = os.path.join(self.datasetDir, fileInfo.filename)
                        if os.path.exists(filePath):
                            os.remove(filePath)
                self.access.removeDatasetInfo()
            os.rmdir(self.datasetDir)

    def create(self, columns:list[str] = None, eachFileFormat:MDatasetEachFileFormat = MDatasetEachFileFormat.BULK_JSON):
        with self.access.locker:
            if os.path.exists(self.datasetDir):
                raise MpowerException(
                    f'dataset already exists. path: {self.datasetDir}',
                    StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
                )
            os.mkdir(self.datasetDir)
            datasetInfo = _MDatasetInfo.createEmpty(
                columns=columns,
                eachFileFormat=eachFileFormat,
                eachFileLimitType=MEachFileLimitType.LIMIT_BY_COUNT,
                eachFileLimitValue=_MDatasetDefinition.eachFileLimitCount,
            )
            self.access.saveDatasetInfo(datasetInfo)

    def shuffle(self, seed = None) -> None:
        with self.access.locker:
            datasetInfo = self.access.loadDatasetInfo()
            rng = Random(seed)
            rng.shuffle(datasetInfo.files)
            self.access.saveDatasetInfo(datasetInfo)
            for fileInfo in datasetInfo.files:
                path = os.path.join(self.datasetDir, fileInfo.filename)
                with open(path, 'r', encoding='utf-8') as f:
                    data = f.read()
                data = data.splitlines(keepends=True)
                rng.shuffle(data)
                data = ''.join(data)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(data)

    def getReader(self) -> 'MDatasetReader':
        return MDatasetReader(self.access)

    def getWriter(self) -> 'MDatasetWriter':
        return MDatasetWriter(self.access)

    def getSubDataset(self, subDatasetName:str) -> 'MDataset':
        return _MSubDataset(self, subDatasetName)

class _MSubDataset(MDataset):
    def __init__(self, parentDataset:MDataset, subDatasetName:str):
        super().__init__(os.path.join(parentDataset.datasetDir, subDatasetName))

        self.parentDataset = parentDataset
        self.subDatasetName = subDatasetName

    def exists(self) -> bool:
        with self.parentDataset.access.locker:
            datasetInfo = self.parentDataset.access.loadDatasetInfo()
            return datasetInfo.hasSubDataset(self.subDatasetName)

    def remove(self) -> None:
        with self.parentDataset.access.locker:
            datasetInfo = self.parentDataset.access.loadDatasetInfo()
            if False == datasetInfo.hasSubDataset(self.subDatasetName):
                raise MpowerException(
                    f'SubDataset does not exists. datasetDir:{self.parentDataset.datasetDir}, subDatasetName:{self.subDatasetName}',
                    StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
                )
            if os.path.exists(self.datasetDir):
                super().remove()
            datasetInfo.removeSubDatast(self.subDatasetName)
            self.parentDataset.access.saveDatasetInfo(datasetInfo)

    def create(self, columns:Optional[list[str]] = None):
        with self.parentDataset.access.locker:
            if super().exists():
                raise MpowerException(
                    f'SubDataset directory already exists. datasetDir:{self.parentDataset.datasetDir}, subDatasetName:{self.subDatasetName}',
                    StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
                )
            datasetInfo = self.parentDataset.access.loadDatasetInfo()
            datasetInfo.setSubDataset(self.subDatasetName)
            self.parentDataset.access.saveDatasetInfo(datasetInfo)
            super().create(columns)

class MDatasetReader:
    def __init__(self, access:_MDatasetAccessHandler):
        self.access = access

        self.datasetInfo:_MDatasetInfo = None

    def __enter__(self) -> 'MDatasetReader':
        self.lock()
        return self

    def __exit__(self, type, value, traceback):
        self.unlock()

    def hasLockOwnership(self):
        return self.access.locker.hasLockOwnership()

    def lock(self) -> int:
        if 1 == self.access.locker.lock():
            self.datasetInfo = self.access.loadDatasetInfo()
        return self.access.locker.lockCount

    def unlock(self) -> int:
        if 1 == self.access.locker.lockCount:
            self.datasetInfo = None
            self.access.locker.unlock()
        return self.access.locker.lockCount

    def getColumnNameList(self) -> list[str]:
        if False == self.hasLockOwnership():
            raise MpowerException(
                f'dataset has not locked. datasetDir:{self.access.datasetDir}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )
        return self.datasetInfo.getColumnNameList()

    def getCount(self) -> int:
        if False == self.hasLockOwnership():
            raise MpowerException(
                f'dataset has not locked. datasetDir:{self.access.datasetDir}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )
        return self.datasetInfo.getCount()

    def getData(self, columns:Optional[list[str]] = None) -> Generator[tuple, None, None]:
        if False == self.hasLockOwnership():
            raise MpowerException(
                f'dataset has not locked. datasetDir:{self.access.datasetDir}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )
        if None != columns:
            if None == self.datasetInfo.columns:
                raise MpowerException(
                    f'dataset does not have column informations. dataset:{self.access.datasetDir}',
                    StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
                )
            columnIndexes:list[int] = []
            for columnName in columns:
                try:
                    columnIndex = self.datasetInfo.columns.index(columnName)
                except:
                    raise MpowerException(
                        f'column name not exists in dataset. columnName:{columnName}, dataset:{self.access.datasetDir}',
                        StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
                    )
                columnIndexes.append(columnIndex)
            #columnIndexes = [self.datasetInfo.columns.index(columnName) for columnName in columns]
        else:
            columnIndexes:list[int] = None
        for fileInfo in self.datasetInfo.files:
            path = os.path.join(self.access.datasetDir, fileInfo.filename)
            with open(path, 'r', encoding='utf-8') as f:
                for _ in range(fileInfo.count):
                    line = f.readline()
                    if MDatasetEachFileFormat.JSON_ENCODED_TSV == self.datasetInfo.eachFileFormat:
                        columns = [json.loads(column) for column in line.split('\t')]
                    elif MDatasetEachFileFormat.BULK_JSON == self.datasetInfo.eachFileFormat:
                        columns = json.loads(line)
                    else:
                        raise MpowerException(
                            f'Unknown each file format. eachFileFormat:{self.datasetInfo.eachFileFormat.value}',
                            StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
                        )
                    if None == columnIndexes:
                        yield tuple(columns)
                    else:
                        yield tuple(columns[columnIndex] for columnIndex in columnIndexes)

    def extraInfoExists(self, name:str) -> bool:
        if False == self.hasLockOwnership():
            raise MpowerException(
                f'dataset has not locked. datasetDir:{self.access.datasetDir}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )
        return name in self.datasetInfo.hasExtraInfo(name)

    def getExtraInfo(self, name:str) -> dict:
        if False == self.hasLockOwnership():
            raise MpowerException(
                f'dataset has not locked. datasetDir:{self.access.datasetDir}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )
        return self.datasetInfo.getExtraInfo(name)

class _MDatasetFileWriter:
    def __init__(self, datasetDir:str, fileInfo:_MDatasetFileInfo):
        self.datasetDir = datasetDir
        self.fileInfo = fileInfo

        self.file:TextIOBase = None

    def getSize(self) -> int:
        return self.file.tell()

    def getCount(self) -> int:
        return self.fileInfo.count

    @staticmethod
    def encodeTSVLine(values:tuple[Any]) -> bytes:
        line = '\t'.join(json.dumps(value, ensure_ascii=False) for value in values) + '\n'
        return line.encode('utf-8')

    @staticmethod
    def encodeBulkJsonLine(values:tuple[Any]) -> bytes:
        line = json.dumps(values, ensure_ascii=False) + '\n'
        return line.encode('utf-8')

    def writeLine(self, encodedLine:bytes) -> None:
        if None == self.file:
            self.file = open(os.path.join(self.datasetDir, self.fileInfo.filename), 'ab')
        self.file.write(encodedLine)
        self.fileInfo.count += 1

class MDatasetWriter:
    def __init__(self, access:_MDatasetAccessHandler):
        self.access = access

        self.datasetInfo:_MDatasetInfo = None
        self.fileWriter:_MDatasetFileWriter = None

        self.utilClass = MClassFactory.getUtility()

    def __del__(self):
        if self.hasLockOwnership():
            raise MpowerException(
                f'dataset __del__ has called without unlocked. datasetDir: {self.access.datasetDir}'
            )

    def __enter__(self) -> 'MDatasetWriter':
        self.lock()
        return self

    def __exit__(self, type, value, traceback):
        self.unlock()

    def hasLockOwnership(self) -> bool:
        return self.locked

    def lock(self) -> int:
        if 1 == self.access.locker.lock():
            self.locked = True
            try:
                self.datasetInfo = self.access.loadDatasetInfo()
                fileInfo = self.datasetInfo.getFirstWritingFileInfo()
                self.fileWriter = _MDatasetFileWriter(self.access.datasetDir, fileInfo)
                self.datasetInfo.setWritingStatus(_MDatasetFileWritingStatus.WRITING)
                self.access.saveDatasetInfo(self.datasetInfo)
                return self.access.locker.lockCount
            except:
                self.datasetInfo = None
                self.writingContext = None
                self.fileWriter = None
                self.access.locker.unlock()
                self.locked = False
                raise

    def unlock(self) -> int:
        if 1 == self.access.locker.lockCount:
            self.datasetInfo.setWritingFileInfo(self.fileWriter.fileInfo)
            self.datasetInfo.setWritingStatus(_MDatasetFileWritingStatus.SUCCESS)
            self.access.saveDatasetInfo(self.datasetInfo)
            self.fileWriter = None
            self.writingContext = None
            self.datasetInfo = None
            self.access.locker.unlock()
            self.locked = False
        return self.access.locker.lockCount

    def _openNextFile(self) -> None:
        self.datasetInfo.setWritingFileInfo(self.fileWriter.fileInfo)
        fileInfo = self.datasetInfo.getNextWritingFileInfo()
        self.fileWriter = _MDatasetFileWriter(self.access.datasetDir, fileInfo)
        self.access.saveDatasetInfo(self.datasetInfo)

    def write(self, *args) -> None:
        if False == self.hasLockOwnership():
            raise MpowerException(
                f'dataset has not locked. datasetDir:{self.access.datasetDir}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )

        columnNameList = self.datasetInfo.getColumnNameList()
        if None != columnNameList and len(columnNameList) != len(args):
            raise MpowerException(
                f'column count mismatch. datasetDir:{self.access.datasetDir}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )

        if MDatasetEachFileFormat.JSON_ENCODED_TSV == self.datasetInfo.eachFileFormat:
            line = _MDatasetFileWriter.encodeTSVLine(args)
        elif MDatasetEachFileFormat.BULK_JSON == self.datasetInfo.eachFileFormat:
            line = _MDatasetFileWriter.encodeBulkJsonLine(args)
        else:
            raise MpowerException(
                f'Unknown each file format. eachFileFormat:{self.datasetInfo.eachFileFormat.value}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )
        if MEachFileLimitType.LIMIT_BY_COUNT == self.datasetInfo.eachFileLimit.type:
            if self.fileWriter.getCount() >= self.datasetInfo.eachFileLimit.limit:
                self._openNextFile()
        elif MEachFileLimitType.LIMIT_BY_SIZE == self.datasetInfo.eachFileLimit.type:
            if (self.fileWriter.getSize() + len(line)) > self.datasetInfo.eachFileLimit.limit:
                self._openNextFile()
        else:
            raise MpowerException(
                f'Unknown file wriing limit type. type:{self.datasetInfo.eachFileLimit.type.value}'
            )

        self.fileWriter.writeLine(line)

    def hasExtraInfo(self, name:str) -> bool:
        if False == self.hasLockOwnership():
            raise MpowerException(
                f'dataset has not locked. datasetDir:{self.access.datasetDir}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )
        self.datasetInfo.hasExtraInfo(name)

    def getExtraInfo(self, name:str) -> dict:
        if False == self.hasLockOwnership():
            raise MpowerException(
                f'dataset has not locked. datasetDir:{self.access.datasetDir}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )
        self.datasetInfo.getExtraInfo(name)

    def setExtraInfo(self, name:str, data:dict) -> None:
        if False == self.hasLockOwnership():
            raise MpowerException(
                f'dataset has not locked. datasetDir:{self.access.datasetDir}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )
        self.datasetInfo.setExtraInfo(name, data)

    def removeExtraInfo(self, name:str) -> None:
        if False == self.hasLockOwnership():
            raise MpowerException(
                f'dataset has not locked. datasetDir:{self.access.datasetDir}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )
        self.datasetInfo.removeExtraInfo(name)

    def hasExtraInfoClass(self, klass:type[MToFromConfigClass]) -> MToFromConfigClass:
        return self.hasExtraInfo(klass.__name__)

    def getExtraInfoClass(self, klass:type[MToFromConfigClass]) -> MToFromConfigClass:
        return klass.createFromConfig(self.getExtraInfo(klass.__name__))

    def setExtraInfoClass(self, instance:MToFromConfigClass) -> None:
        self.setExtraInfo(type(instance).__name__, instance.exportToConfig())

    def removeExtraInfoClass(self, klass:type[MToFromConfigClass]) -> None:
        self.removeExtraInfo(klass.__name__)

##############################################################################
# __all__ 구성
##############################################################################

__all__ = [
    MDataset.__name__,
    MDatasetReader.__name__,
    MDatasetWriter.__name__,
    MDatasetEachFileFormat.__name__,
    MEachFileLimitType.__name__,
]
