import sys
import argparse
from pathlib import Path
from tqdm import tqdm
from pympower.classes.mbase import *
from pympower.classes.mcorpus import *

class CorpusRemoverApp(MBase):
    def __init__(self, powerdb_con:MpowerDB2, logger:MLogger, appId:str, dryRun:bool, paths:list[str]):
        self.powerdb_con = powerdb_con
        self.logger = logger
        self.appId = appId
        self.dryRun = dryRun
        self.paths = paths

    def close(self):
        pass

    def run(self):
        with MFileLocker(os.path.join(global_val.MPOWER_TEMP_DIR, self.appId)):
            self.logger.logging(MLogger.LOG_INFO, f"druRun: {self.dryRun}")
            self.logger.logging(MLogger.LOG_INFO, 'deleting source paths')
            for path in self.paths:
                self.logger.logging(MLogger.LOG_INFO, f'- {path}')

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
            self.logger.logging(MLogger.LOG_INFO, f"deleting checking. count:{len(allRs)}")

            for rs in tqdm(allRs, ncols=120, ascii=True):
                pathMatched = 0
                paths = remover.getPaths(rs['RFILE_NAME'])
                for path in paths:
                    for pathToDelete in self.paths:
                        if Path(path).is_relative_to(pathToDelete):
                            pathMatched += 1
                if len(paths) != pathMatched:
                    continue

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
                        self.logger.logging(MLogger.LOG_ERROR, f"{rs['CFILE_ID']}: deleting error. message:{e.message}")
                    except Exception as e:
                        errorCount += 1
                        self.logger.logging(MLogger.LOG_ERROR, f"{rs['CFILE_ID']}: deleting error. message:{str(e)}")

            self.logger.logging(MLogger.LOG_INFO, f'deleted: {deletedCount}')
            self.logger.logging(MLogger.LOG_INFO, f'error: {errorCount}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app-id', dest='appId', required=True, type=str, help='appId')
    parser.add_argument('--dry-run', dest='dryRun', action='store_true', default=False, help='dry run')
    parser.add_argument('paths', metavar='path', type=str, nargs='+', help='node or file paths to delete corpus')

    class _Args:
        appId:str
        dryRun:bool
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

    app = CorpusRemoverApp(powerdb_con, logger, args.appId, args.dryRun, args.paths)
    app.run()

if __name__ == '__main__':
    try:
        main()
    except MpowerException as e:
        print(e.message, file=sys.stdout)

