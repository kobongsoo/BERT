import subprocess
from datetime import datetime, timedelta
from importlib.resources import path
import os
import sys
import shutil
from socket import gethostbyname, gethostname, inet_aton, socket
from statistics import mode
from struct import unpack
import time
from unicodedata import decimal
from random import random, randrange
from uuid import uuid4
from typing import Iterable, Generator
# dateutil은 기본으로 설치되어 있지 않다. 
# 따라서 아래 명령어로 설치한다. 
# conda install python-dateutil 
from dateutil.relativedelta import relativedelta

from pympower.common.statuscode import MMessage, StatusCode
from pympower.common.global_val import global_val
from pympower.classes.mbase import *
global_val = global_val.load_global_val();

if 'nt' == os.name:
    import msvcrt
else:
    import fcntl

class MUtility(MBase):
    
    def __init__(self, powerdb_con:MpowerDB2=None):
        super().__init__(powerdb_con);
    
    def close(self):
        pass
    
    def getTestString(self):
        return "test";
    
    def getRFilePath(self, dirCount:int = 10, dirDepth:int = 3):
        rfilePath = '';
        for idx in range(dirDepth):
            rfilePath += str(randrange(0, dirCount)).rjust(3, '0');
            if (idx != (dirDepth - 1)):
                rfilePath += '/';
        return rfilePath;
    
    def getVolumePath(self, volType:int, volId:str, workdb_con:MpowerDB2=None):
        if (workdb_con == None):
            workdb_con = self.powerdb_con;
        query = """
                SELECT VOL_ID, VOL_PATH
                  FROM  STORAGE_INFO
                 WHERE VOL_TYPE = %s
                   AND VOL_ID = %s
                """;
    
        stmt = None;
        try:
            stmt = workdb_con.createStatement();
            workdb_con.execute(stmt=stmt, query=query, args=(volType, volId));
            rs = workdb_con.fetchNext(stmt);
            if (rs != None):
                return rs['VOL_PATH'];
            
        except MpowerException as ex:
            raise ex;  
        finally:
            if stmt:
                workdb_con.closeStmt(stmt);
        return '';                
    
    def getAvailableVolume(self, volType:int, size:int, workdb_con:MpowerDB2 = None):
        if (workdb_con == None):
            workdb_con = self.powerdb_con;
        
        query = """
                SELECT VOL_ID, VOL_PATH, MAX(TOTAL_SPACE-(USED_SPACE+SAFE_SPACE)) AS MAX_VOL
                  FROM  STORAGE_INFO
                 WHERE VOL_TYPE = %s AND STATUS = '1'
                 GROUP BY VOL_ID, VOL_PATH
                 HAVING MAX(TOTAL_SPACE-(USED_SPACE+SAFE_SPACE)) > %s
                 ORDER BY VOL_ID  
                """;

        stmt = None;
        try:
            stmt = workdb_con.createStatement();
            workdb_con.execute(stmt=stmt, query=query, args=(volType, size));
            while (True):
                rs = workdb_con.fetchNext(stmt);
                if (rs == None):
                    break;
                volPath = rs['VOL_PATH'];
                if os.path.exists(path=volPath) == False:
                    raise MpowerException(
                            "volume path not found. (%s)" % (volPath), 
                            StatusCode.SC_OVER_VOL_SIZE.value, workdb_con.getDBIndex(), 
                            'VOL_PATH_NOT_FOUND');
            
            # 디스크 가용량을 확인한다. 
            
        except MpowerException as ex:
            raise ex;  
        finally:
            if stmt:
                workdb_con.closeStmt(stmt);
        return None;                

    def makeUniqueID(self, header:str='', tail:str=''):
        return header + uuid4().hex + tail;

    @staticmethod
    def randomString(len:int = 8):
        temp = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
        rand = "";
        for idx in range(0, 8):
            rand += temp[randrange(0, 61)];
        return rand;    

    def makeMRKUniqueID(self):
        return uuid4().hex;   
    
    def getCurrentTime(self):
        return datetime.now().strftime('%Y%m%d%H%M%S');
    
    def getCurrentDate(self):
        return datetime.now().strftime('%Y%m%d');
    
    def getMillisecondTime(self):
        return round(time.time() * 1000);
    
    def getTimeFromMillisecond(self, ms:int):
        return datetime.fromtimestamp(ms / 1000.0).strftime('%Y%m%d%H%M%S');
    
    def getAfterTime(self, mode:str, val:int, bPlus:bool=True):
        # mode Y: 년,  m: 월, w: 주,  d:일,   H: 시간, i: 분, s:초
        now_time = datetime.now();
        delta = None;
        if mode == "Y":
            delta = relativedelta(years=val);
        elif mode == "m":
            delta = relativedelta(months=val);
        elif mode == "w":
            delta = timedelta(weeks=val);
        elif mode == "d":
            delta = timedelta(days=val);
        elif mode == "H":
            delta = timedelta(hours=val);
        elif mode == "i":
            delta = timedelta(minutes=val);
        elif mode == "s":
            delta = timedelta(seconds=val);
        if (bPlus):
            new_time = now_time + delta;
        else:
            new_time = now_time - delta; 
        return new_time.strftime('%Y%m%d%H%M%S');                       
    
    def getDateTimeFromStr(self, timeStr:str, format:str="%Y%m%d%H%M%S"):
        return datetime.strptime(timeStr, format);
    
    def getDateFormat(self, timeStr:str, format:str="%Y-%m-%d %H:%M:%S"):
        dt = self.getDateTimeFromStr(timeStr=timeStr, format="%Y%m%d%H%M%S");
        return dt.strftime(format);
    
    def DiffDateString(self, curTime:str, timeOpt:str, timeVal:int, bAfter:bool=False):
        # 시간 기준. 1:월, 2:주, 3:일, 4:초, 5:분, 6:시, 7:년
        if curTime == "":
            dt = datetime.now();
        else:
            dt = self.getDateTimeFromStr(timeStr=curTime);
        
        delta = None;
        if timeOpt == "7":
            delta = relativedelta(years=timeVal);
        elif timeOpt == "1":
            delta = relativedelta(months=timeVal);
        elif timeOpt == "2":
            delta = timedelta(weeks=timeVal);
        elif timeOpt == "3":
            delta = timedelta(days=timeVal);
        elif timeOpt == "6":
            delta = timedelta(hours=timeVal);
        elif timeOpt == "5":
            delta = timedelta(minutes=timeVal);
        elif timeOpt == "4":
            delta = timedelta(seconds=timeVal);
        if (bAfter):
            new_time = dt + delta;
        else:
            new_time = dt - delta; 
        return new_time.strftime('%Y%m%d%H%M%S');                       
    
    def getElapsedTime(self, startTime:str, endTime:str, format:str="%Y%m%d%H%M%S"):
        start_dt = self.getDateTimeFromStr(timeStr=startTime, format=format);
        end_dt = self.getDateTimeFromStr(timeStr=endTime, format=format);
        start_time = time.mktime(start_dt.timetuple());
        end_time = time.mktime(end_dt.timetuple());
        return end_time - start_time;
    
    def _ip2long(ip:str):
        return unpack("!L", inet_aton(ip))[0];
    
    def isIPinRange(self, startIP:str, endIP:str, reqIP:str):
        start = self._ip2long(startIP);
        end = self._ip2long(endIP);
        req = self._ip2long(reqIP);
        return (req >= start and req <= end);
    
    
    def getAppName(self, appType:int):
        appName = "unknown";
        if appType == global_val.APP_ADMIN:
            appName = global_val.APP_ADMIN_NAME;
        elif appType == global_val.APP_WEB:
            appName = global_val.APP_WEB_NAME;
        elif appType == global_val.APP_WEB_UPDOWNLOADER:
            appName = global_val.APP_WEB_UPDOWNLOADER_NAME;
        elif appType == global_val.APP_CS:
            appName = global_val.APP_CS_NAME;
        elif appType == global_val.APP_MDRIVE:
            appName = global_val.APP_MDRIVE_NAME;
        elif appType == global_val.APP_MOBILE:
            appName = global_val.APP_MOBILE_NAME;
        elif appType == global_val.APP_EZISC:
            appName = global_val.APP_EZISC_NAME;
        elif appType == global_val.APP_EZISC:
            appName = global_val.APP_EZISC_NAME;
        elif appType == global_val.APP_EZISV:
            appName = global_val.APP_EZISV_NAME;
        elif appType == global_val.APP_INTF:
            appName = global_val.APP_INTF_NAME;
        elif appType == global_val.APP_FORCED_IMPORT:
            appName = global_val.APP_FORCED_IMPORT_NAME;
        elif appType == global_val.APP_BATCH:
            appName = global_val.APP_BATCH_NAME;
        elif appType == global_val.APP_FTP:
            appName = global_val.APP_FTP_NAME;
        elif appType == global_val.APP_EXPORT:
            appName = global_val.APP_EXPORT_NAME;
        return appName;

    def number_format(self, num:float, decimals:int=0):
        new_num = round(num, decimals);
        if decimals == 0:
            new_num = int(new_num);
        return f"{new_num:,}"
    
    def size_format(self, size:float, decimals:int=0):
        unitName = {1:'Bytes', 2:'KB', 3:'MB', 4:'GB', 5:'TB', 6:'PB'};
        numStr = "";
        unitStr = "";
        for idx in range(1, 7):
            if (size < 1024):
                numStr = self.number_format(num=size, decimals=decimals);
                unitStr = unitName[idx];
                break;
            elif (size < pow(1024, idx)):
                numStr = self.number_format(num=(size/pow(1024, idx-1)), decimals=decimals);
                unitStr = unitName[idx];
                break;
        return numStr + " " + unitStr;
    
    def getFileSize(self, path:str, throwEx:bool=True):
        try:
            size = os.path.getsize(path);
        except Exception as ex:
            if (throwEx):
                raise MpowerException(
                        "%s (%s)" % (ex, path), 
                        StatusCode.SC_NOT_OPEN_FILE.value, -1, 
                        'NOT_OBTAIN_FILE_SIZE', 
                        type(ex).__name__);
            else:
                return False;                
        else:
            pass
        finally:
            pass 
        return size;    

    def getDirSize(self, dir:str, throwEx:bool=True):
        total = 0;
        try:
            with os.scandir(dir) as items:
                for item in items:
                    if item.is_file:
                        total += item.stat().st_size;
                    else:
                        subTotal = self.getDirSize(item.path);
                        if subTotal == False:
                            return False;
                        total += subTotal;
        except Exception as ex:
            if (throwEx):
                raise MpowerException(
                        "%s (%s)" % (ex, dir), 
                        StatusCode.SC_NOT_OPEN_FILE.value, -1, 
                        'NOT_OBTAIN_DIR_SIZE', 
                        type(ex).__name__);
            else:
                return False;                
        else:
            pass
        finally:
            pass 
        return total;    

    def get_file_drive(self, path:str):
        return os.path.splitdrive(path)[0];
    
    def get_file_dir(self, path:str):
        return os.path.dirname(path);
    
    def get_file_name(self, path:str):
        baseName = os.path.basename(path);
        return os.path.splitext(baseName)[0];
        
    def get_file_ext(self, path:str):
        return os.path.splitext(path)[1][1:];

    def createAllDirectory(self, dir:str, throwEx=True):
        try:
            os.makedirs(dir, exist_ok=True);
        except Exception as ex:
            if (throwEx):
                raise MpowerException(
                        "%s (%s)" % (ex, dir), 
                        StatusCode.SC_NOT_CREATE_DIR.value, -1, 
                        StatusCode.SC_NOT_CREATE_DIR.name, 
                        type(ex).__name__);
            else:
                return False;                
        else:
            pass
        finally:
            pass 
        return True;    

    def deleteAllDirectory(self, dir:str, throwEx=True):
        try:
            if False == os.path.exists(path=dir):
                return True;
            with os.scandir(path=dir) as items:
                for item in items:
                    fullPath = dir + '/' + item.name;
                    if item.is_file():
                        os.remove(path=fullPath);
                    else:
                        self.deleteAllDirectory(dir=fullPath);
            
            os.rmdir(path=dir);
        except Exception as ex:
            if (throwEx):
                raise MpowerException(
                        "%s (%s)" % (ex, dir), 
                        StatusCode.SC_DELETE_FILE_ERR.value, -1, 
                        StatusCode.SC_DELETE_FILE_ERR.name, 
                        type(ex).__name__);
            else:
                return False;                
        else:
            pass
        finally:
            pass 
        return True;    

    def removeDirectorySeparator(self, path:str):
        path = self.changeDirectorySeparator(path=path);
        return path.rstrip("/");
    
    def changeDirectorySeparator(self, path:str):
        return path.replace("\\", "/").rstrip("/");
    
    def getLocalIP(self):
        return gethostbyname(gethostname());
    
    def isWindows(self):
        if os.name == 'nt':
            return True;
        return False;
    
    def _copy_move_file(self, action:str, src:str, dst:str, overwrite:bool=True):
        try:
            if overwrite == False:
                if os.path.exists(path=dst) and os.path.isfile(path=dst):
                    raise MpowerException(
                            "file already exists. (dst:%s)" % (dst), 
                            StatusCode.CS_FILE_ALREADY_EXISTS.value, -1, 
                            StatusCode.CS_FILE_ALREADY_EXISTS.name);
            dir = self.get_file_dir(path=dst);    
            self.createAllDirectory(dir=dir);
        except MpowerException as ex:
            raise ex;

        # action_error = "";
        errorCode = 0;
        errorName = "";
        try:
            # shutil.copyfile는 기본적으로 덮어쓰기를 해버린다. 
            if (action == "copy"):
                errorCode = StatusCode.SC_ERR_COPY_FILE.value;
                errorName = StatusCode.SC_ERR_COPY_FILE.name;
                shutil.copyfile(src=src, dst=dst);
            elif (action == "move"):
                errorCode = StatusCode.SC_ERR_MOVE_FILE.value;
                errorName = StatusCode.SC_ERR_MOVE_FILE.name;
                shutil.move(src=src, dst=dst);
        except Exception as ex:
            raise MpowerException(
                    "%s (src:%s, dst:%s)" % (ex, src, dst), 
                    errorCode, -1, 
                    errorName, 
                    type(ex).__name__);
        
    def copyFile(self, src:str, dst:str, overwrite:bool=True):
        self._copy_move_file(action="copy", src=src, dst=dst, overwrite=overwrite);
        
    def moveFile(self, src:str, dst:str, overwrite:bool=True):
        self._copy_move_file(action="move", src=src, dst=dst, overwrite=overwrite);        
        
    def removeDirectorySeparator(self, path:str):
        path = self.changeDirectorySeparator(path=path);
        return path.rstrip("/");
    
    def execProcess(self, args:list):
        response = subprocess.run(args, stdout=subprocess.PIPE);
        return response.returncode, response.stdout;
    
    def get_disk_usage(self, path:str, divide:int=1):
        try:
            total, used, free = shutil.disk_usage(path);
            # GiB는 devide를 (2**30), GB는 1024*1024*1024로 처리 
            total = total // divide;
            used = used // divide;
            free = free // divide;
        except Exception as ex:
            raise MpowerException(
                    "failed to get disk usage. %s" % (ex), 
                    StatusCode.CS_DISK_GETSIZE_ERROR.value, -1, 
                    StatusCode.CS_DISK_GETSIZE_ERROR.name,  
                    type(ex).__name__);
        return total, used, free;            
                        
        
        
        #print("Total: %d GiB" % (total // (2**30)))
        #print("Used: %d GiB" % (used // (2**30)))
        #print("Free: %d GiB" % (free // (2**30)))
        
    
    def subClassTest(self):
        return "Main Class";

    def round_robin_merge_max(generators:Iterable) -> Generator:
        '''
        여러개의 generator에서 하나씩 값을 가져와 Round Robin 방식으로
        합치는 함수이다. 길이가 다르다고해서 자르지 않는다.
        '''
        iterators = [iter(generator) for generator in generators]
        i = 0
        while True:
            try:
                text = next(iterators[i % len(iterators)])
                yield text
                i += 1
            except StopIteration:
                iterators.pop(i % len(iterators))
                if 0 == len(iterators):
                    break

    def round_robin_merge_min(generators:Iterable) -> Generator:
        '''
        여러개의 generator에서 하나씩 값을 가져와 Round Robin 방식으로
        합치는 함수이다. 가장 짧은 길이에 맞춰 합치고 나머지는 버린다.
        '''
        iterators = [iter(generator) for generator in generators]
        i = 0
        while True:
            try:
                text = next(iterators[i % len(iterators)])
                yield text
                i += 1
            except StopIteration:
                pass

    def lockFile(self, fd:int):
        if 'nt' == os.name:
            curPos = os.lseek(fd, 0, os.SEEK_CUR)
            os.lseek(fd, 0, os.SEEK_SET)
            try:
                # PermissionError: [Errno 13] Permission denied
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 0x7FFFFFFF)
            except:
                raise MpowerException(
                    f'failed to lock a file',
                    StatusCode.BT_ERR_LOCK_FILE.value, -1, StatusCode.BT_ERR_LOCK_FILE.name,
                )
            finally:
                os.lseek(fd, curPos, os.SEEK_SET)
        else:
            # BlockingIOError: [Errno 11] Resource temporarily unavailable
            try:
                fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB, sys.maxsize, 0, 0)
            except:
                raise MpowerException(
                    f'failed to lock a file',
                    StatusCode.BT_ERR_LOCK_FILE.value, -1, StatusCode.BT_ERR_LOCK_FILE.name,
                )

    def unlockFile(self, fd:int):
        '''
        lockFile을 두 번 호출하고, unlockFile을 한 번 호출하면 잠금이 풀린다.
        '''
        if 'nt' == os.name:
            curPos = os.lseek(fd, 0, os.SEEK_CUR)
            os.lseek(fd, 0, os.SEEK_SET)
            msvcrt.locking(fd, msvcrt.LK_UNLCK, 0x7FFFFFFF)
            os.lseek(fd, curPos, os.SEEK_SET)
        else:
            fcntl.lockf(fd, fcntl.LOCK_UN, sys.maxsize, 0, 0)
