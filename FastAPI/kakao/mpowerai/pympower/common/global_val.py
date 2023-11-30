from abc import *
import importlib
from pympower.hostname import HostName

# PHP의 global_val.php와 동일 
# 이 기반 클래스를 site_props내 global_val_{site} 클래스에서 override 한다. 
# PHP의 define과 다르게 if defined처럼 처리할 필요가 없다. 재지정되면 마지막 지정된 값을 사용한다. 
# 해당 변수값은 소스코드상에서 동적으로 변경이 가능하다. 변경되지 않도록 유의한다. 
#
# define.sha.php 도 이곳에 정의했다. 
# PHP의 전체 값을 모두 가져오지는 않았음. 따라서, 필요시 추가해야 한다. 

# 이곳에는 정의를 안하고, site_props에만 정의할 경우 
# 실제 코딩할때 intellisense가 적용되지 않아 코딩이 어려워진다. 
# 이를 회피하고자, 사용하지 않는 변수는 값을 None으로 할당한다. 
# 이 경우 defined 함수에서 값이 None인 경우 False를 반환하도록 하였다. 

class global_val(metaclass=ABCMeta):
    
    # DB 유형 
    MYSQL = 1;
    ORACLE = 2;
    MSSQL = 3;
    TIBERO = 4; 
    
    # WORK_TYPE
    BAC_DISK = 1; # 백업디스크.v10에는 백업 없음 
    WEB_DISK = 2; # 웹디스크
    CORPUS_DISK = 3; # 코퍼스 디스크 
    
    # __TARGET 관련 최대 127까지만 허용한다.
    TARGET_SYSTEM = 99; # 시스템
    TARGET_ORG = 31; # 조직
    TARGET_GROUP = 21; # 그룹
    TARGET_USER = 11; # 유저
    TARGET_GUEST = 16; # 게스트
    TARGET_PROJECT = 6; # 프로젝트 (club_info)
    TARGET_PROJECT_CLASS = 7;	# 프로젝트 클래스 (club_class)
    TARGET_IP = 5; # IP
    TARGET_FILE = 50;	# FILE : 현재 LOG_ADMIN_ACTION 에서 대상 구분 위해 사용됨
    TARGET_FOLDER = 51; # FOLDER : 현재 LOG_ADMIN_ACTION 에서 대상 구분 위해 사용됨
    
    
    # 업로드 상태 
    FO_CHECK =  1; # 동일명의 파일이 있는지 체크. 있으면 에러 코드 반환
    FO_SKIP_CURRENT =  2; # 현재 파일만 SKIP
    FO_SKIP_ALL =  3; # 모든 파일만 SKIP
    FO_OVERWRITE_CURRENT =  4; # 현재 파일만 덮어쓰기
    FO_OVERWRITE_ALL =  5; # 모든 파일 덮어쓰기
    FO_RENAME_CURRENT =  6; # 현재 파일만 이름변경
    FO_RENAME_ALL =  7; # 모든 파일 이름 변경
    FO_MOVE_NODE =  8; # 노드 이동
    FO_PROP_CHECK =  9; # 속성 체크
    FO_RETRY =  99; # 재시도
    
    # 권한 정의
    ACLB_WAIT = 0x00100000;
    ACLB_V = 0x00000001; # 10진수 1
    ACLB_R = 0x00000002; # 10진수 2
    ACLB_W = 0x00000004; # 10진수 4
    ACLB_D = 0x00000008; # 10진수 8
    # 기존 권한 정보
    ACLB_GENERIC_READ = ACLB_V | ACLB_R; # 10진수 3
    ACLB_GENERIC_WRITE = ACLB_V | ACLB_W; # 10진수 5
    ACLB_GENERIC_READWRITE = ACLB_V | ACLB_R | ACLB_W; # 10진수 7
    ACLB_GENERIC_ALL = ACLB_V | ACLB_R | ACLB_W | ACLB_D; # 10진수 15
    
    # 아이템 유형 정의 시작
    # 클라이언트에서 INT 형으로 처리하고 있기 때문에, 숫자로 처리해야 한다.
    ITEM_TYPE_NODE = '0'; # 폴더 
    ITEM_TYPE_FILE = '1'; # 파일
    ITEM_TYPE_PASSWORD_NODE = '2'; # 비밀번호 적용된 폴더
    ITEM_TYPE_FILESTREAM = '3'; # 파일스트림. 향후 개발 예정
    ITEM_TYPE_VER_FILE = '5'; # 버전 파일
    
    # 그룹권한 (USER_GROUP_RELATE_INFO.GROUP_RIGHT)
    GROUP_RIGHT_NORMAL =  0x00000001; #일반사용자
    GROUP_RIGHT_LEADER =  0x00000002; #부서장
    GROUP_RIGHT_ADMIN =  0x00000004;  #부서관리자

    # 관계 유형 (USER_GROUP_RELATE_INFO.RELATE_TYPE
    UGRI_MEMBER = 101; # 소속임(원소속)
    UGRI_ADD_MEMBER = 102; # 소속임(겸직)

    # GLOBAL_CONFIG 의 CFG_TYPE 값
    CFG_EXPIRED_FILE = 1; # 1=문서 보존연한 설정
    CFG_EXPIRED_UPLOAD_TEMP = 2; # 2=이어올리기 보관주기 설정
    CFG_EXPIRED_DELETED_FILE = 3; # 3=삭제 파일 보관 주기 설정
    CFG_EXPIRED_RECYCLE_BIN_FILE = 4; # 4=휴지통 파일 보관 주기 설정
    CFG_EXPIRED_EZISC_EXPORT_FILE = 5; # 5=EZis-C 반출 파일 보관 주기 설정
    CFG_EXPIRED_APRVL_FILE = 6; # 6=결재 첨부 파일 보관 주기 설정
    CFG_EXPIRED_LOG = 9; # 9=로그 보관 주기 설정

    CFG_EXPIRED_UPLOAD_DOWNLOAD_LOG = 11; # 11=업로그 & 다운로그 보관 주기 설정
    CFG_EXPIRED_USER_ACTION_LOG = 12; # 12=사용자 행위 보관 주기 설정
    CFG_EXPIRED_PC_VIOLATION_LOG = 13; # 13=보안 위반 내역 보관 주기 설정


    # SCHEDULE_DETAILS.SU_ELEM_TYPE
    ELEM_TYPE_FOLDER_NON_INCLUDE_CHILD = 1;    #폴더(하위 폴더 제외)
    ELEM_TYPE_FOLDER_INCLUDE_CHILD = 2;    #폴더(하위 폴더 포함)
    ELEM_TYPE_FILE = 3;    #파일
    ELEM_TYPE_INCLUDE_EXT = 4; #확장자 포함
    ELEM_TYPE_NON_INCLUDE_EXT = 5; #확장자 제외
    ELEM_TYPE_WATCH_FOLDER = 7;    #감시 폴더(실시간 파일 백업)
    ELEM_TYPE_WATCH_FILTER = 8;    #감시 필터(실시간 파일 백업)
    ELEM_TYPE_INCLUDE_KEYWORD = 9; #키워드(포함)
    ELEM_TYPE_NON_INCLUDE_KEYWORD = 0; #키워드(제외)

    #결재 클래스 타입
    APRVL_CLASS_TYPE_VC_MDF = 1; # 바이러스오탐정정요청
    APRVL_CLASS_TYPE_PI_MDF = 2; # 개인정보오탐정정요청
    APRVL_CLASS_TYPE_PI_DOWN = 3; # 개인정보다운로드요청
    APRVL_CLASS_TYPE_PI_DEL = 4; # 개인정보삭제연장요청
    APRVL_CLASS_TYPE_EXP = 5; # 반출요청
    APRVL_CLASS_TYPE_NET = 6; # 망간자료반출요청
    APRVL_CLASS_TYPE_CPCTY = 7; # 용량신청

    APRVL_ALINE_LEVEL_NORMAL = 0; # 일반 결재
    APRVL_ALINE_LEVEL_LATER = 1; # 후결

    #결재 상태 값. 
    APRVL_STATUS_DRAFT = 'DF'; # 기안
    APRVL_STATUS_CANCEL = 'CC'; # 회수
    APRVL_STATUS_REJECT = 'RJ'; # 반려
    APRVL_STATUS_REJECT_EXPIRED = 'RE'; # 반려 기간 만료
    APRVL_STATUS_APPROVAL = 'AR'; # 승인

    # 백신 엔진 관련 상수 설정
    VC_NOT_DEFINED = 0;
    SYMANTEC_ENDPOINT_PROTECTION_ENGINE = 1;
    SYMANTEC_ENDPOINT_PROTECTION_ENGINE8 = 2;
    
    # LOCK_MODE. (NODE)
    LOCK_MODE_USER = '1'; # 사용자에 의한 잠금
    LOCK_MODE_SYSTEM = '2'; # 시스템에 의한 잠금. 삭제 불가. 

    # LOCK_TYPE. (FILE)
    UNLOCK_FILE = 0;
    LOCK_FILE = 1; # 보호잠금. 사용자가 직접 잠금 처리한 경우
    LOCK_IO = 2; # I/O 잠금. M드라이브 또는 직접 편집을 목적으로 잠금 처리한 경우 

    # File Operation
    FO_CANCEL = 0;
    FO_COPY = 1;
    FO_MOVE = 2;
    FO_UPDATE_NODE_DEPENDENCY = 3;
    FO_LIST = 4;
    FO_CHECK_CONDITION = 5;
    FO_LOCK = 6;
    FO_UNLOCK = 7;
    FO_SEARCH = 8;

    # SHARE_FILE_INFO의 LFILE_ATTR 값 정의
    LFA_FILESTREAM = 0x00000001; # 파일 스트림 포함
    LFA_SOFTCAMP_DRM = 0x00000002; # 소프트캠프 DRM
    LFA_FASOO_DRM = 0x00000004; # 파수 DRM
    LFA_NASCA_DRM = 0x00000008; # NASCA DRM
    
    # NODE_TYPE
    NODE_ROOT = 9999;	# M드라이브 에서 SINGLE 드라이브 사용 시 논리적 노드.
    NODE_MY_ROOT = 1;	# 내 문서함
    NODE_MY_ROOT_NAME_KR = "내 폴더";
    NODE_MY_ROOT_NAME_EN = "My Folders";
    NODE_MY_FOLDER = 2;	# 내 문서함 하위 일반 폴더
    NODE_MY_RECV = 3;	# 수신함
    NODE_MY_RECV_NAME_KR = "수신함";
    NODE_MY_RECV_NAME_EN = "InBox";
    NODE_NPKI = 4;	# NPKI 폴더
    NODE_NPKI_NAME_KR = "NPKI";
    NODE_NPKI_NAME_EN = "NPKI";
    NODE_GPKI = 5;	# GPKI 폴더
    NODE_GPKI_NAME_KR = "GPKI";
    NODE_GPKI_NAME_EN = "GPKI";
    NODE_GUEST = 6;	# 게스트 폴더
    NODE_GUEST_NAME_KR = "GUEST";
    NODE_GUEST_NAME_EN = "GUEST";
    NODE_FORCED_IMPORT = 7;	# 강제 반입 폴더
    NODE_FORCED_IMPORT_NAME_KR = "강제반입";
    NODE_FORCED_IMPORT_NAME_EN = "Forced Import";
    NODE_APPROVAL = 15; # 결재 폴더
    NODE_APPROVAL_NAME_KR = "결재 폴더"; 
    NODE_APPROVAL_NAME_EN = "Approval Folder";
    NODE_RECYCLE_BIN = 99; # 휴지통 폴더
    NODE_RECYCLE_BIN_NAME_KR = "휴지통";
    NODE_RECYCLE_BIN_NAME_EN = "RecycleBin";
    NODE_WHOLE_ROOT = 101; # 전체 공유 ROOT
    NODE_WHOLE_ROOT_NAME_KR = "전체 공유";
    NODE_WHOLE_ROOT_NAME_EN = "Whole Sharing";
    NODE_WHOLE_EACH_ROOT = 102; # 전체 공유 개별 ROOT(조직과 동일)	
    NODE_WHOLE_FOLDER = 103; # 전체 공유 내 일반 폴더	
    NODE_GROUP_ROOT = 201;	# 그룹 공유 ROOT
    NODE_GROUP_ROOT_NAME_KR = "그룹 공유";	
    NODE_GROUP_ROOT_NAME_EN = "Group Sharing";	
    NODE_GROUP_EACH_ROOT = 202;	# 개별 그룹 굥유 ROOT(그룹과 동일)
    NODE_GROUP_FOLDER = 203;		# 그룹 공유 내 일반 폴더 
    NODE_PROJECT_ROOT = 301;		# 프로젝트 ROOT
    NODE_PROJECT_ROOT_NAME_KR = "프로젝트";
    NODE_PROJECT_ROOT_NAME_EN = "Project";
    NODE_PROJECT_EACH_ROOT = 302;		# 개별 프로젝트 ROOT
    NODE_PROJECT_FOLDER = 303;	# 프로젝트 내 일반 폴더
    NODE_SHARE_RECV = 1001;
    NODE_SHARE_RECV_NAME_KR = "공유받은 폴더";
    NODE_SHARE_RECV_NAME_EN = "Sharing Users";
    NODE_SHARE_RECV_SUB = 1002;
    NODE_SHARE_SEND = 1011;
    NODE_SHARE_SEND_NAME_KR = "공유해준 폴더";
    NODE_SHARE_SEND_NAME_EN = "Shared Folders";
    NODE_SHARE_LOCK_LIST = 1021;
    NODE_SHARE_LOCK_LIST_NAME_KR = "잠금파일 목록";
    NODE_SHARE_LOCK_LIST_NAME_EN = "Locked files";
    NODE_SHARE_FAVORITES = 1031;
    NODE_SHARE_FAVORITES_NAME_KR = "즐겨찾기 목록";
    NODE_SHARE_FAVORITES_NAME_EN = "Favorites List";
    NODE_SHARE_RECENT_UPLOAD = 1032;    
    NODE_SHARE_RECENT_UPLOAD_NAME_KR = "최근 사용 파일";
    NODE_SHARE_RECENT_UPLOAD_NAME_EN = "Recent Files";
    __NODE_SHARE_BOARD = 1041;
    NODE_SHARE_BOARD_NAME_KR = "게시판";
    NODE_SHARE_BOARD_NAME_EN = "Board";

    # 로그 설정     
    MPOWER_HOME = "/MOCOMSYS";
    MPOWER_LOG_PATH = MPOWER_HOME + "/app_logs/";
    MPOWER_LOGFILE_SIZE = 1024 * 1024 * 10;
    MPOWER_LOGFILE_IDX = 5;
    MPOWER_ERROR_LOGFILE_IDX = 3;
    
    # 인터페이스 유형 정의 
    APP_ADMIN = 					0x00000001;	# 관리자
    APP_WEB = 						0x00000002;	# 보안파일서버 웹
    APP_WEB_UPDOWNLOADER = 			0x00000004;	# 웹에서 설치형 프로그램을 통해 올리기/내려받기 함.
    APP_CS = 						0x00000008;	# 보안파일서버 접속기
    APP_MDRIVE = 					0x00000010;	# M드라이브
    APP_MOBILE = 					0x00000020;	# 보안파일서버 모바일
    APP_GUEST = 					0x00000040;	# 보안파일서버 GUEST
    APP_FILELINK = 					0x00000080;	# 보안파일서버 URL 링크
    APP_LINKMAIL = 					0x00000100;	# 보안파일서버 메일 링크
    APP_BATCH = 					0x00000200;	# 배치
    APP_EZISC =  					0x00000400;	# EZis-C
    APP_EZISV =  					0x00000800;	# EZis-V
    APP_INTF =  					0x00001000;	# 인터페이스 연동
    APP_FORCED_IMPORT =  			0x00002000;	# 강제반입
    APP_FTP =  			            0x00004000;	# FTP
    APP_EXPORT =  			        0x00008000;	# 반출

    APP_ADMIN_NAME = 				"admin";
    APP_WEB_NAME = 					"web";
    APP_WEB_UPDOWNLOADER_NAME = 	"updownloader";
    APP_CS_NAME = 					"cs";
    APP_MDRIVE_NAME = 				"mdrive";
    APP_MOBILE_NAME = 				"mobile";
    APP_BATCH_NAME = 				"batch";
    APP_EZISC_NAME =  				"ezisc";	# EZis-C
    APP_EZISV_NAME =  				"ezisv";	# EZis-V
    APP_INTF_NAME =  				"interface";	# 인터페이스 연동
    APP_FORCED_IMPORT_NAME =        "forceimport"; # 강제반입
    APP_FTP_NAME =                  "ftp"; # FTP
    APP_EXPORT_NAME =               "export"; #반출

    APP_ADMIN_NAME_KR = 		    "관리자";
    APP_WEB_NAME_KR = 				"웹";
    APP_WEB_UPDOWNLOADER_NAME_KR =  "업다운로더";
    APP_CS_NAME_KR = 				"접속기";
    APP_MDRIVE_NAME_KR = 			"M드라이브";
    APP_MOBILE_NAME_KR = 			"모바일";
    APP_BATCH_NAME_KR = 			"배치";
    APP_EZISC_NAME_KR =  			"로컬저장제어";	# EZis-C
    APP_EZISV_NAME_KR =  			"가상저장제어";	# EZis-V
    APP_INTF_NAME_KR =  			"인터페이스";	# 인터페이스 연동

    APP_ADMIN_NAME_EN = 		    "Admin";
    APP_WEB_NAME_EN = 				"Web";
    APP_WEB_UPDOWNLOADER_NAME_EN =  "UpDownloader";
    APP_CS_NAME_EN = 				"Client";
    APP_MDRIVE_NAME_EN = 			"MDrive";
    APP_MOBILE_NAME_EN = 			"Mobile";
    APP_BATCH_NAME_EN = 			"Batch";
    APP_EZISC_NAME_EN =  			"EZisC";	# EZis-C
    APP_EZISV_NAME_EN =  			"EZisV";	# EZis-V
    APP_INTF_NAME_EN =  			"Interface";	# 인터페이스 연동
    
    
    DB_KIND = None;
    USE_AI = None;

    PASSWORD_ENC_MODE =             "sha256";

    # 임시 파일 경로 관련 설정
    MPOWER_TEMP_DIR = '/MP_VROOT/temp'

	# 전처리 관련 설정
    FASTTEXT_MODEL_PATH = MPOWER_HOME + "/nlp_model/fasttext/lid.176.ftz";
    TFHUB_HANDLE_PREPROCESS = MPOWER_HOME + "/nlp_model/tfhub/tensorflow/bert_multi_cased_preprocess_3";
    TFHUB_HANDLE_ENCODER = MPOWER_HOME + "/nlp_model/tfhub/tensorflow/bert_multi_cased_L-12_H-768_A-12_4";
    CP_BOS_PREDICTION = MPOWER_HOME + "/nlp_model/mocomsys/wikicut1/ko_headcut-1.h5";
    CP_EOS_PREDICTION = MPOWER_HOME + "/nlp_model/mocomsys/wikicut1/ko_tailcut-1.h5";
    EOS_MARKS = [ ".", "!", "?", "。", "！", "？" ]

    # 데이터 셋 관련 설정
    CORPUS_DIR = MPOWER_HOME + '/nlp_corpus'

    # MocoCrypto
    MOCOCRYPTO_DLL = MPOWER_HOME + '/util74/lib/MocoCrypto.so'

    def __init__(self) -> None:
        pass
    
    @classmethod
    def defined(cls, name):
        if hasattr(cls, name):
            val = getattr(cls, name);
            if (val != None):
                return True;            
        return False;

    @staticmethod
    # -> global_val 로 typing 하면 에러가 발생. 
    # 3.10 부터는 정상적으로 처리된다고 하기는 함. 현재는 "" 로 묶어 준다. 
    def load_global_val() -> "global_val":
        module_name = "pympower.site_props.global_val_%s" % (HostName.GLOBAL_CONFIG_NAME);
        module = importlib.import_module(name=module_name, package=None);
        return module.global_val_site;

