import sys
import argparse
from pympower.classes.mbase import *
from pympower.common.global_val import *
global_val = global_val.load_global_val()

class CorpusCheckerArgs:
    checkExistence:bool
    checkUnhandledFiles:bool
    checkDeleted:bool

class CorpusCheckerApp(MBase):
    def __init__(self, powerdb_con:MpowerDB2, args:CorpusCheckerArgs):
        super().__init__(powerdb_con)

        self.args = args

    def close(self):
        pass

    def run(self):
        if self.args.checkExistence:
            print('checking existence')
            self._checkCFileExistence()

        if self.args.checkUnhandledFiles:
            print('checking unhadled files')
            self._checkUnhandledFiles()

        if self.args.checkDeleted:
            print('checking deleted files')
            self._checkDeleted()

    def _checkCFileExistence(self):
        stmt = self.powerdb_con.createStatement()
        query = (
            'SELECT CFILE_ID, VOL_PATH, CFILE_PATH, CFILE_NAME'
            ' FROM CORPUS_FILE_INFO C, STORAGE_INFO S'
            ' WHERE C.VOL_ID=S.VOL_ID'
        )
        self.powerdb_con.execute(stmt, query)
        allRs = self.powerdb_con.fetchAll(stmt)
        for index, rs in enumerate(allRs, start=1):
            print(f'\r[{index}/{len(allRs)}]', end='')
            sys.stdout.flush()
            path = os.path.join(rs['VOL_PATH'], rs['CFILE_PATH'], rs['CFILE_NAME'])
            if False == os.path.exists(path):
                print(f"\r{rs['CFILE_ID']} not exists")
                sys.stdout.flush()

    def _checkUnhandledFiles(self):
        stmt = self.powerdb_con.createStatement()
        query = 'SELECT VOL_ID, VOL_PATH FROM STORAGE_INFO WHERE VOL_TYPE=%(VOL_TYPE)s'
        self.powerdb_con.execute(stmt, query, {
            'VOL_TYPE': global_val.CORPUS_DISK
        })
        for rs in self.powerdb_con.fetchAll(stmt):
            print(f"checking: {rs['VOL_PATH']}")
            fileList:list[str] = []
            for root, _, files in os.walk(rs['VOL_PATH']):
                for cFileName in files:
                    fileList.append((root, cFileName))
            for index, (root, cFileName) in enumerate(fileList, start=1):
                cFilePath = os.path.relpath(root, rs['VOL_PATH'])
                print(f'\r[{index}/{len(fileList)}] {cFilePath} {cFileName}', end='')
                sys.stdout.flush()
                query = (
                    'SELECT STATUS'
                    ' FROM CORPUS_FILE_INFO'
                    ' WHERE VOL_ID=%(VOL_ID)s'
                    ' AND CFILE_PATH=%(CFILE_PATH)s'
                    ' AND CFILE_NAME=%(CFILE_NAME)s'
                )
                self.powerdb_con.execute(stmt, query, {
                    'VOL_ID': rs['VOL_ID'],
                    'CFILE_PATH': cFilePath,
                    'CFILE_NAME': cFileName,
                })
                if 0 == len(self.powerdb_con.fetchAll(stmt)):
                    path = os.path.join(root, cFileName)
                    print(f'\r{path} information not found in db.')
                    sys.stdout.flush()

    def _checkDeleted(self):
        stmt = self.powerdb_con.createStatement()
        query = (
            'SELECT C.CFILE_ID, C.RFILE_NAME, F.STATUS'
            ' FROM CORPUS_FILE_INFO C'
            ' LEFT OUTER JOIN SHARE_FILE_INFO F'
            ' ON C.RFILE_NAME=F.RFILE_NAME'
            ' WHERE C.PARENT_ID IS NULL'
            ' AND (F.RFILE_NAME IS NULL OR F.STATUS<>%(STATUS)s)'
        )
        self.powerdb_con.execute(stmt, query, {
            'STATUS': 1,
        })
        deletedCount = 0
        for rs in self.powerdb_con.fetchAll(stmt):
            query = (
                'SELECT STATUS'
                ' FROM SHARE_FILE_INFO'
                ' WHERE RFILE_NAME=%(RFILE_NAME)s'
                ' AND STATUS=%(STATUS)s'
            )
            self.powerdb_con.execute(stmt, query, {
                'RFILE_NAME': rs['RFILE_NAME'],
                'STATUS': 1,
            })
            if 0 == len(self.powerdb_con.fetchAll(stmt)):
                print(f"{rs['CFILE_ID']} deleted. status={rs['STATUS']}")
                deletedCount += 1
        print(f"{deletedCount} files deleted.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--check-existence',
        dest='checkExistence',
        action=argparse.BooleanOptionalAction,
        help='check existence'
    )
    parser.set_defaults(checkExistence=False)
    parser.add_argument(
        '--check-unhandled-files',
        dest='checkUnhandledFiles',
        action=argparse.BooleanOptionalAction,
        help='check unhandled files'
    )
    parser.set_defaults(checkUnhandledFiles=False)
    parser.add_argument(
        '--check-deleted',
        dest='checkDeleted',
        action=argparse.BooleanOptionalAction,
        help='check deleted files'
    )
    parser.set_defaults(checkUnhandledFiles=False)

    args:CorpusCheckerArgs = parser.parse_args()

    powerdb_con = MpowerDB2()
    powerdb_con.connectWithIndex()

    app = CorpusCheckerApp(powerdb_con, args)
    app.run()

if __name__ == '__main__':
    main()