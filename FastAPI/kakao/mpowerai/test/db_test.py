###################################################
# DB 처리 예제 프로그램 
###################################################

import importlib
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

print('start');
powerdb_con = MpowerDB2();
stmt = None;
shaClass = None;
logger = None;
try:
    
    logger = MLogger(appName=MSESSION.get("lol_appName"), userId=MSESSION.get("lol_ids81"));
    logger.setDebug(True);
    logger.logging(MLogger.LOG_DEBUG, "start app");
    
    powerdb_con.connectWithIndex();
    stmt = powerdb_con.createStatement();
    
    userId = 'skchoi';
    dbIdx = 0;
    # SQL 문은 특수문자를 사용하기 위해 """ {SQL} """ 의 셋따옴표를 사용한다. 
    # bind는 %s로 한다. 문자열이나 숫자 처리는 내부적으로 전달되는 변수에 따라서 알아서 처리한다. 
    # 유의할 사항은 문자듯, 숫자든 무조건 %s이다. 즉, %s가 문자열을 의미하는 것이 아닌 바인드 변수를 의미한다. 
    query = """SELECT * FROM USER_INFO WHERE USER_ID = %s AND DB_IDX = %s""";
    powerdb_con.execute(stmt, query, (userId, dbIdx));
    
    idx = 1;
    while (True):
        rs = powerdb_con.fetchNext(stmt);
        if (rs == None):
            break;
        logger.logging(MLogger.LOG_DEBUG, str(idx) + ':\n', powerdb_con.getDBIndex(), rs);
        idx += 1;
    
    #rs = powerdb_con.fetchAll(stmt);
    #print(rs);
    
    shaClass = MClassFactory.getSha(powerdb_con);
    shaClass.setLogger(logger=logger);
    
    # /내 폴더/nlp_sample/powerpnt/이중화 설계.ppt
    fullPath = shaClass.getFullPath(global_val.ITEM_TYPE_FILE, 'SF_b13f1dfd988311286fb8161b7de348a9_00');
    logger.logging(MLogger.LOG_DEBUG, "fullPath: %s" % (fullPath), powerdb_con.getDBIndex());
    
except MpowerException as ex:
    logger.exceptionLogging(MLogger.LOG_ERROR, ex);
else:    
    pass
finally:
    if powerdb_con != None:
        if stmt != None:
            powerdb_con.closeStmt(stmt);
        powerdb_con.close();    
    print("finished.");

