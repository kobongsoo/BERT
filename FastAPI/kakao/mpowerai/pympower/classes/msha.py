from pympower.common.session import MSESSION
from pympower.common.statuscode import StatusCode
from pympower.common.global_val import global_val
from pympower.classes.mbase import *
global_val = global_val.load_global_val();

class MSha(MBase):
    
    def __init__(self, powerdb_con:MpowerDB2=None):
        super().__init__(powerdb_con);
        
    def close(self):
        pass
    
    def getFullPath(self, 
                    itemType:str, itemId:str, workdb_con:MpowerDB2 = None):
        if (workdb_con == None):
            workdb_con = self.powerdb_con;
        query = '';
        if (itemType == global_val.ITEM_TYPE_FILE):
            query	= """SELECT sha_getFileFullPath(%s) as FULL_PATH """;
        else:
            query	= """SELECT sha_getNodeFullPath(%s) as FULL_PATH """;
        query += workdb_con.getDummyFrom();
        
        stmt = None;
        try:
            stmt = workdb_con.createStatement();
            workdb_con.execute(stmt=stmt, query=query, args=(itemId));
            rs = workdb_con.fetchNext(stmt);
            if (rs != None):
                return rs['FULL_PATH'];
            else:
                raise MpowerException(
                        'Item not found. type:%s, id:%s' % (itemType, itemId),
						StatusCode.SC_OBJECT_NOT_FOUND.value, 
						workdb_con.getDBIndex(),
                        StatusCode.SC_OBJECT_NOT_FOUND.name);   
        except MpowerException as ex:
            raise ex;  
        finally:
            if stmt:
                workdb_con.closeStmt(stmt);
        return '';                
            
    def isSystemNode(self, nodeArr:list):
        if False == ('NODE_TYPE' in nodeArr):
            return False;
        
        if (nodeArr['NODE_TYPE'] in 
            (global_val.NODE_MY_ROOT, 
			 global_val.NODE_MY_RECV, 
			 global_val.NODE_NPKI, 
			 global_val.NODE_GPKI, 
			 global_val.NODE_GUEST, 
			 global_val.NODE_APPROVAL, 
			 global_val.NODE_FORCED_IMPORT, 
			 global_val.NODE_RECYCLE_BIN, 
			 global_val.NODE_WHOLE_ROOT, 
			 global_val.NODE_WHOLE_EACH_ROOT, 
			 global_val.NODE_GROUP_ROOT, 
			 global_val.NODE_GROUP_EACH_ROOT, 
			 global_val.NODE_PROJECT_ROOT, 
			 global_val.NODE_PROJECT_EACH_ROOT, 
			 global_val.NODE_SHARE_RECV, 
			 global_val.NODE_SHARE_RECV_SUB, 
			 global_val.NODE_SHARE_SEND, 
			 global_val.NODE_SHARE_LOCK_LIST, 
			 global_val.NODE_SHARE_FAVORITES, 
	         global_val.NODE_SHARE_BOARD, 
		     global_val.NODE_SHARE_RECENT_UPLOAD)):
            return True;
        return False;
    
    def GetACLInfo(self, nodeId:str, userId:str, referId:str, ownerId:str, 
			        nodeType:int = 0, workdb_con:MpowerDB2 = None):
        
        pass
                   