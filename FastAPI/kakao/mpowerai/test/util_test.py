###################################################
# Util 클래스 예제 프로그램 
# 파일 처리를 위해 nlp_sample의 경로를 지정하고 테스트 해야 함. 
###################################################

import sys
from os import path
# 모듈 import를 위해 MPOWER_AI_HOME 경로를 설정한다. 
# 본 프로그램은 MPOWER_AI_HOME/test에 위치하므로, 상위 디렉토리를 설정한다. 
MPOWER_AI_HOME=path.dirname(path.dirname(path.abspath(__file__)));
sys.path.append(MPOWER_AI_HOME);

import os
from ctypes import util
from datetime import datetime
from random import random, randrange
import traceback
from uuid import UUID, uuid4
from pympower.common.session import MSESSION
from pympower.common.global_val import global_val
from pympower.classes.mbase import *
from pympower.classes.mutility import MUtility
global_val = global_val.load_global_val();
from pympower.hostname import HostName
HostName.setMPOWER_AI_HOME(MPOWER_AI_HOME);

MSESSION.set('lol_ids81', 'SYSTEM');
MSESSION.set('lol_ids81_name', 'SYSTEM');
MSESSION.set('lol_dbIdx', 0);
MSESSION.set('lol_orgId', '');
MSESSION.set('lol_appType', global_val.APP_BATCH);
MSESSION.set('lol_appName', os.path.splitext(os.path.basename(__file__))[0]);
MSESSION.set("log_path", path.dirname(path.abspath(__file__)) + "/logs");
MSESSION.set('use_console_log', True);

print('start');

powerdb_con = None;
stmt = None;
logger = None;
utilClass = None;
try:
    logger = MLogger(appName=MSESSION.get("lol_appName"), userId=MSESSION.get("lol_ids81"));
    logger.setDebug(True);
    logger.logging(MLogger.LOG_DEBUG, "start app");
    
    powerdb_con = MpowerDB2();
    powerdb_con.setLogger(logger=logger);
    powerdb_con.connectWithIndex();
    stmt = powerdb_con.createStatement();

    utilClass = MClassFactory.getUtility(powerdb_con);
    utilClass.setLogger(logger=logger);
    
    # subclass 테스트 
    # HostName.GLOBAL_CONFIG_NAME = 'gpu'로 설정되어 있음. 
    # MClassFactory.getUtility 에서 'gpu'일 경우 
    # pympower.classes.custom.gpu_module내의 GPU_MUtility를 반환하도록 되어 있음
    # 해당 subclass가 인스턴스로 반환되었는지를 테스트 하기 위함임. 
    # "Sub Class"가 출력되어져야 함. 
    print(utilClass.subClassTest());

    ############################
    # File Util
        
    if HostName.GLOBAL_CONFIG_NAME == "skchoi":
        testHomeDir = "E:/test";
    else:
        testHomeDir = "/MOCOMSYS";                
    src_dir = testHomeDir + "/nlp_sample";
    src_dir = utilClass.changeDirectorySeparator(src_dir);
    logger.logging(MLogger.LOG_DEBUG, "replaced dir:%s" % (src_dir));
    
    # disk 사용량
    total, used, free = utilClass.get_disk_usage(src_dir);
    logger.logging(MLogger.LOG_DEBUG, "bytes: %d %d %d" % (total, used, free));
    total, used, free = utilClass.get_disk_usage(src_dir, 2**30);
    logger.logging(MLogger.LOG_DEBUG, "GiB: %d %d %d" % (total, used, free));
    total, used, free = utilClass.get_disk_usage(src_dir, 1024*1024*1024);
    logger.logging(MLogger.LOG_DEBUG, "GB: %d %d %d" % (total, used, free));
    
    # 파일 및 디렉토리 크기 
    path = src_dir + "/excel/excel sheet text.xlsx";
    logger.logging(MLogger.LOG_DEBUG, 
                   "dir:%s, fname:%s, ext:%s" % 
                   (utilClass.get_file_dir(path), utilClass.get_file_name(path), utilClass.get_file_ext(path))
                   );
    fsize = utilClass.getFileSize(path=path, throwEx=False);
    logger.logging(MLogger.LOG_DEBUG, "size:%d" % (fsize));
    dsize = utilClass.getDirSize(dir=src_dir, throwEx=False);
    logger.logging(MLogger.LOG_DEBUG, "dir size:%d" % (dsize));
            
    # 디렉토리 삭제 및 생성             
    test_dir = testHomeDir + "/nlp_result/test";
    utilClass.deleteAllDirectory(dir=test_dir);
    new_dir = test_dir + "/n1/n2/n3/n4";
    utilClass.createAllDirectory(dir=new_dir);
    
    # 파일 복사
    src = src_dir + "/excel/excel sheet text.xlsx"
    dst = test_dir + "/n1/excel sheet text.xlsx";
    utilClass.copyFile(src=src, dst=dst);
    logger.logging(MLogger.LOG_DEBUG, "copy file, src:%s, dst:%s" % (src, dst));
    
    # 파일 이동 
    src = dst;
    dst = test_dir + "/n2/excel sheet text.xlsx"
    utilClass.moveFile(src=src, dst=dst);
    logger.logging(MLogger.LOG_DEBUG, "move file, src:%s, dst:%s" % (src, dst));
    
    # UUID 
    logger.logging(MLogger.LOG_DEBUG, "uuid:%s" % (utilClass.makeUniqueID('H_', '_00')));
    
    # 날짜 관련 
    logger.logging(MLogger.LOG_DEBUG, "current date:%s" % (utilClass.getCurrentDate()));
    logger.logging(MLogger.LOG_DEBUG, "current time:%s" % (utilClass.getCurrentTime()));
    logger.logging(MLogger.LOG_DEBUG, "current millisecond time:%s" % (utilClass.getMillisecondTime()));
    logger.logging(MLogger.LOG_DEBUG, "current time from millisecond:%s" % (utilClass.getTimeFromMillisecond(utilClass.getMillisecondTime())));
    afterMode = 'H';
    afterVal = 2;
    # 가급적 아래 DiffDateString 으로 사용을 통일한다. 
    logger.logging(MLogger.LOG_DEBUG, "after time:%s(mode=%s, val=%d)" \
                   % (utilClass.getAfterTime(mode=afterMode, val=afterVal, bPlus=True), \
                      afterMode, afterVal));
    curTime = "20220301123212";
    timeOpt = "1";            
    timeVal = 3;
    logger.logging(MLogger.LOG_DEBUG, "diff time(before):%s(timeOpt=%s, timeVal=%d)" \
                   % (utilClass.DiffDateString(curTime=curTime, timeOpt=timeOpt, timeVal=timeVal, bAfter=False), \
                      timeOpt, timeVal));
    curTime="";
    logger.logging(MLogger.LOG_DEBUG, "diff time(after):%s(timeOpt=%s, timeVal=%d)" \
                   % (utilClass.DiffDateString(curTime=curTime, timeOpt=timeOpt, timeVal=timeVal, bAfter=True), \
                      timeOpt, timeVal));
    
    start_time = "20220310094712";
    end_time = "20220310094733";
    logger.logging(MLogger.LOG_DEBUG, "elapsed seconds:%d(start=%s, end=%s)" \
                   % (utilClass.getElapsedTime(startTime=start_time, endTime=end_time), \
                      start_time, end_time));
    
    timeStr = "20220301123212";
    timeFormat = "%Y-%m-%d %H:%M:%S";
    logger.logging(MLogger.LOG_DEBUG, "formatted time:%s(format=%s)" \
                   % (utilClass.getDateFormat(timeStr=timeStr, format=timeFormat), timeFormat));
    
    # RFilePath 및 볼륨 패스 
    logger.logging(MLogger.LOG_DEBUG, "rfilePath:%s" % (utilClass.getRFilePath()));
    volPath = utilClass.getVolumePath(global_val.CORPUS_DISK, 'VOL_02');
    logger.logging(MLogger.LOG_DEBUG, "volPath:%s" % (volPath));                   
    
    # random string 
    randomString = MUtility.randomString();
    logger.logging(MLogger.LOG_DEBUG, "randomString:%s" % (randomString));                   
    
    # 숫자 포맷 
    #num = 123456732131289.7673;
    num = 1024 * 1024;
    logger.logging(MLogger.LOG_DEBUG, "number_format : %s" % (utilClass.number_format(num=num, decimals=0)));
    logger.logging(MLogger.LOG_DEBUG, "size_format : %s" % (utilClass.size_format(size=num, decimals=0)));
    
    # Local IP 
    logger.logging(MLogger.LOG_DEBUG, "local IP: %s" % utilClass.getLocalIP());
    
    
    
    
    ############################

except MpowerException as ex:
    logger.exceptionLogging(MLogger.LOG_ERROR, ex);
else:
    pass
finally:
    if powerdb_con != None:
        powerdb_con.close();










print('finish');