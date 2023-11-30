
################################################################
# 기본 클래스 모듈 
# Circular Import 에러를 회피하기 위해 
# !!!유의 사항!!!
#   MBase, MClassFactory, MLogger, MpowerDB2, MpowerException을 
#   모두 이곳에 선언하여 하나의 모듈로 만들었음. 
################################################################

from abc import *
from datetime import datetime
import importlib
import inspect
import json
import os
from pathlib import Path
from sqlite3 import Cursor
import traceback
import pymysql
from typing import Callable
import re

from pympower.common.global_val import global_val
from pympower.common.session import MSESSION
from pympower.common.statuscode import StatusCode
from pympower.hostname import HostName
global_val = global_val.load_global_val();

class MBase(metaclass=ABCMeta):
 
    def __init__(self, powerdb_con:"MpowerDB2"=None) -> None:
        self.powerdb_con = powerdb_con;
        
    def __del__(self):
        self.close();
    
    @abstractmethod
    def close(self):
        pass
    
    def setDBConn(self, powerdb_con:"MpowerDB2"):
        self.powerdb_con = powerdb_con;
        
    def setLogger(self, logger:"MLogger"):
        self.logger = logger;       
        
class MClassFactory:
    
    #########################################################
    # 반환해야 하는 모듈을 함수내에서 동적으로 import하여
    # import 시의 circular import 에러를 회피한다. 
    #########################################################
    
    @staticmethod
    def getUtility(powerdb_con:"MpowerDB2"=None):
        """ MUtility 클래스를 반환한다. 
            고객사별로 subclass가 존재할 경우 해당 클래스를 반환
            
        Args:
            powerdb_con (MpowerDB2, optional): DB 연결 객체. Defaults to None.

        Returns:
            MUtility: MUtility 또는 subclass
        """        
        from pympower.classes.mutility import MUtility
        if (HostName.GLOBAL_CONFIG_NAME == "gpu"):
            module_name = "pympower.classes.custom.%s_module" % (HostName.GLOBAL_CONFIG_NAME);  
            module = importlib.import_module(name=module_name, package=None);
            obj = module.GPU_MUtility(powerdb_con);
        else:            
            obj = MUtility(powerdb_con);
        return obj;
    
    @staticmethod
    def getSha(powerdb_con:"MpowerDB2" = None):
        from pympower.classes.msha import MSha
        obj = MSha(powerdb_con);
        return obj;
       
    @staticmethod
    def getShaAI(powerdb_con:"MpowerDB2" = None):
        from pympower.classes.mshaai import MShaAI
        obj = MShaAI(powerdb_con);
        return obj;
       
    @staticmethod
    def getMCrypt():
        from pympower.classes.mcrypt import MCrypt
        obj = MCrypt();
        return obj;

       
class MLogger():
    
    LOG_ROLL_OVER = 1;
    LOG_DAILY = 2;
    
    LOG_DEBUG = 101;
    LOG_INFO = 102;
    LOG_ERROR = 103;
    
    def __init__(self, appName:str, userId:str, 
                 logPath:str="", logType:int=LOG_ROLL_OVER) -> None:
        super().__init__();
        self.appName = appName;
        self.userId	= userId;
        self.useConsole = False;
        if MSESSION.defined('use_console_log') and MSESSION.get('use_console_log') == True:
            self.useConsole = True;
        self.logPath = logPath;
        self.logType = logType;
        self.utilClass = MClassFactory.getUtility();
        
        if logPath == "" and MSESSION.defined('log_path'):
            logPath =  MSESSION.get('log_path');
            self.logPath = logPath;
        self.utilClass.createAllDirectory(dir=logPath, throwEx=False);

    def __del__(self):
        LOG_DEBUG = 2;
        self.close();
    
    def close(self):
        pass
        
    def setUseConsole(self, useConsole:bool):
        self.useConsole = useConsole;
        
    def setDebug(self, bDebug:bool):
        if self.logPath == "" or not os.path.exists(self.logPath) or not os.path.isdir(self.logPath):
            return;
        
        debugPath = self.logPath + "/do.debug.log";
        if bDebug == True:
            Path(debugPath).touch(exist_ok=True);
        else:
            if os.path.exists(debugPath) and os.path.isfile(debugPath):
                os.remove(debugPath);
        
    def setLogPath(self, path:str):
        self.utilClass.createAllDirectory(dir=path, throwEx=True);
        self.logPath = path;
        
    def setLogType(self, logType:int):
        self.logType = logType;
        
    def logging(self, logLevel:int, log_text:str, dbidx:int=-1, 
                list1:dict=None, list2:dict=None, list3:dict=None):
        frame = inspect.stack()[1];
        fname = os.path.basename(frame.filename);
        lineno = str(frame.lineno);
        function = frame.function;
        if function == '<module>':
            function = "";
        else:
            function = ":" + function;
        
        if list1 != None and len(list1) > 0:
            log_text += "\n" + json.dumps(list1);
        if list2 != None and len(list2) > 0:
            log_text += "\n" + json.dumps(list2);
        if list3 != None and len(list3) > 0:
            log_text += "\n" + json.dumps(list3);
        
        self._logging(logLevel=logLevel, log_text=log_text, dbidx=dbidx, 
                 fname=fname, lineno=lineno, function=function);
        
    def exceptionLogging(self, logLevel:int, ex:"MpowerException", 
                         prefix:str='', 
                         list1:dict=None, list2:dict=None, list3:dict=None):
        
        frame = inspect.stack()[1];
        fname = os.path.basename(frame.filename);
        lineno = str(frame.lineno);
        function = frame.function;
        if function == '<module>':
            function = "";
        else:
            function = ":" + function;
        
        dbidx = ex.getDBIdx();
        native = "";
        if ex.getNative() != "":
            native = ", native=" + ex.getNative();
        log_text = "%s%s, code:%d%s\n%s\n" % (prefix, ex.getMessage(), ex.getCode(), native, ex.getTrace());
        
        if list1 != None and len(list1) > 0:
            log_text += " " + json.dump(list1);
        if list2 != None and len(list2) > 0:
            log_text += " " + json.dump(list2);
        if list3 != None and len(list3) > 0:
            log_text += " " + json.dump(list3);
            
        self._logging(logLevel=logLevel, log_text=log_text, dbidx=dbidx, 
                 fname=fname, lineno=lineno, function=function);
            
    def _logging(self, logLevel:int, log_text:str, dbidx:int, 
                 fname:str, lineno:str, function:str):
        if logLevel == MLogger.LOG_DEBUG:
            debugPath = self.logPath + '/' + 'do.debug.log';
            if False == os.path.exists(debugPath):
                return;
        
        logtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S');
        self.utilClass.createAllDirectory(self.logPath);
        
        strLogLevel = 'UNKNOWN';
        if logLevel == MLogger.LOG_DEBUG:
            strLogLevel = 'DEBUG';
        elif logLevel == MLogger.LOG_INFO:
            strLogLevel = 'INFO';
        elif logLevel == MLogger.LOG_ERROR:
            strLogLevel = 'ERROR';
        
        message = "%s [%s][%s][%s][%s%s:%s:%d] %s\n" % \
                (logtime, self.userId, HostName.HOST_NAME, strLogLevel, \
                 fname, function, lineno, dbidx, log_text);
        
        # 콘솔 로그를 남긴다. 
        if self.useConsole:
            print(message);

        logday = self.utilClass.getCurrentDate();
        
        # 일반 파일 로그
        if (self.logType == MLogger.LOG_DAILY):
            filename = "%s/%s_%s_%s.log" % (self.logPath, self.appName, self.userId, logday);
        else:
            filename = "%s/%s_%s.log" % (self.logPath, self.appName, self.userId);

        fd = open(filename, "a");
        if (fd):
            fd.write(message);
            fd.close();
            if logLevel == MLogger.LOG_DAILY:
                self._rollover_logfile(
                            bError=False, logFilePath=filename, logPath=self.logPath, 
                            appName=self.appName, userId=self.userId);
            
        # 에러 로그 
        if logLevel == MLogger.LOG_ERROR:
            if (self.logType == MLogger.LOG_DAILY):
                filename = "%s/%s_%s_%s.error.log" % (self.logPath, self.appName, self.userId, logday);
            else:
                filename = "%s/%s_%s.error.log" % (self.logPath, self.appName, self.userId);
            fd = open(filename, "a");
            if (fd):
                fd.write(message);
                fd.close();
                if logLevel == MLogger.LOG_DAILY:
                    self._rollover_logfile(
                                bError=True, logFilePath=filename, logPath=self.logPath, 
                                appName=self.appName, userId=self.userId);

        if self.logType == MLogger.LOG_DAILY:
            # rollover를 수행한다. 
            pass 
        
        
    def _rollover_logfile(self, 
                          bError:bool, logFilePath:str, logPath:str, appName:str, userId:str):
        fileSize = self.utilClass.getFileSize(path=logFilePath, throwEx=False);
        if (fileSize == False or fileSize <= global_val.MPOWER_LOGFILE_SIZE):
            return;
        if bError:
            lastIdx = global_val.MPOWER_ERROR_LOGFILE_IDX;
            ext = '.error.log.';
        else:
            lastIdx = global_val.MPOWER_LOGFILE_IDX;
            ext = '.log.';
        # 마지막 파일을 지운다.
        lastFilePath = "%s/%s_%s%s%s" % (logPath, appName, userId, ext, str(lastIdx).rjust(2, '0'));
        os.remove(path=lastFilePath);
        
        # 기존 파일들의 인덱스를 변경한다. 
        idx = lastIdx - 1;
        while (idx > 0):
            oldLogFilePath = "%s/%s_%s%s%s" % (logPath, appName, userId, ext, str(idx).rjust(2, '0'));
            newLogFilePath = "%s/%s_%s%s%s" % (logPath, appName, userId, ext, str(idx+1).rjust(2, '0'));
            os.rename(oldLogFilePath, newLogFilePath);
        
class MpowerDB2:
    
    def __init__(self, dbkind:int = global_val.DB_KIND):
        self.host = '127.0.0.1';
        self.port = 3306;
        self.user = 'Mpower10U';
        self.password = 'manager@.!';
        self.dbname = 'Mpower10U';
        self.dbkind = dbkind;
        self.dbidx = -1;
        self.conn = None;
        self.logger = None;
        self.useDebug = False;
        if MSESSION.defined('lol_appName') and MSESSION.defined('lol_ids81'):
            self.logger = MLogger(
                MSESSION.get('lol_appName') + "_db", 
                MSESSION.get('lol_ids81'));
    
    def __del__(self):
        self.close();
    
    def setDebugLog(self, useDebug:bool):
        self.useDebug = useDebug;
    
    def getDBKind(self):
        return self.dbkind;
    
    def setDBKind(self, dbkind:int):
        self.dbkind = dbkind;
        
    def getDBIndex(self):
        return self.dbidx;

    def inTransaction(self):
        # 어떻게 얻어내는지 확인 필요 
        pass
    
    def rowCount(self, cur:Cursor):
        return cur.rowcount;
    
    def getDummyFrom(self):
        if self.dbkind == global_val.ORACLE:
            return ' FROM DUAL ';
        return '';
    
    @staticmethod
    def getLimitQuery(page_per_count:int, page:int, dbkind:int):
        limit = '';
        if page_per_count and page:
            start = (page * page_per_count) - page_per_count;
            if dbkind == global_val.__MYSQL:
                limit = "LIMIT %d, %d" % (start, page_per_count);
            elif dbkind == global_val.MSSQL:
                limit = "OFFSET %d ROWS FETCH NEXT %d ROWS ONLY" % (start, page_per_count); # MS SQL Server 2012 부터 지원 - Order by 구문이 쿼리에 포함 되어 있어야 한다.
            elif dbkind == global_val.ORACLE: 
                limit = "OFFSET %d ROWS FETCH NEXT %d ROWS ONLY" % (start, page_per_count); # Oracle 12c 부터 지원 - Order by 구문이 쿼리에 포함 되어 있어야 한다.
            else:
                raise MpowerException(
                    "not supported dbkind. %d" % (dbkind), 
                    StatusCode.SC_DB_ERROR.value, -1, 
                    StatusCode.SC_DB_ERROR.name, 
                    'NOT_SUPPORT_DB_KIND');
        return limit;
    
    def checkDBKind(self):
        if self.dbkind != global_val.MYSQL:
            raise MpowerException(
                "not supported dbkind. %d" % (self.dbkind), 
                StatusCode.SC_DB_ERROR.value, self.dbidx, 
                StatusCode.SC_DB_ERROR.name, 
                'NOT_SUPPORT_DB_KIND');
        return True;            
    
    def setLogger(self, logger:MLogger):
        self.logger = logger;
    
    def connectWithIndex(self, dbidx:int = 0, dbkind:int=global_val.DB_KIND):
        self.connect(
            host=HostName.DB_LIST_INFO[dbidx]['ADDR'], 
            port=HostName.DB_LIST_INFO[dbidx]['PORT'], 
            user=HostName.DB_LIST_INFO[dbidx]['UID'], 
            password=HostName.DB_LIST_INFO[dbidx]['PWD'], 
            dbname=HostName.DB_LIST_INFO[dbidx]['DB_NAME'], 
            dbkind=dbkind);
        self.dbidx = dbidx;
    
    def connect(self, host:str, port:int, user:str, password:str, dbname:str, dbkind:int=global_val.DB_KIND):
        self.host = host;
        self.port = port;
        self.user = user;
        self.password = password;
        self.dbname = dbname;
        self.dbkind = dbkind;
        
        try:
            self.checkDBKind();
            self.conn = pymysql.connect(host=self.host, 
                                        port=self.port, 
                                        user=self.user, 
                                        password=self.password, 
                                        db=self.dbname);
        except Exception as ex:
            raise MpowerException(
                    "failed to connect to DB. %s" % (ex), 
                    StatusCode.SC_DB_ERROR.value, self.dbidx, 
                    StatusCode.SC_DB_ERROR.name, 
                    type(ex).__name__);
        else:
            pass
        finally:
            pass 
            
    def createStatement(self):
        try:
            stmt = self.conn.cursor(pymysql.cursors.DictCursor);
        except Exception as ex:
            raise MpowerException(
                    "failed to create curosr. %s" % (ex), 
                    StatusCode.SC_DB_ERROR.value, self.dbidx, 
                    StatusCode.SC_DB_ERROR.name, 
                    type(ex).__name__);
        else:
            pass
        finally:
            pass 
        return stmt;
            
    def get_sql_string(self, query:str, args=[]):
        unique = "%PARAMETER%";
        query = query.replace("%s", unique);
        for v in args: query = query.replace(unique, repr(v), 1);
        return query;
            
    def execute(self, stmt:Cursor, query:str, args=[]):
        try:
            stmt.execute(query, args);
            if (self.useDebug and self.logger):
                sql = self.get_sql_string(query, args);
                self.logger.logging(MLogger.LOG_DEBUG, "sql: %s" % (sql), self.dbidx);
        except Exception as ex:
            sql = self.get_sql_string(query, args);
            raise MpowerException(
                    "%s. sql:\n%s" % (ex, sql), 
                    StatusCode.SC_SQL_ERROR.value, self.dbidx, 
                    StatusCode.SC_SQL_ERROR.name, 
                    type(ex).__name__);
        else:
            pass
        finally:
            pass 
    
    def fetchNext(self, stmt:Cursor):
        try:
            rs = stmt.fetchone();
        except Exception as ex:
            raise MpowerException(
                    "%s" % (ex), 
                    StatusCode.SC_SQL_ERROR.value, self.dbidx, 
                    StatusCode.SC_SQL_ERROR.name, 
                    type(ex).__name__);
        else:
            pass
        finally:
            pass 
        return rs;
    
    def fetchAll(self, stmt:Cursor):
        try:
            rs = stmt.fetchall();
        except Exception as ex:
            raise MpowerException(
                    "%s" % (ex), 
                    StatusCode.SC_SQL_ERROR.value, self.dbidx, 
                    StatusCode.SC_SQL_ERROR.name, 
                    type(ex).__name__);
        else:
            pass
        finally:
            pass 
        return rs;
    
    def begin(self):
        try:
            self.conn.begin();
        except Exception as ex:
            raise MpowerException(
                    "begin error. %s" % (ex), 
                    StatusCode.SC_SQL_ERROR.value, self.dbidx, 
                    StatusCode.SC_SQL_ERROR.name, 
                    type(ex).__name__);
        else:
            pass
        finally:
            pass 
    
    def commit(self):
        try:
            self.conn.commit();
        except Exception as ex:
            raise MpowerException(
                    "commit error. %s" % (ex), 
                    StatusCode.SC_SQL_ERROR.value, self.dbidx, 
                    StatusCode.SC_SQL_ERROR.name, 
                    type(ex).__name__);
        else:
            pass
        finally:
            pass 
            
    def rollback(self):
        try:
            self.conn.commit();
        except Exception as ex:
            raise MpowerException(
                    "rollback error. %s" % (ex), 
                    StatusCode.SC_SQL_ERROR.value, self.dbidx, 
                    StatusCode.SC_SQL_ERROR.name, 
                    type(ex).__name__);
        else:
            pass
        finally:
            pass 
        
    def closeStmt(self, stmt:Cursor):
        if stmt != None:
            stmt.close();
        
    def close(self):
        try:
            if self.conn != None:
                self.conn.close();
        except Exception as ex:
            raise MpowerException(
                    "close error. %s" % (ex), 
                    StatusCode.SC_SQL_ERROR.value, self.dbidx, 
                    StatusCode.SC_SQL_ERROR.name, 
                    type(ex).__name__);
        else:
            pass
        finally:
            self.conn = None;        
        
class MpowerException(Exception):
    
    def __init__(self, msg, code=0, dbidx=-1, brief='', native=''):
        super().__init__(msg, code, dbidx, brief, native);
        self.message = msg;
        self.code = code;
        self.dbidx = dbidx;
        self.brief = brief;
        self.native = native;
        
    def getCode(self):
        return self.code;

    def getMessage(self):
        return self.message;

    def getDBIdx(self):
        return self.dbidx;

    def getBrief(self):
        return self.brief;
        
    def getNative(self):
        return self.native;
    
    def getTrace(self):
        return traceback.format_exc();

class MToFromConfigClass(metaclass=ABCMeta):
    '''
    객체 정보를 설정으로 내보내고, 그 내보낸 설정 정보로 다시 객체를 생성할 수 있는 기능을 제공하는 인터페이스이다.
    '''

    @staticmethod
    @abstractmethod
    def createFromConfig(config:dict) -> 'MToFromConfigClass':
        pass

    @abstractmethod
    def exportToConfig(self) -> dict:
        '''
        JSON으로 인코딩할 수 있는 클래스 정보를 내보낸다.
        '''
        pass

class MToFromConfigClassFactory:
    def __init__(self):
        self.factory_methods:dict[str, Callable] = {}

    def addFactoryMethod(self, name:str, factoryMethod:Callable):
        if name in self.factory_methods:
            raise MpowerException(
                f"class '{name}' already exists.",
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )

        self.factory_methods[name] = factoryMethod

    def addFactoryMethods(self, factoryMethods:dict[str, Callable]):
        for name in factoryMethods:
            self.addFactoryMethod(name, factoryMethods[name])

    def addClass(self, klass:type[MToFromConfigClass]):
        self.addFactoryMethod(klass.__name__, klass.createFromConfig)

    def addClasses(self, classes:list[type[MToFromConfigClass]]):
        for klass in classes:
            self.addClass(klass)

    def createInstance(self, name:str, config:dict) -> MToFromConfigClass:
        factory_method = self.factory_methods[name]
        return factory_method(config)

    def createInstanceFromConfig(self, factoryConfig:dict) -> MToFromConfigClass:
        return self.createInstance(
            name=factoryConfig['name'],
            config=factoryConfig['config'],
        )

    def exportInstanceToConfig(self, instance:MToFromConfigClass) -> dict:
        return {
            'name': type(instance).__name__,
            'config': instance.exportToConfig(),
        }

class MFileLocker:
    def __init__(self, path:str, *, deleteOnClose:bool = True, useLockCount:bool = False):
        self.path = path
        self.deleteOnClose = deleteOnClose
        self.useLockCount = useLockCount

        self.file = None
        self.lockCount = 0
        self.utilClass = MClassFactory.getUtility()

    def __del__(self):
        if 0 != self.lockCount:
            raise MpowerException(
                f'File locker deleted without unlock. path:{self.path}, lockCount:{self.lockCount}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )

    def __enter__(self) -> 'MFileLocker':
        self.lock()
        return self

    def __exit__(self, type, value, traceback):
        self.unlock()

    def hasLockOwnership(self) -> bool:
        return None != self.file

    def lock(self) -> int:
        if self.hasLockOwnership():
            if self.useLockCount:
                self.lockCount += 1
                return
            else:
                raise MpowerException(
                    f'file has already been locked. path:{self.path}',
                    StatusCode.BT_ERR_LOCK_FILE.value, -1, StatusCode.BT_ERR_LOCK_FILE.name
                )
        try:
            self.file = open(self.path, 'w')
        except:
            raise MpowerException(
                f'failed to open a lock file. path:{self.path}',
                StatusCode.BT_ERR_CREATE_LOCK_FILE.value, -1, StatusCode.BT_ERR_CREATE_LOCK_FILE.name,
            )
        try:
            self.utilClass.lockFile(self.file.fileno())
        except:
            self.file = None
            if self.deleteOnClose:
                os.remove(self.path)
            raise MpowerException(
                f'failed to lock a file. path:{self.path}',
                StatusCode.BT_ERR_LOCK_FILE.value, -1, StatusCode.BT_ERR_LOCK_FILE.name,
            )

        self.lockCount += 1
        return self.lockCount

    def unlock(self) -> int:
        if False == self.hasLockOwnership():
            raise MpowerException(
                f'file has not been locked. path:{self.path}',
                StatusCode.SC_INTERNAL_ERROR.value, -1, StatusCode.SC_INTERNAL_ERROR.name
            )
        self.lockCount -= 1
        if 0 == self.lockCount:
            self.file.close()
            self.file = None
            if self.deleteOnClose:
                os.remove(self.path)
        return self.lockCount
