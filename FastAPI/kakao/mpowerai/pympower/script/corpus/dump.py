import os
import sys
import argparse
from tqdm import tqdm
from typing import Iterable
from pympower.classes.mbase import *
from pympower.classes.mcrypt import *
from pympower.classes.mdataset import *
from pympower.classes.mcorpus import *
from pympower.classes.mpreprocessing import *

class MCorpusNodeUtil(MBase):
    def __init__(self, powerdb_con:MpowerDB2):
        super().__init__(powerdb_con)

    def close(self):
        pass

    def getNodeIdByName(self, parentId:str, nodeName:str) -> list[str]:
        stmt = self.powerdb_con.createStatement()
        query = (
            'SELECT NODE_ID'
            ' FROM SHARE_NODE_INFO'
            ' WHERE NODE_NAME=%(NODE_NAME)s'
            ' AND PARENT_ID=%(PARENT_ID)s'
            ' AND STATUS=%(STATUS_1)s'
        )
        self.powerdb_con.execute(stmt, query, {
            'NODE_NAME': nodeName,
            'PARENT_ID': parentId,
            'STATUS_1': '1',
        })
        return [rs['NODE_ID'] for rs in self.powerdb_con.fetchAll(stmt)]

    def getNodeIdBySplittedRelPath(self, parentId:str, splittedRelPath:list[str]) -> list[str]:
        nodeIds = []
        for nodeId in self.getNodeIdByName(parentId, splittedRelPath[0]):
            if len(splittedRelPath) >= 2:
                splittedRelPath = splittedRelPath[1:]
                nodeIds.extend(self.getNodeIdBySplittedRelPath(nodeId, splittedRelPath))
            else:
                nodeIds.append(nodeId)
        return nodeIds

    def getNodeIdBySplittedPath(self, splittedPath:list[str]) -> list[str]:
        return self.getNodeIdBySplittedRelPath('0', splittedPath)

class MergeableUnitDumperApp(MBase):
    def __init__(self,
        powerdb_con:MpowerDB2,
        logger:MLogger,
        appId:str,
        dumpDir:str,
        eachFileFormat:MDatasetEachFileFormat,
        paths:list[str]
    ):
        self.powerdb_con = powerdb_con
        self.logger = logger
        self.appId = appId
        self.dumpDir = dumpDir
        self.eachFileFormat = eachFileFormat
        self.paths = paths

        self.nodeUtil = MCorpusNodeUtil(self.powerdb_con)
        self.totalCount = 0
        self.successCount = 0
        self.errorCount = 0
        self.notSupportedCount = 0

        self.paragraphSplitter = MParagraphSplitter()
        self.preprocessor = MCompositePreprocessor([
            MLanguageFilter(['en', 'ko']),
        ])

    def close(self):
        pass

    def run(self):
        with MFileLocker(os.path.join(global_val.MPOWER_TEMP_DIR, self.appId)):
            self.logger.logging(MLogger.LOG_INFO, 'dump corpus')
            self.logger.logging(MLogger.LOG_INFO, f"dumpDir: {self.dumpDir}")

            cFileIds = []
            for path in self.paths:
                nodeIds = self.nodeUtil.getNodeIdBySplittedPath(path.split('/'))
                for nodeId in nodeIds:
                    cFileIds.extend(self._getCFileIdsRec(nodeId))

            cFileIds = set(cFileIds)
            dataset = MDataset(self.dumpDir)
            if dataset.exists():
                dataset.remove()
            dataset.create(['CFILE_ID', 'CHUNK_NUMBER', 'SNF_FORMAT_CODE', 'SNF_FORMAT_NAME', 'TEXT'], self.eachFileFormat)
            with dataset.getWriter() as writer:
                for cFileId in tqdm(cFileIds, ncols=120, ascii=True):
                    self._dumpCFile(writer, cFileId)

            self.logger.logging(MLogger.LOG_INFO, f'totalCount : {len(cFileIds)}')
            self.logger.logging(MLogger.LOG_INFO, f'successCount: {self.successCount}')
            self.logger.logging(MLogger.LOG_INFO, f'errorCount: {self.errorCount}')
            self.logger.logging(MLogger.LOG_INFO, f'notSupportedCount: {self.notSupportedCount}')

    def _getCFileIdsRec(self, nodeId:str):
        cFileIds = []
        stmt = self.powerdb_con.createStatement()
        query = (
            'SELECT CFILE_ID'
            ' FROM SHARE_FILE_INFO F,'
            ' CORPUS_FILE_INFO C'
            ' WHERE F.RFILE_NAME=C.RFILE_NAME'
            ' AND F.NODE_ID=%(NODE_ID)s'
            ' AND F.STATUS=%(STATUS_1)s'
            ' AND C.STATUS=%(STATUS_1)s'
        )
        self.powerdb_con.execute(stmt, query, {
            'NODE_ID': nodeId,
            'STATUS_1': '1',
        })
        for rs in self.powerdb_con.fetchAll(stmt):
            cFileIds.append(rs['CFILE_ID'])

        # 자식 노드 CFILE_ID 조회
        query = (
            'SELECT NODE_ID'
            ' FROM SHARE_NODE_INFO'
            ' WHERE PARENT_ID=%(PARENT_ID)s'
            ' AND STATUS=%(STATUS_1)s'
        )
        self.powerdb_con.execute(stmt, query, {
            'PARENT_ID': nodeId,
            'STATUS_1': '1',
        })
        for rs in self.powerdb_con.fetchAll(stmt):
            cFileIds.extend(self._getCFileIdsRec(rs['NODE_ID']))

        return cFileIds

    def _dumpCFile(self, writer:MDatasetWriter, cFileId:str):
        stmt = self.powerdb_con.createStatement()
        query = (
            'SELECT CFILE_ID, VOL_PATH, SNF_FORMAT_CODE, SNF_FORMAT_NAME, CFILE_PATH, CFILE_NAME, C.ENC_MODE, C.ZIP_MODE, C.MRK'
            ' FROM CORPUS_FILE_INFO C,'
            ' STORAGE_INFO S'
            ' WHERE S.VOL_ID=C.VOL_ID'
            ' AND CFILE_ID=%(CFILE_ID)s'
        )
        self.powerdb_con.execute(stmt, query, {
            'CFILE_ID': cFileId,
        })
        for rs in self.powerdb_con.fetchAll(stmt):
            decryptor = MDecryptor(rs['ENC_MODE'], rs['ZIP_MODE'], rs['MRK'])
            cFilePath = os.path.join(rs['VOL_PATH'], rs['CFILE_PATH'], rs['CFILE_NAME'])
            with open(cFilePath, 'rb') as reader:
                paragraphs = reader.read()
            paragraphs = str(decryptor.update(paragraphs) + decryptor.final(), encoding='utf-8')
            if self.paragraphSplitter.isSupportedType(rs['SNF_FORMAT_CODE']):
                try:
                    paragraphs = self.paragraphSplitter.split(rs['SNF_FORMAT_CODE'], [paragraphs])
                    paragraphs = self.preprocessor.preprocess(paragraphs)
                    for paragraphIndex, mergeableUnit in enumerate(paragraphs, start=1):
                        writer.write(
                            rs['CFILE_ID'],
                            paragraphIndex,
                            rs['SNF_FORMAT_CODE'],
                            rs['SNF_FORMAT_NAME'],
                            mergeableUnit,
                        )
                    self.successCount += 1
                except:
                    self.errorCount += 1
                    raise
            else:
                self.notSupportedCount += 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app-id', dest='appId', required=True, type=str, help='appId')
    parser.add_argument('--dump-dir', dest='dumpDir', required=True, type=str, help='path to dump directory')
    parser.add_argument(
        '--each-file-format',
        dest='eachFileFormat',
        type=MDatasetEachFileFormat,
        default=MDatasetEachFileFormat.BULK_JSON,
        help='dataset each file format'
    )
    parser.add_argument('paths', metavar='path', type=str, nargs='+', help='node or file paths of secure file server to build corpus')

    class _Args:
        appId:str
        dumpDir:str
        eachFileFormat:MDatasetEachFileFormat
        paths:list[str]
    args:_Args = parser.parse_args()

    powerdb_con = MpowerDB2()
    powerdb_con.connectWithIndex()

    mainModuleFilePath = Path(sys.modules[__name__].__file__)
    logger = MLogger(
        mainModuleFilePath.stem,
        args.appId,
        os.path.join(global_val.MPOWER_LOG_PATH, mainModuleFilePath.parent.parent.name, mainModuleFilePath.parent.name),
        MLogger.LOG_DAILY,
    )

    app = MergeableUnitDumperApp(powerdb_con, logger, args.appId, args.dumpDir, args.eachFileFormat, args.paths)
    app.run()

if __name__ == '__main__':
    try:
        main()
    except MpowerException as e:
        print(e.message, file=sys.stderr)
