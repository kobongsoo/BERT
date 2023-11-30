
from pympower.common.global_val import *
# 기본값은 global_val_basic에 정의되어 있고, 
# 별도의 값을 사용해야 하는 경우 이곳에 정의한다. 
# PHP처럼 HostName.GLOBAL_CONFIG_NAME을 기반으로 자동 로드되는 기능은 찾지 못하여 
# 
class global_val_site(global_val):
    # 추가로 정의해야 할 사항을 이곳에 정의한ㄷ. 
    
    DB_KIND = global_val.MYSQL;

    PASSWORD_ENC_MODE = "md5";

    MPOWER_TEMP_DIR = '/MOCOMSYS/temp'

    USE_AI = {
        "corpus": {
            "uncompressDepth": 9999, # 0은 사용안함. 9999는 무제한 
            "extType": "exclude", # __USE_CONTENTS_INDEXING의 extType 정책 참조
            "limitSize": 0, # __USE_CONTENTS_INDEXING의 limitSize 정책 참조
            "encMode": 0, # 코퍼스 파일에 대한 암호화 모드 
            "loggingTarget": ['E', 'F'] # 로깅을 수행할 CRPS_STATUS 상태값
        }, 
        # 자연어 본문 인덱싱
        "index": {
        }, 
        # 자연어 본문 검색  
        "search": {
        },
        # 자연어 문서 분류  
        "class": {
        }, 
        # 자연어 문서 요약  
        "summary": {
        }, 
    };
    
    def __init__(self) -> None:
        super().__init__();
    
    
    