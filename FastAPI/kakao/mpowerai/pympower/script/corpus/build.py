import sys
import argparse
from typing import Union, Generator
from pathlib import Path
from tqdm import tqdm
from pympower.classes.mbase import *
from pympower.classes.mcorpus import *
from pympower.classes.mscript import *
from pympower.common.global_val import *
global_val = global_val.load_global_val()

class CorpusBuilderApp(MBase):
    def __init__(self, powerdb_con:MpowerDB2, logger:MLogger, appId:str, paths:list[str]):
        super().__init__(powerdb_con)
        self.logger = logger
        self.appId = appId
        self.paths = paths

        self.loggingMessage = ''
        self.utilClass = MClassFactory.getUtility()
        self.builder = MCorpusBuilder(self.powerdb_con)

    def close(self):
        pass

    def run(self):
        with MFileLocker(os.path.join(global_val.MPOWER_TEMP_DIR, self.appId)):
            self.logger.logging(MLogger.LOG_INFO, 'extractig source paths')
            for path in self.paths:
                self.logger.logging(MLogger.LOG_INFO, f'- {path}')

            sys.stdout.flush()
            sFileIdList = self._getSFileIdList()
            self.logger.logging(MLogger.LOG_INFO, f'total: {len(sFileIdList)}')

            successCount = 0
            errorCount = 0
            skipCount = 0

            MStopEvent.setup()
            for sFileId in tqdm(sFileIdList, ncols=120, ascii=True):
                if MStopEvent.isSignaled():
                    self.logger.logging(MLogger.LOG_INFO, f'stop event has signaled')
                    print('stop event has signaled', file=sys.stderr)
                    break
                rFileName, status = self._getRFileNameAndCorpusStatus(sFileId)
                if (1 == status) or (0 == status):
                    skipCount += 1
                    continue
                elif None != status:
                    self.logger.logging(MLogger.LOG_INFO, f'{sFileId}: delete and retry', self.powerdb_con.dbidx)
                    self.builder.remove(rFileName)
                try:
                    self.builder.build(rFileName)
                except MpowerException as e:
                    errorCount += 1
                    self.logger.logging(MLogger.LOG_ERROR, f'{sFileId}: {e.message}', self.powerdb_con.dbidx)
                except Exception as e:
                    errorCount += 1
                    self.logger.logging(MLogger.LOG_ERROR, f'{sFileId}: {str(e)}', self.powerdb_con.dbidx)
                else:
                    successCount += 1
                    self.logger.logging(MLogger.LOG_INFO, f'{sFileId}: success')
            self.logger.logging(MLogger.LOG_INFO, 'complete')
            self.logger.logging(MLogger.LOG_INFO, f'success: {successCount}')
            self.logger.logging(MLogger.LOG_INFO, f'error: {errorCount}')
            self.logger.logging(MLogger.LOG_INFO, f'skip: {skipCount}')
            self.logger.logging(MLogger.LOG_INFO, 'source paths')

    def _getRFileNameAndCorpusStatus(self, sFileId):
        stmt = self.powerdb_con.createStatement()
        query = (
            'SELECT F.RFILE_NAME, C.STATUS'
            ' FROM SHARE_FILE_INFO F'
            ' LEFT OUTER JOIN CORPUS_FILE_INFO C'
            ' ON F.RFILE_NAME=C.RFILE_NAME'
            ' WHERE C.PARENT_ID IS NULL'
            ' AND F.SFILE_ID=%(SFILE_ID)s'
        )
        self.powerdb_con.execute(stmt, query, {
            'SFILE_ID': sFileId,
        })
        rs = self.powerdb_con.fetchAll(stmt)
        if 0 == len(rs):
            return None
        else:
            rs = rs[0]
            return rs['RFILE_NAME'], rs['STATUS']

    def _getSFileIdList(self) -> list[str]:
        sFileIdList = []
        for path in self.paths:
            for itemType, itemId in self._getItemTypeAndId(path):
                if global_val.ITEM_TYPE_NODE == itemType:
                    sFileIdList.extend(list(self._getSFileIdListInNodeRec(itemId)))
                else:
                    sFileIdList.append(itemId)
        return list(set(sFileIdList))

    def _getItemTypeAndId(self, path:str) -> list[tuple[str, str]]:
        return self._getItemTypeAndIdRec('0', path.split('/'), 0)

    def _getItemTypeAndIdRec(self, parentId:str, pathComponents:list[str], curPos:int) -> list[tuple[str, str]]:
        # 마지막 경로
        if len(pathComponents) == curPos + 1:
            nextPos, nodeIdList = self._getNodeId(parentId, pathComponents, curPos)
            if 0 == len(nodeIdList):
                sFileId = self._getSFileIdIfExists(parentId, pathComponents[curPos])
                if None == sFileId:
                    curPath = '/'.join(pathComponents)
                    raise MpowerException(f'경로를 찾을 수 없습니다. {curPath}')
                return [(global_val.ITEM_TYPE_FILE, sFileId)]
            else:
                return [(global_val.ITEM_TYPE_NODE, nodeId) for nodeId in nodeIdList]
        else:
            # 중간 경로
            nextPos, nodeIdList = self._getNodeId(parentId, pathComponents, curPos)
            if 0 == len(nodeIdList):
                raise MpowerException(f'경로를 찾을 수 없습니다. {curPath}')
            elif nextPos == len(pathComponents):
                return [(global_val.ITEM_TYPE_NODE, nodeId) for nodeId in nodeIdList]
            else:
                childNodeIdList = []
                for nodeId in nodeIdList:
                    childNodeIdList.extend(self._getItemTypeAndIdRec(nodeId, pathComponents, nextPos))
                return childNodeIdList

    def _getNodeId(self, parentId:str, pathComponents:list[str], curPos:int) -> tuple[int, list[str]]:
        stmt = self.powerdb_con.createStatement()
        for nextPos in range(curPos + 1, len(pathComponents) + 1):
            nodeName = '/'.join(pathComponents[curPos:nextPos])
            query = (
                'SELECT NODE_ID'
                ' FROM SHARE_NODE_INFO'
                ' WHERE PARENT_ID=%(PARENT_ID)s'
                ' AND NODE_NAME=%(NODE_NAME)s'
            )
            self.powerdb_con.execute(stmt, query, {
                'PARENT_ID': parentId,
                'NODE_NAME': nodeName,
            })
            nodeIdList = [rs['NODE_ID'] for rs in self.powerdb_con.fetchAll(stmt)]
            if len(nodeIdList):
                return nextPos, nodeIdList
        return curPos, []

    def _getSFileIdIfExists(self, nodeId:str, lFileName:str) -> Union[str, None]:
        stmt = self.powerdb_con.createStatement()
        query = (
            'SELECT SFILE_ID'
            ' FROM SHARE_FILE_INFO'
            ' WHERE NODE_ID=%(NODE_ID)s'
            ' AND LFILE_NAME=%(LFILE_NAME)s'
            ' ORDER BY SEQ_ID DESC'
            ' LIMIT 1'
        )
        self.powerdb_con.execute(stmt, query, {
            'NODE_ID': nodeId,
            'LFILE_NAME': lFileName,
        })
        rs = self.powerdb_con.fetchAll(stmt)
        if 0 == len(rs):
            return None
        else:
            rs = rs[0]
        return rs['SFILE_ID']

    def _getSFileIdListInNodeRec(self, nodeId:str) -> Generator[str, None, None]:
        stmt = self.powerdb_con.createStatement()
        query = (
            'WITH CTE_FILE_INFO AS ('
            ' SELECT ROW_NUMBER() OVER (PARTITION BY NODE_ID, LFILE_NAME ORDER BY SEQ_ID DESC) AS VERSION_NUMBER,'
            ' SFILE_ID'
            ' FROM SHARE_FILE_INFO'
            ' WHERE STATUS=%(STATUS)s'
            ' AND NODE_ID=%(NODE_ID)s'
            ' )'
            ' SELECT SFILE_ID FROM CTE_FILE_INFO'
            ' WHERE VERSION_NUMBER=%(VERSION_NUMBER)s'
        )
        self.powerdb_con.execute(stmt, query, {
            'STATUS': '1',
            'NODE_ID': nodeId,
            'VERSION_NUMBER': 1,
        })
        for rs in self.powerdb_con.fetchAll(stmt):
            yield rs['SFILE_ID']
        query = (
            'SELECT NODE_ID'
            ' FROM SHARE_NODE_INFO'
            ' WHERE PARENT_ID=%(PARENT_ID)s'
            ' AND STATUS=%(STATUS)s'
        )
        self.powerdb_con.execute(stmt, query, {
            'PARENT_ID': nodeId,
            'STATUS': '1',
        })
        for rs in self.powerdb_con.fetchAll(stmt):
            for sFileId in self._getSFileIdListInNodeRec(rs['NODE_ID']):
                yield sFileId

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--app-id', dest='appId', required=True, type=str, help='appId')
    parser.add_argument('paths', metavar='path', type=str, nargs='+', help='node or file paths of secure file server to build corpus')

    class _Args:
        appId:str
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

    app = CorpusBuilderApp(powerdb_con, logger, args.appId, list(set(args.paths)))
    app.run()

if __name__ == '__main__':
    try:
        main()
    except MpowerException as e:
        print(e.message, file=sys.stderr)
