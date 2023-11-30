
###################################################
# PHP 연동 및 AI 관련 예제 프로그램 
###################################################

import json
import subprocess
import sys
from os import path
# 모듈 import를 위해 MPOWER_AI_HOME 경로를 설정한다. 
# 본 프로그램은 MPOWER_AI_HOME/test에 위치하므로, 상위 디렉토리를 설정한다. 
MPOWER_AI_HOME=path.dirname(path.dirname(path.abspath(__file__)));
sys.path.append(MPOWER_AI_HOME);

from pympower.common.session import MSESSION
from pympower.common.statuscode import MMessage, StatusCode
from pympower.common.global_val import global_val
from pympower.hostname import HostName
HostName.setMPOWER_AI_HOME(MPOWER_AI_HOME);
# MpowerScript가 기본 경로(/MOCOMSYS/MpowerScript)에 설치되지 않은 경우 
# HostName.setMPOWER_SCRIPT_HOME룰 통해 해당 경로를 설정해야 한다. 
from pympower.classes.mbase import *
global_val = global_val.load_global_val();

MSESSION.set('lol_ids81', 'SYSTEM');
MSESSION.set('lol_ids81_name', 'SYSTEM');
MSESSION.set('lol_dbIdx', 0);
MSESSION.set('lol_orgId', '');
MSESSION.set('lol_appType', global_val.APP_BATCH);
MSESSION.set('lol_appName', os.path.splitext(os.path.basename(__file__))[0]);
MSESSION.set("log_path", path.dirname(path.abspath(__file__)) + "/logs");
MSESSION.set('use_console_log', True);


logger = None;
try:
    logger = MLogger(appName=MSESSION.get("lol_appName"), userId=MSESSION.get("lol_ids81"));
    logger.setDebug(True);
    logger.logging(MLogger.LOG_DEBUG, "start app");
    
    utilClass = MClassFactory.getUtility();
    utilClass.setLogger(logger);
    cryptClass = MClassFactory.getMCrypt();
    cryptClass.setLogger(logger);
    aiClass = MClassFactory.getShaAI();
    aiClass.setLogger(logger);
    
    # 테스트 결과를 저장할 디렉토리 
    resultPath = path.dirname(path.abspath(__file__)) + "/result";
    utilClass.deleteAllDirectory(resultPath);
    utilClass.createAllDirectory(resultPath);
    
    
    srcPath = "/data4/MP_VROOT/SHARE/005/000/008/F_45ffc0d1028e248d64b337e51dd28573.SMF";
    tgtPath = resultPath + "/removed.ppt";
    encMode = 3;
    zipMode = 0;
    MRK = "8133e1a0a0c2c59af818cc25ae45dc4c";
    
    if os.path.exists(tgtPath):
        os.remove(tgtPath);
    
    # 복호화를 수행한다. 
    cryptClass.mpowerDecrypt(srcPath=srcPath, tgtPath=tgtPath, encMode=encMode, zipMode=zipMode, MRK=MRK);
    logger.logging(MLogger.LOG_DEBUG, "decrypted. src:%s, tgt:%s" % (srcPath, tgtPath));
    
    # Synap File Format을 확인한다. 
    fmt_id, fmt_name = aiClass.detectFileFormat(tgtPath);
    logger.logging(MLogger.LOG_INFO, 
                   "format_id:%d, format_name:%s" % (fmt_id, fmt_name), -1);
    
    # 텍스트를 추출한다. 
    rawPath = tgtPath + '.raw';
    if os.path.exists(rawPath):
        os.remove(rawPath);
    isMultiple, resultDir, corpusList = aiClass.extract(srcPath=tgtPath, tgtPath=rawPath, checkMultiple=False);
    logger.logging(MLogger.LOG_DEBUG, 
                   "extracted. src:%s, tgt:%s, isMultiple:%s, multiDir:%s " 
                   % (tgtPath, rawPath, isMultiple, resultDir));
    
    # 텍스트를 암호화 한다. 
    encPath = tgtPath + '.enc';
    if os.path.exists(encPath):
        os.remove(encPath);
    cryptClass.mpowerEncrypt(srcPath=rawPath, tgtPath=encPath, encMode=encMode, zipMode=zipMode, MRK=MRK);
    logger.logging(MLogger.LOG_DEBUG, "encrypted. src:%s, tgt:%s" % (rawPath, encPath));
    
    # 텍스트를 복호화 한다. 
    decPath = tgtPath + '.dec';
    if os.path.exists(decPath):
        os.remove(decPath);
    cryptClass.mpowerDecrypt(srcPath=encPath, tgtPath=decPath, encMode=encMode, zipMode=zipMode, MRK=MRK);
    logger.logging(MLogger.LOG_DEBUG, "decrypted. src:%s, tgt:%s" % (encPath, decPath));
    
    # 압축 파일을 추출한다. 
    srcPath = "/MOCOMSYS/nlp_sample/compress/compress_folder_sample.zip";
    rawPath = resultPath + "/compress_folder_sampl.zip.raw";
    if os.path.exists(rawPath):
        os.remove(rawPath);
    isMultiple, resultDir, corpusList = aiClass.extract(srcPath=srcPath, tgtPath=rawPath);
    logger.logging(MLogger.LOG_DEBUG, 
                   "compress file . src:%s, tgt:%s, isMultiple:%s, multiDir:%s " 
                   % (srcPath, rawPath, isMultiple, resultDir));
    if isMultiple:
        corpusListStr = json.dumps(corpusList, indent=4, ensure_ascii=False);
        logger.logging(MLogger.LOG_DEBUG, "corpus list\n%s" % (corpusListStr));
    
    
    # 추가 : 멀티플 유형인지 확인 
    bMultiple = aiClass.isMultiFile(path=rawPath)
    logger.logging(MLogger.LOG_DEBUG, "isMultiple? path:%s, result:%s" % (rawPath, bMultiple));
    
except MpowerException as ex:
    logger.exceptionLogging(MLogger.LOG_ERROR, ex);
finally:
    pass     
