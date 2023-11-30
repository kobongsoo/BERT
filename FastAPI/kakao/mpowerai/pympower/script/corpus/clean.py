import sys
import argparse
from tqdm import tqdm
from pympower.classes.mbase import *
from pympower.classes.mcorpus import *
from pympower.classes.mscript import *

class CorpusCleanerApp(MBase):
    '''
    CORPUS_FILE_INFO에 있는 항목을 조사하여 다음 조건에 해당하는 파일을 삭제한다.
    1. SHARE_FILE_INFO에서 삭제된 파일
    2. SHARE_FILE_INFO에서 최신 버전이 아닌 파일
    '''
    def __init__(self, powerdb_con:MpowerDB2, logger:MLogger, appId:str, dryRun:bool):
        self.powerdb_con = powerdb_con
        self.logger = logger
        self.appId = appId
        self.dryRun = dryRun

    def close(self):
        pass

    def run(self):
        with MFileLocker(os.path.join(global_val.MPOWER_TEMP_DIR, self.appId)):
            MStopEvent.setup()

            remover = MCorpusBuilder(self.powerdb_con)
            stmt = self.powerdb_con.createStatement()
            query = (
                'SELECT CFILE_ID, RFILE_NAME'
                ' FROM CORPUS_FILE_INFO'
                ' WHERE PARENT_ID IS NULL'
            )
            self.powerdb_con.execute(stmt, query)
            deletedCount = 0
            errorCount = 0
            allRs = self.powerdb_con.fetchAll(stmt)
            self.logger.logging(MLogger.LOG_INFO, f"cleaner checking. count:{len(allRs)}")
            self.logger.logging(MLogger.LOG_INFO, f"druRun: {self.dryRun}")
            for rs in tqdm(allRs, ncols=120, ascii=True):
                if MStopEvent.isSignaled():
                    self.logger.logging(MLogger.LOG_INFO, f'stop event has signaled')
                    break
                query = (
                    'SELECT RFILE_NAME'
                    ' FROM (SELECT RFILE_NAME, STATUS,'
                    ' ROW_NUMBER() OVER (PARTITION BY F.NODE_ID, F.LFILE_NAME ORDER BY SEQ_ID DESC) AS VERSION_NUMBER'
                    ' FROM SHARE_FILE_INFO F,'
                    ' (SELECT NODE_ID, LFILE_NAME FROM SHARE_FILE_INFO WHERE RFILE_NAME=%(RFILE_NAME)s) V'
                    ' WHERE F.NODE_ID=V.NODE_ID AND F.LFILE_NAME=V.LFILE_NAME'
                    ' ) X'
                    ' WHERE STATUS<>%(STATUS_1)s OR VERSION_NUMBER<>%(VERSION_NUMBER_1)s'
                    ' GROUP BY RFILE_NAME'
                )
                self.powerdb_con.execute(stmt, query, {
                    'RFILE_NAME': rs['RFILE_NAME'],
                    'STATUS_1': '1',
                    'VERSION_NUMBER_1': 1,
                })
                rsShareFileInfo = self.powerdb_con.fetchAll(stmt)
                if 0 == len(rsShareFileInfo):
                    continue
                rsShareFileInfo = rsShareFileInfo[0]

                if self.dryRun:
                    deletedCount += 1
                    self.logger.logging(MLogger.LOG_INFO, f"{rs['CFILE_ID']}: deleted (dryRun).")
                else:
                    try:
                        remover.remove(rs['RFILE_NAME'])
                        deletedCount += 1
                        self.logger.logging(MLogger.LOG_INFO, f"{rs['CFILE_ID']}: deleted.")
                    except MpowerException as e:
                        errorCount += 1
                        self.logger.logging(MLogger.LOG_ERROR, f"{rs['CFILE_ID']}: error. message:{e.message}")
                    except Exception as e:
                        errorCount += 1
                        self.logger.logging(MLogger.LOG_ERROR, f"{rs['CFILE_ID']}: error. message:{str(e)}")

            self.logger.logging(MLogger.LOG_INFO, f'deleted: {deletedCount}')
            self.logger.logging(MLogger.LOG_INFO, f'error: {errorCount}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', dest='dryRun', action='store_true', default=False, help='dry run')

    class _Args:
        dryRun:bool
    args:_Args = parser.parse_args()

    powerdb_con = MpowerDB2()
    powerdb_con.connectWithIndex()

    mainModuleFilePath = Path(sys.modules[__name__].__file__)
    logger = MLogger(
        mainModuleFilePath.stem,
        '',
        os.path.join(global_val.MPOWER_LOG_PATH, mainModuleFilePath.parent.parent.name, mainModuleFilePath.parent.name),
        MLogger.LOG_DAILY,
    )

    app = CorpusCleanerApp(powerdb_con, logger, 'clean-single', args.dryRun)
    app.run()

if __name__ == '__main__':
    try:
        main()
    except MpowerException as e:
        print(e.message, file=sys.stdout)

