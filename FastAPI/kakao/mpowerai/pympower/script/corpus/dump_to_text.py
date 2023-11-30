import sys
import argparse
from pympower.classes.mbase import *
from pympower.classes.mdataset import *
from pympower.classes.mpreprocessing import *

class DumpToTextApp(MBase):
    def __init__(self,
        powerdb_con:MpowerDB2,
        logger:MLogger,
        appId:str,
        dumpDir:str,
        textDir:MDatasetEachFileFormat,
    ):
        self.powerdb_con = powerdb_con
        self.logger = logger
        self.appId = appId
        self.dumpDir = dumpDir
        self.textDir = textDir

    def close(self):
        pass

    def run(self):
        with MFileLocker(os.path.join(global_val.MPOWER_TEMP_DIR, self.appId)):
            self.logger.logging(MLogger.LOG_INFO, 'dump to text')
            self.logger.logging(MLogger.LOG_INFO, f"dumpDir: {self.dumpDir}")
            self.logger.logging(MLogger.LOG_INFO, f"textDir: {self.textDir}")

            dataset = MDataset(self.dumpDir)
            if not dataset.exists():
                raise MpowerException(
                    f'dump directory not exsits {self.dumpDir}'
                )


            writer = MCompositePreprocessor([
                MTupleToValueFilter(0),
                MMultiTextFileLineWriter(self.textDir, 100_000, '', '.txt'),
            ])

            with dataset.getReader() as reader:
                print(list(writer.preprocess(reader.getData(['TEXT']))))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app-id', dest='appId', required=True, type=str, help='appId')
    parser.add_argument('--dump-dir', dest='dumpDir', required=True, type=str, help='path to dump directory')
    parser.add_argument('--text-dir', dest='textDir', required=True, type=str, help='path to output directory')

    class _Args:
        appId:str
        dumpDir:str
        textDir:str
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

    app = DumpToTextApp(powerdb_con, logger, args.appId, args.dumpDir, args.textDir)
    app.run()

if __name__ == '__main__':
    try:
        main()
    except MpowerException as e:
        print(e.message, file=sys.stderr)
