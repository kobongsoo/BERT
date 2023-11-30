class HostName():
    HOST_NAME = '_00';
    
    # njhs
    # tuple로 설정하여 변경할 수 없도록 한다. 
    # 내부 dict 끝에는 콤마를 추가해야 index로 접근이 가능하다. 
    DB_LIST_INFO = (
        {"DB_NAME": "Mpower10U", "ADDR": "127.0.0.1", "PORT": 3306, "UID": "Mpower10U", "PWD": "manager@.!"},  
        );
    # site 구분자 
    GLOBAL_CONFIG_NAME = 'gpu';
    
    # 설치 위치 
    MPOWER_HOME = '/MOCOMSYS';
    MPOWER_AI_HOME = '/MOCOMSYS/MpowerAI_v10';
    MPOWER_SCRIPT_HOME = '/MOCOMSYS/MpowerScript';

    @staticmethod
    def setHOST_NAME(hostName:str):
        HostName.HOST_NAME = hostName;
        
    @staticmethod
    def setDB_LIST_INFO(dbInfo:dict):
        HostName.DB_LIST_INFO = dbInfo;
        
    @staticmethod
    def setGLOBAL_CONFIG_NAME(confName:str):
        HostName.GLOBAL_CONFIG_NAME = confName;
        
    @staticmethod
    def setMPOWER_HOME(homdDir:str):
        HostName.MPOWER_HOME = homdDir;

    @staticmethod
    def setMPOWER_AI_HOME(aiDir:str):
        HostName.MPOWER_AI_HOME = aiDir;
        
    @staticmethod
    def setMPOWER_SCRIPT_HOME(scriptHome:str):
        HostName.MPOWER_SCRIPT_HOME = scriptHome;

