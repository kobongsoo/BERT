from enum import Enum

class StatusCode(Enum):
    # 클라이언트에서 사용하는 StatusCode를 PHP로 포팅함. 
    # C/S 어플리케이션의 경우 기존에 숫자로 된 값을 반환하기 때문에, 
    # 어떤 에러인지 소스코드 상으로는 구별하기 어려웠음. 

    RESULT_SUCCESS = 				0;	# 성공
    RESULT_CONTINUE = 				10;	# 다음 작업으로 이동
    RESULT_STOP = 					11;	# 현재 작업 중지
    RESULT_RETRY = 					12;	# 현재 작업 재 시도
    RESULT_SUCCESSFUL = 			200; # 200 OK

    #############################/
    # 1 - 100
    # PHP Extension에서의 오류 코드 시작
    #############################/

    #############################/
    # *** 100 - 199 ***
    # 시스템 레벨에서 사용할 것임. 일단 사용하지 말것
    #############################/

    #############################/
    # *** 200 - 299 ***
    # 로그인 관련 코드 정의
    #############################/
    #SC_LOGIN_OVER_SESSION = 		201;	# 사용자 세션 초과
    SC_LOGIN_NOT_FOUND_UID = 		202;	# 존재하지 않는 계정
    SC_LOGIN_WRONG_PWD = 			203;	# 암호 오류
    SC_LOGIN_EXPIRED_UID = 			204;	# 계정 사용기간 초과
    SC_LOGIN_PAUSED_UID = 			205;	# 계정 일시 정지
    SC_LOGIN_WRONG_VERSION = 		206;	# 버젼 불일치
    #SC_LOGIN_EXCEED_SLOT = 		207;	# 슬롯(서버 총세션) 초과
    SC_LOGIN_MAINTAIN_SYS = 		208;	# 서버 점검
    SC_LOGIN_EXCEED_LICENSE = 		209;	# 라이선스 초과
    SC_LOGIN_EXPIRED_PWD = 			210;	# 비밀번호 사용기간 초과
    SC_LOGIN_LOCK_UID = 			211;	# 계정 잠김(암호 5회이상 오류)
    SC_LOGIN_EXIT_MPOWER = 			212;	# 신한생명용. 해당 값이 오면 메시지를 띄우지 않고 프로그램을 종료한다.

    # SKCHOI. 2016.05.23 Java쪽에서 사용하기 위해 추가함.
    SC_ERR_USER_AUTH =  			213;	# 사용자 인증 오류
    SC_ERR_SERVICE_NOT_INITIALIZED =214;	# 서비스가 초기화되지 않음
    SC_ERR_INVALID_LICENSE =  		215;	# 잘못된 라이선스 파일
    SC_LOGIN_LOCK_DURATION =  		216;	# 계정 잠김(기간 잠금)
    SC_BUILDNO_NOT_FOUND = 			217;	# 빌드 정보 누락
    SC_LOGIN_CLOSED_UID =  			218;	# 폐쇄된 계정
    SC_NOT_ALLOWED_IP =  			219;	# 접근 제한된 IP 
    SC_NOT_ALLOWED_MAC =  			220;	# 접근 제한된 MAC
    SC_CONFIG_NOT_FOUND =  			221;	# 정책 조회 실패
    SC_NOT_ALLOWED_TIME =  			222;	# 접근 제한된 시간
    SC_INVALID_BUILDNO = 			223;	# 사용할 수 없는 빌드 번호
    SC_NOT_ALLOWED_SERVICE = 		224;	# 사용불가 서비스
    SC_DUP_LOGIN_EXIST = 		    225;	# 중복 로그인 존재

    #############################/
    # *** 300 - 399 ***
    # 서버 에러 메시지 정의
    #############################/
    SC_FOUND_SAME_HASH = 			300;	# 해쉬 파일 존재함(send once)
    SC_SKIP_OVER_FILE = 			301;	# 스킵파일(incremental)
    SC_NOT_FOUND_FILE = 			302;	# 해당 파일 없음
    SC_NOT_OPEN_FILE = 				303;	# 파일 열기 오류
    SC_NOT_SEEK_FILE = 				304;	# 파일포인터 이동 오류
    SC_NOT_READ_FILE = 				305;	# 파일 읽기 오류
    SC_NOT_WRITE_FILE = 			306;	# 파일 쓰기 오류
    SC_NOT_CLOSE_FILE = 			307;	# 파일 닫기 오류
    SC_NOT_SAME_FSIZE = 			308;	# 보낸 크기 <> 받은 크기(전송 크기 오류)
    SC_EXCEED_SESSION = 			309;	# 세션 초과
    SC_OVER_VOL_SIZE = 				310;	# 시스템 볼륨 용량 초과(S)
    SC_OVER_USER_SIZE = 			311;	# 사용자 할당 용량 초과(S)
    SC_INVALID_SESSION = 			312;	# 불법 세션(서버 로그인 세션 없음)
    SC_FOUND_SAME_DIR = 			313;	# 동일 폴더 존재함
    SC_FOUND_SAME_FILE = 			314;	# 동일 파일 존재함
    SC_NOT_FOUND_DIR = 				315;	# 노드 없음
    SC_OVER_FIELD_SIZE = 			316;	# DB 필드 길이 초과
    SC_INVALID_XML_DATA = 			317;	# XML 데이타 오류
    SC_FOUND_SAME_ACL = 			318;	# 동일 ACL 존재함
    SC_FOUND_SAME_PUB = 			319;	# 동일 PUB 존재함
    SC_FOUND_SAME_SUB = 			320;	# 동일 SUB 존재함
    SC_FOUND_SUB_DIR = 				321;	# 하위 폴더에 존재함(대상 폴더가 원본 폴더의 하위 폴더입니다)
    SC_OVER_DISK_SIZE = 			322;	# 시스템 디스크 용량 초과(S)
    SC_AUTHORITY_ERR = 				323;	# 업로드 권한이 없습니다.
    SC_FOUND_VIRUS = 				324;	# 바이러스 발견(치료불가)
    SC_CHANGE_FILE = 				325;	# 전송중 파일 변경 오류
    SC_FOUND_LOCK_FILE = 			326;
    SC_FOUND_LOCK_FILE_MYSELY = 	327;	# 잠금 파일 발견(자신이 잠금)
    SC_FOUND_LOCK_FILE_OTHER = 		328;	# 잠금 파일 발견(타인이 잠금)
    SC_FOUND_MANUAL_LOCK = 			329;	# 잠금 해제 실패(수동잠금모드(1)을 자동잠금모드(2)으로 풀려고할때)
    SC_DO_NOT_USE_TIME = 			330;	# 사용할 수 없는 시간입니다.
    SC_FAIL_OPEN_LOCK_FILE = 		331;	# 파일 락 열기 오류
    SC_FAIL_LOCK_FILE = 			332;	# 파일 락 오류
    SC_FAIL_SQL_QUERY = 			333;	# SQL 쿼리 오류
    SC_PERMISSION_FAIL = 			334;	# 기업은행용. 파일 업로드 권한 없음.
    SC_BLOCK_MISSING = 				336;    # 모든 블록이 업데이트 되지 않음. (고속 파일 전송)
    SC_NOT_SCAN_VIRUS = 			337;    # 바이러스 미검사
    SC_NOT_CRC_FILE =  				338;    # CRC오류 


    # skchoi. 2014.11.03 NetDrive
    SC_ERR_UNSUPPORTED_ENC_MODE = 	341;	# 지원하지 않는 암호화 모드
    SC_ERR_CREATE_CRYPTO_KEY = 		342;	# 암호화 키 생성 오류
    SC_ERR_INITIALIZE_CRYPTO = 		343;	# 암호화 모듈 초기화 오류
    SC_ERR_DECRYPT_DATA = 			344;	# 복호화 오류
    SC_ERR_ENCRYPT_DATA = 			345;	# 암호화 오류
    SC_TIMEOUT = 					346;	# 시간 초과
    SC_ERR_RECV_DATA = 				347;	# 데이터 수신 오류
    SC_ERROR_PERSNAL_YN = 			348;		
    SC_ERR_COMPRESS = 				350;	# 압축 실패
    SC_ERR_UNCOMPRESS = 			351;	# 압축 해제 실패
    SC_NO_DATA = 					352;	# 데이터 없음
    SC_INVALID_METHOD = 			353;	# 잘못된 메소드
    SC_ERR_ZIPFILE = 				354;	# 압축파일은 실패
    SC_ERR_DB_CONN = 				355;	# DB 연결 오류 
    SC_DIR_NOT_CHANGED = 			356;	# 디렉토리 변경 오류 
    SC_ERR_CREATE_DIR = 			357;	# 디렉토리 생성 실패
    SC_ERR_SEND_HTTP =  			358;	# HTTP 전송 실패 
    SC_ERR_COPY_FILE =  			359;	# 파일 복사 에러 
    SC_AUTH_READ_ERR =  			360;	# 읽기 권한 없음. 
    SC_AUTH_WRITE_ERR =  			361;	# 쓰기 권한 없음.
    SC_AUTH_DELETE_ERR =  			362;	# 삭제 권한 없음.
    SC_AUTH_ADMIN_ERR =  			363;	# 관리자 권한 없음.
    SC_DELETE_FILE_ERR =  			364;	# 파일 삭제 오류
    SC_NOT_OPEN_STREAM =  			365;	# 스트림 열기 실패 
    SC_NOT_FOUND_VOL =  			366;	# 볼륨 찾기 실패 
    SC_ERR_META_INFO =  			367;	# 메타 정보 처리 실패
    SC_ERR_RAPID_INDEX_INFO =  		368;	# 고속전송 인덱스 처리 실패
    SC_EXCEED_MAX_FILE_SIZE = 		369;	# 최대 파일크기 초과 
    SC_NOT_EXEC_COMMAND =  			370;	# 명령어 처리 실패
    SC_NOT_FOUND_ITEM =  			371;	# 아이템 찾기 실패
    SC_ERR_MOVE_FILE = 				372;	# 잘못된 파라미터
    SC_AUTH_SYSTEM_NODE_ERR =  		373;	# 시스템 폴더  편집, 삭제, 복사시 오류 
    SC_PASSWORD_NODE_FOUND = 		374;	# 비밀번호 폴더 존재
    SC_ORDERMARK_UNMATCH = 			375;	# ORDER MARK 오류
    SC_CONNECTION_CLOSE = 			376;	# 연결 종료
    SC_NOT_RENAME_ITEM = 			377;	# 이름 변경 오류 
    SC_NOT_ALLOW_CHAGE_VALUE =  	378;	# 값 변경 불가 오류 
    SC_AUTH_VIEW_ERR =  			379;	# 보기 권한 없음.

    #############################/
    # *** 400 - 599 ***
    # 클라이언트 에러 메시지 정의 (서버에 전송되는 코드임)
    #############################/
    CS_NOT_FOUND_FILE = 			401;	# 파일 찾기 오류
    CS_NOT_OPEN_FILE = 				402;	# 파일 열기 오류
    CS_NOT_READ_FILE = 				403;	# 파일 읽기 오류
    CS_NOT_WRITE_FILE = 			404;	# 파일 쓰기 오류
    CS_NOT_CLOSE_FILE = 			405;	# 파일 닫기 오류
    CS_NOT_SAME_FSIZE = 			406;	# 동일 파일 크기
    CS_CANCEL_WORK = 				407;	# 취소 버튼 클릭
    CS_SAME_FILE = 					408;	# 동일 파일
    CS_NOT_RENAME_FILE = 			409;	# 파일 이름 변경 오류
    CS_SYS_UNKNOWN_EXP_ERR = 		410;	# 클라이언트 Exception 오류
    CS_XML_UNKNOWN_EXP_ERR = 		411;	# XML Exception 오류
    CS_SQL_UNKNOWN_EXP_ERR = 		412;	# SQL Exception 오류
    CS_NOT_CREATE_DIR = 			413;	# 디렉토리 생성 실패. 추가
    CS_OVER_DISK_SIZE = 			414;	# 디스크 초과
    CS_SUB_FUNC_RETURN_ERR = 		415;	# 디스크 용량 얻기 실패
    CS_NOT_CRC_FILE = 				416;	# 전송중 파일 변경
    CS_NOT_SEEK_FILE = 				417;	# 파일포인터이동오류(C)
    CS_TURNOFF_PC = 				418;	# 컴퓨터 종료
    CS_FAIL_COMPRESS = 				419;	# 전송중 압축 오류(C)
    CS_NOT_RECV_MRK = 				420;	# 암호화 키(MRK)를 받지 못했습니다
    CS_LOCK_FILE_ALREADY = 			421;	# 다른 프로세스가 이미 올리고 있는 파일입니다.
    CS_NOT_OBTAIN_DIR_NODE = 		422;	# 디렉토리 조회 오류. 웹에서 사용 ???
    CS_FASSO_ERROR = 				423;	# 농협손해보험 파수 DRM 에러
    CS_NOT_CREATE_RESOURCE = 		424;	# 리소스 생성 실패
    CS_NO_MORE_ITEMS = 				425;	# 아이템이 더이상 없음.
    CS_NOT_WRITE_LOG = 				426;	# ForcedImpoter에서 로그 생성 시 사용
    CS_NOT_DELETE_FILE = 			427;	# ForcedImpoter에서 로그 생성 시 사용
    CS_ERR_PASSWORD_AUTH = 			428;	# 비밀번호 인증 실패 

    SC_NOT_FOUND_SESSION =          403;    #에러처리
    SC_CUSTOM_ERROR =               888;    #에러처리

    # 박규영. 2015.03.27 MpowerAutomation
    CS_TIMEOUT = 					446;	# 시간 초과

    # 클라이언트 바이러스 검사 에러 메시지 정의(바이러스 체이서)
    # 실제 사용되지 않으므로, 배제함.
    # CS_FOUND_VIRUS = 						450;	# 바이러스 발견(아무조치하지 않음)
    # CS_FOUND_VIRUS_CURE = 					451;	# 바이러스 발견(치료함)
    # CS_FOUND_VIRUS_MOVE = 					452;	# 알려진 바이러스 발견(치료불가-검역소 이동)
    # CS_FOUND_VIRUS_DELETE = 					453;	# 알려진 바이러스 발견(치료불가-삭제)
    # CS_FOUND_VIRUS_MODIFICATION_MOVE = 		454;	# 바이러스 발견(감염의심-검역소 이동)
    # CS_FOUND_VIRUS_MODIFICATION_DELETE = 	455;	# 바이러스 발견(감염의심-삭제)
    # CS_FOUND_VIRUS_UNKNOWN_MOVE = 			456;	# 바이러스 발견(감염의심-검역소 이동)
    # CS_FOUND_VIRUS_UNKNOWN_DELETE = 			457;	# 바이러스 발견(감염의심-삭제)
    # CS_FAIL_SCAN_VIRUS = 					458;	# 바이러스 검사 실패(???)

    # 킹스정보통신 개인정보 검출 솔루션 통합 에러 코드
    # 실제 사용되지 않으므로, 배제함.
    # CS_FOUND_PRIVACY_0 = 					460;	# 킹스 정보 통신 함수의 리턴 값을 CS_FOUND_PRIVACY_0 + x 로 사용.
    # CS_FOUND_PRIVACY_PRIVACY = 			460;	# 고객정보 있음
    # CS_FOUND_PRIVACY_KEYWORD = 			461;	# 키워드 있음
    # CS_FOUND_PRIVACY_NOTHING = 			462;	# 고객정보 및 키워드 없음 (Success)
    # CS_FOUND_PRIVACY_PRIVACY_AND_KEYWORD = 	463;	# 고객정보 및 키워드 있음
    # CS_FOUND_PRIVACY_ERROR = 				464;	# 나머지 에러 코드.
    # CS_FOUND_PRIVACY_NOT_INSTALLED = 		465;	# 킹스 정보 통신 개인 정보 검출 솔루션이 설치 되지 않음.

    # IBK SecuInfra 개인정보 검출 솔루션 에러 코드
    #CS_NOT_APPROVED_SECUINFRA =  			470;	# SecuInfra에서 전송 허용하지 않음.

    # 고속 전송 클라이언트
    CS_MISSING_BLOCK = 			    471;	# 고속 전송 데이터 블럭 누락
    CS_ERR_RAPID_INDEX_INFO = 	    472;	# 고속 전송 인덱스 처리 실패

    CS_DISCONNECT_SERVER = 		    500;	# 서버 연결 오류
    CS_UNKNOWN_HEADER = 			501;	# 알수 없는 헤더 오류
    CS_CANT_MAKE_HEADER = 		    502;	# 헤더 생성 오류
    CS_MISMATCH_HEADER = 		    503;	# 일치하지 않는 프로토콜
    CANT_READ_RESULT_CODE = 		504;	# 결과 값 읽기 오류
    CS_ADD_NODE_ERR = 			    505;	# 노드 추가 오류(C)
    CS_CANT_CREATE_SOCKET = 		506;	# 소켓 생성 오류(C)
    CS_CANT_CONNECT_SERVER = 	    507;	# 서버 접속 오류(C)
    CS_FILE_ALREADY_EXISTS = 	    508;	# 동일파일명 존재
														
    #############################/
    # *** 600 - 699 ***
    # 클라이언트 에러 메시지 정의 
    # 서버에서 사용할일 없음
    # 웹에서 사용  
    #############################/
    CC_FAIL_CREATE_ADM_SOCKET = 	600;	# 통합 서버(ADM) 소켓 생성을 실패하였습니다.
    CC_FAIL_CONNECT_ADM_SERVER = 	601;	# 통합 서버(ADM) 연결에 실패하였습니다.
    CC_FAIL_CREATE_NS_SOCKET = 	    602;	# 백업 서버(NS) 소켓 생성을 실패하였습니다.
    CC_FAIL_CONNECT_NS_SERVER = 	603;	# 백업 서버(NS) 연결에 실패하였습니다.
    CC_FAIL_SEND_PACKET = 		    604;	# 패킷 송신에 실패하였습니다.
    CC_FAIL_RECV_PACKET = 		    605;	# 패킷 수신에 실패하였습니다.
    CC_FAIL_MAKE_HEADER = 		    606;	# 헤더 생성 오류
    CC_FAIL_ADD_NODE = 			    607;	# 노드 추가 오류(C)
    CC_WRONG_ORDER_MARK = 		    608;	# 잘못된 패킷(Order Mark)입니다.
    CC_MISMATCH_COMMAND = 		    609;	# 프로토콜 명령어(Command)가 일치하지 않습니다.
    CC_DISCONNECTED_SERVER = 	    610;	# 서버와 연결이 끊어졌습니다.
    CC_FAIL_CONNECT_IIS_SERVER = 	611;	# 서버(HTTP) 연결에 실패하였습니다.
    CC_FAIL_DELETE_MDB = 			612;	# MDB 파일 삭제 실패
    CC_BAD_HTTP = 					613;	# 지원하지 않는 프로토콜 (Transfer-Encoding 또는 파일 크기가 아닌경우)
    CC_FAIL_CREATE_UPGRADE_INFO_XML = 614;  # UPGRADE_INFO.XML 생성 실패
    CC_FAIL_ENCODE_BASE64 = 		615;	# BASE64 인코딩 오류
    CC_FAIL_DECODE_BASE64 = 		616;	# BASE64 디코딩 오류

    CC_LIC_ERROR =                  820;    # 라이선스 오류 
    # 폴더 암호 설정
    CC_FAIL_FOLDER_INPUT_PWD =      650;    
    CC_FAIL_FOLDER_WRONG_PWD =      651;


    # 알수 없는 에러 정의 ---------------------------------------------------------------------------------
    SC_SYS_UNKNOWN_EXP_ERR = 		700;	# 시스템 알수 없는 에러
    SC_SYS_CONFIG_ERR = 			701;	# 시스템 설정 오류 
    SC_XML_UNKNOWN_EXP_ERR = 		800;	# XML 오류
    SC_SQL_UNKNOWN_EXP_ERR = 		900;	# SQL 오류
    SC_SUB_FUNC_RETURN_ERR = 		1000;	# 함수 리턴 오류
    #---------------------------------------------------------------------------------------------------


    #############################/
    # *** 1000 - 1999 ***
    # 클라이언트 에러 메시지 정의 (서버 전송)
    # 서버에서 사용할일 없음
    #############################/
    CS_RETRY_NETWORK_CONNECT = 	    1001;	# 재접속중(네트워크 장애)
    CS_PREPARE_TRANSFER = 		    1002;	# 준비중...
    CS_ALREADY_UPLOAD = 		    1003;	# 다른 프로세스가 이미 전송중인 파일입니다.
    CS_RESUME_UPLOAD = 			    1004;	# 이어올리기중...
    CS_EXCEPTION_UPLOAD = 		    1005;	# 전송중 예외 오류
    CS_DONE_TRANSFER = 			    1006;	# 전송 완료
    CS_HASH_OPNE_ERROR = 		    1007;	# 해시 파일 열기 오류(C)
    CS_HASH_PREPARE = 			    1008;	# 해시 비교 준비중(H)...
    CS_HASH_READ_ERROR = 		    1009;	# 해시 파일 읽기 오류(C)
    CS_END_COMPUTER = 			    1010;	# 컴퓨터 종료
    CS_UPLOADLIST_ERROR = 		    1011;	# 업로드 리스트 오류
    CS_DOWNLOADLIST_ERROR = 		1012;	# 다운로드 리스트 오류
    CS_DOWNLOAD_CREATE_FOLDER = 	1013;	# 폴더 생성
    CS_DOWNLOAD_OPENFILE = 		    1014;	# 읽기전용
    CS_DOWNLOAD_DIRECTEDIT = 	    1015;	# 직접편집
    CS_DOWNLOAD_SKIP = 			    1016;	# 동일 파일 스킵(C)
    CS_DISK_GETSIZE_ERROR = 		1017;	# 디스크 용량 얻기 실패(C)
    CS_DISK_SIZE_NOTENOUGH = 	    1018;	# 디스크 용량 부족(C)
    CS_DOWNLOAD_CONVERT_ERROR = 	1019;	# 파일 변환 오류(C)
    CS_WAIT_TRANSFER = 			    1020;	# 전송중...
    CS_DOWNLOAD_CONVERT_WAIT = 	    1021;	# 변환중...
    CS_DOWNLOAD_CONVERT_DONE = 	    1022;	# 변환 완료...
    CS_FIND_CONNECT_ERROR = 		1023;	# 연결된 실행파일을 찾는 중에 오류가 발생하였습니다.
    CS_SAVE_OPENFIE_ERROR = 		1024;	# 파일 열기 정보를 저장할 수 없습니다.
    CS_BACKUPLIST_ERROR = 		    1025;	# 백업리스트오류
    CS_CANCEL_TRANSFER = 		    1026;	# 전송 취소

    #############################/
    # *** 1200 - 1399 ***
    # 동기화 관련 코드 정의
    #############################/
    SC_SYNC_USER_NOT_EXISTS = 		1200;	# 동기화 사용자 ID가 존재하지 않습니다.
    SC_SYNC_USER_SAME_ID = 			1201;	# 동일한 동기화 사용자 ID가 이미 존재 합니다.
    SC_SYNC_NODE_NOT_EXISTS = 		1205;	# 동기화 폴더가 존재하지 않습니다.
    SC_MORE_ACTION_EXISTS = 		1210;	# 마지막 동기화 후 서버에 변경된 내용이 있습니다.

    #############################/
    # *** 2000 - 2999 ***
    # 결재 관련 코드 정의
    #############################/
    SC_APRVL_ALREADY_PROGRESS =  	2001;	# 이미 결재 진행중임


    #############################/
    # *** 4000 - 4499 ***
    # 서버 코드 정의 
    #############################/
    SC_OBJECT_NOT_FOUND = 			4001;	# 아이템 찾기 실패
    SC_INVALID_REQUEST = 			4002;   # 잘못된 요청
    SC_FAIL_CREATE_TEMP_FILE = 		4003;   # 임시 파일 생성 실패
    SC_OBJECT_EXISTS = 				4004;   # 오브젝트 존재
    SC_PARENT_OBJECT_NOT_FOUND = 	4005;   # 부모 아이템 찾기 실패
    SC_INVALID_SEEK_POINTER = 		4006;   # 파일 포인터 오류
    SC_PERSONAL_INFO_EXIST = 		4008;   # 개인정보 포함 파일
    SC_PERSONAL_INFO_CHECKING = 	4009;   # 개인정보 검색 중
    SC_NOT_FOUND_RFILE = 			4010;   # 원격 파일 찾기 실패
    SC_NOT_CREATE_DIR = 			4011;   # 디렉토리 생성 실패
    SC_NOT_CREATE_FILE = 			4012;   # 파일 생성 실패
    SC_NOT_CREATE_PROCESS = 		4013;   # 프로세스 생성 실패
    SC_NOT_CREATE_SHORTCUT = 		4014;   # 바로가기 생성 실패 
    SC_FILE_CHANGED = 				4015;   # 파일 변경됨
    SC_DIR_NOT_EMPTY = 				4016;   # 빈 디렉토리가 아님.
    SC_TARGET_OBJECT_NOT_FOUND = 	4018;   # 대상 아이템 없음.
    SC_TARGET_PARENT_OBJECT_NOT_FOUND =4019;# 대상 아이템의 부모 노드 없음
    SC_ERR_LONG_NAME = 				4020;   # 지원할 수 없는 긴 이름
    SC_MOVE_FOLDER_TO_DIFFERENT_DB =4021;   # 폴더 이동 오류(다른 영역)
    SC_SRC_TGT_DBIDX_UNMATCH = 		4023;   # 원본과 대상의 DB 인덱스 다름
    SC_NODE_MOVED = 				4024;   # 노드 이동 완료
    SC_FOUND_PASSWORD_FOLDER = 		4025;   # 암호 폴더 발견
    SC_NOT_DELETE_PASSWORD_DIR = 	4026;   # 암호 폴더 삭제 오류
    SC_NOT_MOVE_PASSWORD_DIR = 		4027;   # 암호 폴더 이동 오류
    SC_REJECT_LOGIN_COS_INIT_PASSWORD =4028;# 초기 패스워드로 로그인 오류
    SC_ERR_PUB_NOT_FOUND = 			4029;   # 공유 정보 찾기 실패
    SC_ERR_PUB_GROUP_TYPE = 		4030;   # 공유 유형 조회 실패
    SC_ERR_PREV_POLICY_NOT_FOUND = 	4031;   # 이전 정책을 찾을 수 없음. 관리자페이지에서 사용
    SC_POLICY_STILL_USED = 			4032;   # 정책이 사용중임.
    SC_ACTION_ID_NOT_FOUND = 		4033;   # 활동 ID 찾기 실패
    SC_NOT_IMPLEMENTED = 			4034;   # 구현되지 않음
    SC_ZERO_BYTE = 				    4035;   # 대상이 0바이트임

    SC_ERR_MOVE_PARENT_TO_CHILD_NODE =4041; # 부모노드를 자식노드로 이동 오류 
    SC_FOUND_SAME_PROJECT_NAME =  	4042;   # 동일 프로젝트 이름 존재 
    SC_FOUND_SAME_SHARE_NAME =  	4043;   # 동일 공유 이름 존재
    SC_ERR_MOVE_SAME_NODE =         4044;   # 같은 노드에  이동시 오류
    SC_JOB_ALREADY_FINISHED =  		4045;   # 이미 완료된 작업
    SC_JOB_IN_PROGRESS =  			4046;   # 진행중인 작업
    SC_ERR_GET_FILE_PROP = 			4051;	# 파일 속성 조회 실패
    SC_ERR_GET_NODE_PROP = 			4052;	# 노드 속성 조회 실패
    SC_FOUND_SAME_NODE_SHARE =  	4053;   # 동일 노드 공유 생성 오류

    SC_SQL_ERROR = 					4100;   # SQL 오류
    SC_DB_ERROR = 					4101;   # DB 오류
    SC_SQL_NO_APPLIED = 			4102;   # 적용된 데이터 없음
    SC_UNSUPPORTED_DB = 			4103;   # 지원하지 않는 데이터베이스 

    SC_VC_ENGINE_UNAVAILABLE =  	4110;	# 백신 엔진 오류 
    SC_INTERNAL_ERROR = 			4111;	# 서버 내부 오류 

    SC_ERR_MODIFY_SYSTEM_CONFIG =  	4121;   # 시스템에 의해 설정된 값은 변경할 수 없습니다.
    SC_FOUND_LOCK_NODE =  			4122;   # 잠금 노드 존재



    # 폴더 비밀번호 관련 추가
    SC_ERR_FOLDER_PWD_ALREADY_EXIST =4151;  # 폴더 패스워드가 기 존재함
    SC_ERR_FOLDER_PWD_NOT_FOUND =  	4152;   # 폴더 패스워드가 없음
    SC_ERR_FOLDER_PWD_NOT_MATCHED = 4153;   # 폴더 패스워드가 일치하지 않음

    # 본문검색 인덱싱 관련 추가. skchoi. 2021.04.19
    SC_ERR_NO_NODE_AVAILABLE =      4181;   # 본문검색 노드를 찾을 수 없음
    SC_ERR_CREATE_CI_INDEX =        4182;   # 본문검색 인덱싱 생성 에러
    SC_ERR_EXCLUDE_CI_FORMAT =      4183;   # 본문검색 인덱싱 대상이 아님
    SC_ERR_DELETE_CI_INDEX =        4184;   # 본문검색 인덱스 삭제 에러
    SC_ERR_SEARCH_CI_INDEX =        4185;   # 본문검색 인덱스 조회 에러

    SC_LDAP_CONNECT_ERROR =  		4300; # LDAP 연결 오류
    SC_ZIP_DOWNLOAD_TOTAL_LIMIT_SIZE =  4400; # 다중 파일 압축 다운로드  전체 사이즈 제한 초과 오류
    SC_ZIP_DOWNLOAD_FILE_LIMIT_SIZE =  	4401; # 다중 파일 압축 다운로드  파일 사이즈 제한 초과 오류
    SC_ERR_ZIP_DOWNLOAD_SIZE_LIMIT = 4402;  # 다중 파일 압축 다운로드  파일 사이즈 제한 초과 오류
    SC_USAGE_MAX_CHECK_EXCEED =  	4410; # 설정 용량  최대값 초과

    #############################/
    # *** 4500 - 4999 ***
    # 클라이언트 코드 정의
    #############################/
    CS_FAIL_LOAD_META_DAT = 		4501;	# 메타데이터 로드 실패(C)
    CS_FAIL_LOAD_VOL_SIZE = 		4502;   # 볼륨 크기 로드 실패(C)
    CS_ENCRYPT_INIT_ERROR = 		4503;   # 암호화 모듈 초기화 실패(C)
    CS_ENCRYPT_ERROR = 				4504;   # 암호화 오류(C)
    CS_DECRYPT_INIT_ERROR = 		4505;   # 복호화 모듈 초기화 실패(C)
    CS_DECRYPT_ERROR = 				4506;   # 복호화 오류(C)
    CS_OPEN_READONLY = 				4507;   # 읽기 전용으로 열기(C)
    CS_UNSUPPORTED_ZIP_MODE = 		4508;   # 지원하지 않는 압축 모드(C)
    CS_UNSUPPORTED_ENC_MODE = 		4509;   # 지원하지 않는 암호화 모드(C)
    CS_FAIL_INSERT_DEFERRED_UPLOAD = 4510;  # 지연 업로드 정보 생성 실패(C)
    CS_NOT_CREATE_FILE = 			4511;   # 파일 생성 오류(C)
    CS_SYSTEM_FOLDER = 				4512;   # 시스템 폴더(C)
    CS_ERR_DECODE_JSON = 			4513;   # JSON 디코딩 오류(C)
    CS_ERR_INVALID_HANDLE = 		4514;	# 잘못된 핸들(C)


    #############################/
    # *** 5000 - 5499 ***
    # 업/다운로드 리스트 메시지. 클라이언트에서만 사용
    #############################/


    #############################/
    # *** 6000 - 6999 ***
    # 신규 서버 코드
    #############################/
    # 허성   2017.12.08  공유 오류
    SC_AUTH_ACCESS = 				6000;   #해당 권한이 없습니다.
    SC_WRONG_ACCESS = 				6001;   #잘못된 접근
    SC_LINK_DELETE_INFO = 			6002;   #삭제된 링크 정보
    SC_LINK_EXCEED_DAY = 			6003;	#링크 설정 날짜 초과
    SC_LINK_EXCEED_DOWN = 			6004;	#링크 다운 횟수 초과
    SC_LINK_DELETE_ITEM_INFO = 		6005;	#삭제된 링크  아이이템 정보
    SC_LINK_INPUT_PW = 				6006;	#링크 패스워드 입력
    SC_LINK_NOT_FOUND_INFO = 		6007;	#링크 정보를 찾을수 없음
    SC_LINK_WRONG_PW = 				6008;	#링크 패스워드 틀림

    SC_FOUND_SUB_PUB = 				6010;	# 하위폴더에 공유가 존재함
    SC_FOUND_PARENT_PUB = 			6011;	# 상위폴더에 공유가 존재함

    SC_PUB_NOT_FOUND_INFO = 		6012;	# 공유정보를 찾지 못함
    SC_PUB_DELETE_INFO = 			6013;	# 삭제된 공유 정보
    SC_PUB_EXCEED_DAY = 			6014;	# 공유 날짜 초과
    SC_PUB_INPUT_PW = 				6015;	# 공유 패스워드 입력
    SC_PUB_WRONG_PW = 				6016;	# 공유 패스워드 틀림
    SC_PUB_DELETE_ITEM_INFO = 		6017;	# 공유  아이템 정보를 찾을 수 없음.

    SC_GUEST_SAME_ID = 				6030;	# 동일할 게스트 아이디 존재.
    SC_NOT_FOUND_GUEST_INFO = 		6031;	# 게스트 정보를 찾을 수 없습니다.

    SC_ALREADY_BATCH_JOB_INFO = 	6040;	# 이미 진행중인 작업이 있습니다.
    SC_JOB_WATING =  				6041; 	# 작업이 대기입니다.
    SC_JOB_RUNNING =  				6042; 	# 작업이 수행중입니다.
    SC_JOB_FINISHED =  				6043; 	# 작업이 완료되었습니다.
    SC_JOB_ERROR =  				6044; 	# 작업이 오류 상태입니다.
    SC_JOB_CANCELED =  				6045; 	# 작업이 오류 상태입니다.

    SC_PROJECT_FULL_MEMBER = 		6050;	# 프로젝트 멤버가 모두 다 찾습니다.
    SC_PROJECT_INPUT_PW = 			6051;	# 프로젝트 패스워드를 입력.
    SC_PROJECT_WRONG_PW = 			6052;	# 프로젝트 패스워드를 틀림.
    SC_PROJECT_MEMBER_GROUP_NO_OUT =6053;	# 프로젝트 그룹으로 가입되어 있어 탈퇴 불가합니다.
    SC_PROJECT_ALREADY_ADD = 	    6054;	# 프로젝트 그룹으로 이미 추가된 사용자입니다.

    SC_POLICY_CHECK_PW = 		    6060;	# 정책에 맞지 않는 비밀번호
    SC_ERR_DRM_DOWNLOAD =           6061;   # DRM 다운로드시 DRM 안걸려있으면 나는 에러

    SC_APRVL_AUTH_ACCESS = 			6100;   #결재 권한이 없거나 결재자 기한이 초과되었습니다.

    #############################/
    # *** 7000 - 7999 ***
    # 신규 클라이언트 코드
    #############################/


    #############################/
    # *** 100000 - 19999 ***
    # 배치 어플리케이션
    #############################/

    WEB_ERROR = 						20000;
    ADMIN_ERROR = 					    21000;
    BATCH_ERROR = 					    22000;

    # 배치 어플리케이션
    BT_NOT_SUPPORTED_PLATFORM =  		100001;
    BT_ERR_INSTALL_SERVICE =  			100002;
    BT_ERR_UNINSTALL_SERVICE =  		100003;
    BT_ERR_START_SERVICE =  			100004;
    BT_ERR_STOP_SERVICE =  				100005;
    BT_ERR_QUERY_SERVICE_STATUS =  		100006;
    BT_ERR_START_SERVICE_DISPATCHER =  	100007;
    BT_OVER_MAX_RETRY_COUNT =  			100008;

    BT_ERR_CREATE_LOCK_FILE =  			100009;
    BT_ERR_OPEN_LOCK_FILE =  			100010;
    BT_ERR_LOCK_FILE =  				100011;



    ###########################/
    # 1-100
    # PHP Extension에서의 오류 코드 시작
    ###########################/
    ERR_CREATE_CRYPTO_KEY = 		1;
    ERR_INIT_CRYPTO = 				2;
    ERR_INIT_COMPRESS = 			3;
    ERR_OPEN_SOURCE_FILE = 			4;
    ERR_OPEN_TARGET_FILE = 			5;
    ERR_ENCRYPT = 					6;
    ERR_COMPRESS = 					7;
    ERR_WRITE_FILE = 				8;
    ERR_DECRYPT = 					9;
    ERR_DECOMPRESS = 				10;
    ERR_OPT_ERROR = 				11;
    ERR_OPT_RUN_TYPE = 				12;
    ERR_OPT_PATH = 					13;
    ERR_OPT_MRK = 					14;
    ERR_OPT_ENC_MODE = 				15;
    ERR_OPT_ZIP_MODE = 				16;
    ERR_READ_FILE = 				17;
    ERR_PI_INIT = 					18;
    ERR_PI_CREATE_SCANNER = 		19;
    ERR_PI_ALREADY_INIT = 			20;
    ERR_PI_LOAD_POLICY = 			21;
    ERR_PI_SET_CONFIG = 			22;
    ERR_PI_SCAN_FILE = 				23;
    ERR_PI_NO_PATTERN = 			24;
    ERR_PI_GET_PATTERN_CNT = 		25;
    ERR_PI_GET_DETAIL_RESULT_TYPE = 26;
    ERR_PI_GET_PATTERN_ID = 		27;
    ERR_PI_GET_COUNT = 				28;
    ERR_PI_GET_DETAIL_COUNT = 		29;
    ERR_PI_GET_DETAIL_VALUE = 		30;
    ERR_PI_GET_DETAIL_RESULT_PATH = 31;
    ERR_PI_GET_POLICY_ID = 			32;
    ERR_PI_GET_POLICY_NAME = 		33;
    ERR_PI_GET_POLICY_MIN_LIMIT = 	34;
    ERR_PI_TIME_LIMIT = 			35;
    ERR_PI_SAVE_RESULT = 			36;

    ERR_DRM_INIT = 					41;
    ERR_DRM_ENCRYPT = 				42;
    ERR_DRM_DECRYPT = 				43;

    ERR_READ_META_FILE = 			50;
    ERR_COPY_FILE = 				51;
    ERR_RENAME_FILE = 				52;
    ERR_ICONV = 					53;
    ERR_UNMATCHED_FILE_SIZE = 		54;
    ERR_OVER_MAX_RETRY_CNT =  		55;
    ERR_LOAD_EXTENSION =  			56;
    ERR_UNKNONW_ENC_MODE =  		57;


    ####################/
    # 문서 추출 에러 코드
    # 10000 ~ 10020
    ####################/
    ERR_PI_EXTRACT_FATAL = 				10000;
    ERR_PI_EXTRACT_UNKNOWN = 			10001;
    ERR_PI_EXTRACT_ENCRYPTED = 			10002;
    ERR_PI_EXTRACT_UNSUPPORTED_VERSION = 10003;
    ERR_PI_EXTRACT_UNKNOWN_FORMAT = 	10004;
    ERR_PI_EXTRACT_DRM = 				10005;
    ERR_PI_EXTRACT_BAD_FILE = 			10006;
    #
    ############################


    #######################
    # 메시지용 코드 
    SC_MSG_AUTH_DELETE_ERR_IN_SUB =  	        900000;
    SC_MSG_ERR_MOVE_PASSWORD_FOLDER =           900001; # 패스워드 폴더 이동
    SC_MSG_ERR_COPY_PASSWORD_FOLDER =           900002; # 패스워드 폴더 복사
    SC_MSG_ERR_DOWNLOAD_PASSWORD_FOLDER =       900003; # 패스워드 폴더 다운로드 
    SC_MSG_ERR_DELETE_PASSWORD_FOLDER =         900004; # 패스워드 폴더 삭제 
    SC_MSG_ERR_LOCK_PASSWORD_FOLDER =           900005; # 패스워드 폴더 잠금설정
    SC_MSG_ERR_UNLOCK_PASSWORD_FOLDER =         900006; # 패스워드 폴더 잠금해제
    SC_MSG_ERR_MOVE_LOCK_FILE =                 900007; # 잠금 파일 이동 오류 
    SC_MSG_ERR_DELETE_LOCK_FILE =               900008; # 잠금 파일 삭제 오류
    SC_MSG_NO_DELETE_FILE_AUTH =                900009; # 파일 삭제 권한이 없음
    SC_MSG_NO_DELETE_NODE_AUTH =                900010; # 폴더 삭제 권한이 없음
    SC_MSG_ERR_DELETE_LOCK_NODE =               900011; # 잠금 폴더 삭제 오류
    SC_MSG_ERR_DELETE_INCLUDE_LOCK_FILE =       900012; # 잠금 파일 포함 폴더 삭제 오류
    SC_MSG_ERR_COPY_NO_READ_AUTH =              900013; # 읽기 권한이 없어 복사할 수 없음
    SC_MSG_ERR_COPY_NO_WRITE_AUTH =             900014; # 쓰기 권한이 없어 복사할 수 없음
    SC_MSG_ERR_NO_WRITE_AUTH_TARGET_NODE =      900015; # 대상 폴더에 쓰기 권한 없음
    SC_MSG_ERR_MOVE_SYSTEM_NODE =               900016; # 시스템 폴더 이동 오류 
    SC_MSG_FAVORITIES_ALREADY_EXISTS =          900017; # 이미 등록된 즐겨찾기 폴더
    SC_MSG_NO_CREATE_FOLDER_PWD_AUTH =          900018; # 폴더 패스워드를 설정할 권한이 없음
    SC_MSG_NO_USER_FOUND =                      900019; # 사용자를 찾을 수 없습니다.
    SC_MSG_ERR_RENAME_LOCK_FILE =               900020; # 잠금 파일 이름 변경 오류
    SC_MSG_ERR_SHARE_FOLDER_NOT_FOUND =         900021; # 공유 폴더 찾기 오류 
    SC_MSG_ERR_RELEASE_SHARE_FOLDER_AUTH =      900022; # 공유 폴더 해제 권한 없음
    SC_MSG_ERR_RELEASE_SHARE_FOLDER_BY_GROUP =  900023; # 그룹으로 등록된 경우 해제 불가. 
    SC_MSG_ERR_CREATE_SHARE_FOLDER_AUTH =       900024; # 공유 폴더를 생성할 권한이 없습니다.
    SC_MSG_ERR_OVERWRITE_TARGET_LOCK_FILE =     900025; # 대상이 잠금 설정된 경우 덮어쓰기 불가 
    SC_MSG_ERR_MOVE_LOCK_NODE =                 900026; # 잠금 폴더 이동 오류
    SC_MSG_FOUND_LOCK_FILE =                    900027; # 잠금 폴더 이동 오류

    SC_MSG_ERR_LOGIN_FAIL =                     900028; # 로그인에 실패했습니다
    SC_MSG_ERR_WEB_LOGIN_ADMIN_FAIL =           900029; # SYSTEM 유저로 로그인 할 수 없습니다
    SC_MSG_ERR_WEB_LOGIN_FUNC_FAIL =            900030; # 웹버전이 사용 제한되어 있습니다. 관리자에게 문의하시기 바랍니다
    SC_MSG_PWD_INIT_CHANGE =                    900031; # 현재 사용중인 비밀번호는 기본 비밀번호 입니다.\\n\\n비밀번호 변경후 정상적으로 사용할 수 있습니다.\\n\\n[확인]버튼을 클릭하여 비밀번호를 변경하여 주십시오.
    SC_MSG_ERR_LINK_NOT_ACCESS =                900032; # 접근이 허용되지 않는 사용자입니다.

    SC_MSG_ERR_COPY_ITEM =                      900033; # 복사할 수 없는 아이템입니다.
    SC_MSG_ERR_MOVE_ITEM =                      900034; # 복사 불가
    SC_MSG_ERR_DOWNLOAD_ITEM =                  900035; # 다운로드 불가
    SC_MSG_ERR_ZIP_DOWNLOAD_FODER_PWD_FAIL =    900036; # 압축 파일 다운로드  폴더 비밀번호 인증되지 않음.
    SC_MSG_ERR_CHECK_FODER_PWD_FAIL =           900037; # 폴더 비밀번호 인증되지 않음.

    SC_MSG_ERR_CHECK_REPEAT_ATTACK =            900038; # 폴더 비밀번호 인증되지 않음.

class MMessage():
    
        briefMsgDict = {
            StatusCode.RESULT_SUCCESS.value: ('성공', 'OK'), 
            StatusCode.RESULT_CONTINUE.value: ('다음작업', 'Next Job'), 
            StatusCode.RESULT_STOP.value: ('작업중지', 'Stop'),
            StatusCode.RESULT_RETRY.value: ('작업재시도', 'Retry'),
            StatusCode.RESULT_SUCCESSFUL.value: ('200 OK', '200 OK'),
            StatusCode.SC_LOGIN_NOT_FOUND_UID.value: ('존재하지 않는 계정', 'ID not found'),
            StatusCode.SC_LOGIN_WRONG_PWD.value: ('암호오류', 'Wrong Password'),
            StatusCode.SC_LOGIN_EXPIRED_UID.value: ('계정사용기간초과', 'Expired ID'),
            StatusCode.SC_LOGIN_PAUSED_UID.value: ('계정일시정지', 'Unavaliable ID'),
            StatusCode.SC_LOGIN_WRONG_VERSION.value: ('버젼 불일치', 'Wrong version'),
            StatusCode.SC_LOGIN_MAINTAIN_SYS.value: ('서버 점검중', 'Under maintenance'),
            StatusCode.SC_LOGIN_EXCEED_LICENSE.value: ('라이선스 초과', 'Exceed max license'),
            StatusCode.SC_LOGIN_EXPIRED_PWD.value: ('비밀번호 사용기간 초과', 'Expired password'),
            StatusCode.SC_LOGIN_LOCK_UID.value: ('계정 잠김', 'Locked ID'),
            StatusCode.SC_ERR_USER_AUTH.value: ('사용자 인증오류', 'Authentication failure'),
            StatusCode.SC_ERR_SERVICE_NOT_INITIALIZED.value: ('서비스가 초기화되지 않음', 'Not initialized service'),
            StatusCode.SC_ERR_INVALID_LICENSE.value: ('잘못된 라이선스 파일', 'Invalid license file'),
            StatusCode.SC_LOGIN_LOCK_DURATION.value: ('계정 잠김(기간 잠금)', 'Locked ID(temporary)'),
            StatusCode.SC_BUILDNO_NOT_FOUND.value: ('빌드정보 누락', 'Build info. not found'),
            StatusCode.SC_LOGIN_CLOSED_UID.value: ('폐쇄된 계정', 'Closed ID'),
            StatusCode.SC_NOT_ALLOWED_IP.value: ('접근제한 IP', 'Restricted IP'),
            StatusCode.SC_NOT_ALLOWED_MAC.value: ('접근제한 MAC', 'Restricted Mac'),
            StatusCode.SC_CONFIG_NOT_FOUND.value: ('정책조회 실패', 'Policy not found'),
            StatusCode.SC_NOT_ALLOWED_TIME.value: ('접근제한 시간', 'Restricted Time'),
            StatusCode.SC_INVALID_BUILDNO.value: ('사용할 수 없는 빌드번호', 'Invalid build number'),
            StatusCode.SC_NOT_ALLOWED_SERVICE.value: ('사용불가 서비스', 'Not allowed service'),
            StatusCode.SC_DUP_LOGIN_EXIST.value: ('중복 로그인 존재', 'Duplicate login'),
            StatusCode.SC_FOUND_SAME_HASH.value: ('해쉬파일 존재', 'Same HASH file found'),
            StatusCode.SC_SKIP_OVER_FILE.value: ('스킵 파일', 'Skip File'),
            StatusCode.SC_NOT_FOUND_FILE.value: ('해당파일 없음', 'File not found'),
            StatusCode.SC_NOT_OPEN_FILE.value: ('파일 열기 오류', 'File open error'),
            StatusCode.SC_NOT_SEEK_FILE.value: ('파일포인터 이동 오류', 'File seek error'),
            StatusCode.SC_NOT_READ_FILE.value: ('파일 읽기 오류', 'File read error'),
            StatusCode.SC_NOT_WRITE_FILE.value: ('파일 쓰기 오류', 'File write error'),
            StatusCode.SC_NOT_CLOSE_FILE.value: ('파일 닫기 오류', 'File close error'),
            StatusCode.SC_NOT_SAME_FSIZE.value: ('전송 크기 오류', 'Transfer size mismatch'),
            StatusCode.SC_EXCEED_SESSION.value: ('세션 초과', 'Exceed max session'),
            StatusCode.SC_OVER_VOL_SIZE.value: ('시스템 볼륨용량 초과(S)', 'System volume exceeded'),
            StatusCode.SC_OVER_USER_SIZE.value: ('사용자 할당용량 초과(S)', 'User capacity exceeded'),
            StatusCode.SC_INVALID_SESSION.value: ('불법 세션', 'Invalid Session'),
            StatusCode.SC_FOUND_SAME_DIR.value: ('동일폴더 존재', 'Same folder found'),
            StatusCode.SC_FOUND_SAME_FILE.value: ('동일파일 존재', 'Same file found'),
            StatusCode.SC_NOT_FOUND_DIR.value: ('노드 없음', 'Node not found'),
            StatusCode.SC_OVER_FIELD_SIZE.value: ('DB 필드길이 초과', 'Exceeded max DB field length'),
            StatusCode.SC_INVALID_XML_DATA.value: ('XML 데이타 오류', 'XML Error'),
            StatusCode.SC_FOUND_SAME_ACL.value: ('동일 ACL 존재', 'Same ACL found'),
            StatusCode.SC_FOUND_SAME_PUB.value: ('동일 PUB 존재', 'Same PUB found'),
            StatusCode.SC_FOUND_SAME_SUB.value: ('동일 SUB 존재', 'Same SUB found'),
            StatusCode.SC_FOUND_SUB_DIR.value: ('하위폴더 존재', 'Sub-folders found'),
            StatusCode.SC_OVER_DISK_SIZE.value: ('시스템디스크 용량초과(S)', 'System disk size exceeded'),
            StatusCode.SC_AUTHORITY_ERR.value: ('권한 없음', 'No authority'),
            StatusCode.SC_FOUND_VIRUS.value: ('바이러스 발견', 'Infected file'),
            StatusCode.SC_CHANGE_FILE.value: ('전송중 파일변경 오류', 'File changed during transfer'),
            StatusCode.SC_FOUND_LOCK_FILE.value: ('잠금파일 존재', 'Locked file found'),
            StatusCode.SC_FOUND_LOCK_FILE_MYSELY.value: ('잠금파일발견(자신이잠금)', 'Locked file(self)'),
            StatusCode.SC_FOUND_LOCK_FILE_OTHER.value: ('잠금파일발견(타인이잠금)', 'Locked file(others)'),
            StatusCode.SC_FOUND_MANUAL_LOCK.value: ('잠금해제 실패', 'Unlock failure'),
            StatusCode.SC_DO_NOT_USE_TIME.value: ('사용할 수 없는 시간', 'Restricted time'),
            StatusCode.SC_FAIL_OPEN_LOCK_FILE.value: ('열기 오류(잠금파일)', 'File open error(locked)'),
            StatusCode.SC_FAIL_LOCK_FILE.value: ('파일락 오류', 'lock file error'),
            StatusCode.SC_FAIL_SQL_QUERY.value: ('SQL 오류', 'SQL error'),
            #StatusCode.SC_PERMISSION_FAIL.value: (기업은행용.파일업로드권한없음.),
            StatusCode.SC_BLOCK_MISSING.value: ('누락된 블록(고속전송)', 'missing block(Rapid Transfer)'),
            StatusCode.SC_NOT_SCAN_VIRUS.value: ('바이러스 미검사', 'not checked infection'),
            StatusCode.SC_NOT_CRC_FILE.value: ('CRC 오류', 'CRC error'),
            StatusCode.SC_ERR_UNSUPPORTED_ENC_MODE.value: ('지원하지 않는 암호화모드', 'unsupported encryption mode'),
            StatusCode.SC_ERR_CREATE_CRYPTO_KEY.value: ('암호화키 생성 오류', 'encryption key creation failure'),
            StatusCode.SC_ERR_INITIALIZE_CRYPTO.value: ('암호화 모듈 초기화 오류', 'encryption module initialization failure'),
            StatusCode.SC_ERR_DECRYPT_DATA.value: ('복호화 오류', 'decryption error'),
            StatusCode.SC_ERR_ENCRYPT_DATA.value: ('암호화 오류', 'encryption error'),
            StatusCode.SC_TIMEOUT.value: ('시간초과', 'timeout'),
            StatusCode.SC_ERR_RECV_DATA.value: ('데이터 수신 오류', 'data receiving error'),
            StatusCode.SC_ERROR_PERSNAL_YN.value: ('개인정보 파일', 'including personal information'),
            StatusCode.SC_ERR_COMPRESS.value: ('압축 실패', 'compress error'),
            StatusCode.SC_ERR_UNCOMPRESS.value: ('압축해제 실패', 'uncompress error'),
            StatusCode.SC_NO_DATA.value: ('데이터 없음', 'no data'),
            StatusCode.SC_INVALID_METHOD.value: ('잘못된 메소드', 'invalid method'),
            StatusCode.SC_ERR_ZIPFILE.value: ('압축파일 생성 실패', 'zip file creation failure'),
            StatusCode.SC_ERR_DB_CONN.value: ('DB 연결 오류', 'DB connction error'),
            StatusCode.SC_DIR_NOT_CHANGED.value: ('디렉토리 변경 오류', 'failed to change directory'),
            StatusCode.SC_ERR_CREATE_DIR.value: ('디렉토리 생성 실패', 'failed to create folder'),
            StatusCode.SC_ERR_SEND_HTTP.value: ('HTTP전송 실패', 'HTTP transfer error'),
            StatusCode.SC_ERR_COPY_FILE.value: ('파일 복사 에러', 'copy file error'),
            StatusCode.SC_AUTH_READ_ERR.value: ('읽기 권한 없음', 'no read permission'),
            StatusCode.SC_AUTH_WRITE_ERR.value: ('쓰기 권한 없음', 'no write permission'),
            StatusCode.SC_AUTH_DELETE_ERR.value: ('삭제 권한 없음', 'no delete permission'),
            StatusCode.SC_AUTH_ADMIN_ERR.value: ('관리자 권한 없음', 'no admin authority'),
            StatusCode.SC_DELETE_FILE_ERR.value: ('파일 삭제 오류', 'failed to delete file'),
            StatusCode.SC_NOT_OPEN_STREAM.value: ('스트림 열기 실패', 'failed to open stream'),
            StatusCode.SC_NOT_FOUND_VOL.value: ('볼륨 찾기 실패', 'volume not found'),
            StatusCode.SC_ERR_META_INFO.value: ('메타정보 처리 실패', 'failed to handle meta information'),
            StatusCode.SC_ERR_RAPID_INDEX_INFO.value: ('인덱스 처리 실패(고속전송)', 'failed to handle index(rapid transfer)'),
            StatusCode.SC_EXCEED_MAX_FILE_SIZE.value: ('최대 파일크기 초과', 'exceeded max file size'),
            StatusCode.SC_NOT_EXEC_COMMAND.value: ('명령어 처리 실패', 'failed to execute command'),
            StatusCode.SC_NOT_FOUND_ITEM.value: ('아이템 찾기 실패', 'item not found'),
            StatusCode.SC_ERR_MOVE_FILE.value: ('잘못된 파라미터', 'invalid parameter'),
            StatusCode.SC_AUTH_SYSTEM_NODE_ERR.value: ('시스템 폴더 처리 오류', 'failed to handle system node'),
            StatusCode.SC_PASSWORD_NODE_FOUND.value: ('비밀번호 폴더 존재', 'password folder found'),
            StatusCode.SC_ORDERMARK_UNMATCH.value: ('ORDERMARK 오류', 'ORDERMARK error'),
            StatusCode.SC_CONNECTION_CLOSE.value: ('연결 종료', 'disconnected'),
            StatusCode.SC_NOT_RENAME_ITEM.value: ('이름변경 오류', 'rename error'),
            StatusCode.SC_NOT_ALLOW_CHAGE_VALUE.value: ('값변경 불가 오류', 'not allowed to change value'),
            StatusCode.SC_AUTH_VIEW_ERR.value: ('보기 권한 없음', 'no view permission'),
            StatusCode.CS_NOT_FOUND_FILE.value: ('파일 찾기 오류', 'file not found'),
            StatusCode.CS_NOT_OPEN_FILE.value: ('파일 열기 오류', 'file open error'),
            StatusCode.CS_NOT_READ_FILE.value: ('파일 읽기 오류', 'file read error'),
            StatusCode.CS_NOT_WRITE_FILE.value: ('파일 쓰기 오류', 'file write error'),
            StatusCode.CS_NOT_CLOSE_FILE.value: ('파일 닫기 오류', 'file close error'),
            StatusCode.CS_NOT_SAME_FSIZE.value: ('파일 크기 오류', 'file size mismatched'),
            StatusCode.CS_CANCEL_WORK.value: ('취소버튼 클릭', 'cancel'),
            StatusCode.CS_SAME_FILE.value: ('동일 파일', 'same file'),
            StatusCode.CS_NOT_RENAME_FILE.value: ('파일 이름변경 오류', 'failed to rename file'),
            StatusCode.CS_SYS_UNKNOWN_EXP_ERR.value: ('클라이언트 Exception 오류', 'client exception'),
            StatusCode.CS_XML_UNKNOWN_EXP_ERR.value: ('XML Exception 오류', 'XML exception'),
            StatusCode.CS_SQL_UNKNOWN_EXP_ERR.value: ('SQL Exception 오류', 'SQL exception'),
            StatusCode.CS_NOT_CREATE_DIR.value: ('디렉토리 생성 실패', 'failed to create directory'),
            StatusCode.CS_OVER_DISK_SIZE.value: ('디스크 용량 초과', 'exceeded disk capacity'),
            StatusCode.CS_SUB_FUNC_RETURN_ERR.value: ('디스크 용량 얻기 실패', 'failed to get disk capacity'),
            StatusCode.CS_NOT_CRC_FILE.value: ('전송중 파일변경', 'file changed during transfer'),
            StatusCode.CS_NOT_SEEK_FILE.value: ('파일포인터 이동오 류(C)', 'failed to move pointer'),
            StatusCode.CS_TURNOFF_PC.value: ('컴퓨터 종료', 'shutdown computer'),
            StatusCode.CS_FAIL_COMPRESS.value: ('전송중 압축 오류(C)', 'compress error during transfer'),
            StatusCode.CS_NOT_RECV_MRK.value: ('암호화키(MRK) 수신 오류', 'encryption key not received'),
            StatusCode.CS_LOCK_FILE_ALREADY.value: ('다른 프로세스가 처리중', 'occupied by other process'),
            StatusCode.CS_NOT_OBTAIN_DIR_NODE.value: ('디렉토리 조회 오류', 'directory not found'),
            StatusCode.CS_FASSO_ERROR.value: ('파수DRM 에러', 'Fasoo DRM error'),
            StatusCode.CS_NOT_CREATE_RESOURCE.value: ('리소스 생성 실패', 'failed to create resources'),
            StatusCode.CS_NO_MORE_ITEMS.value: ('아이템이 더이상 없음', 'no more item'),
            StatusCode.CS_NOT_WRITE_LOG.value: ('로그 쓰기 실패', 'write log error'),
            StatusCode.CS_NOT_DELETE_FILE.value: ('파일 삭제 실패', 'failed to delete file'),
            StatusCode.CS_ERR_PASSWORD_AUTH.value: ('비밀번호 인증실패', 'password authentication failure'),
            StatusCode.SC_NOT_FOUND_SESSION.value: ('잘못된 세션', 'invalid session'),
            StatusCode.SC_CUSTOM_ERROR.value: ('사용자 정의 에러', 'custom error'),
            StatusCode.CS_TIMEOUT.value: ('시간 초과','timeout'),
            StatusCode.CS_MISSING_BLOCK.value: ('데이터 블럭 누락(고속전송)', 'mission block(rapid transfer'),
            StatusCode.CS_ERR_RAPID_INDEX_INFO.value: ('인덱스처리실패(고속전송)', 'failed to handle index(rapid transfer)'),
            StatusCode.CS_DISCONNECT_SERVER.value: ('서버 연결 해제', 'disconnected'),
            StatusCode.CS_UNKNOWN_HEADER.value: ('알수없는 헤더 오류', 'unknown header'),
            StatusCode.CS_CANT_MAKE_HEADER.value: ('헤더 생성 오류', 'failed to create header'),
            StatusCode.CS_MISMATCH_HEADER.value: ('일치하지 않는 프로토콜', 'invalid header'),
            StatusCode.CANT_READ_RESULT_CODE.value: ('결과값 읽기 오류', 'failed to read result'),
            StatusCode.CS_ADD_NODE_ERR.value: ('노드 추가 오류(C)', 'failed to add node'),
            StatusCode.CS_CANT_CREATE_SOCKET.value: ('소켓 생성 오류(C)', 'failed to create socket'),
            StatusCode.CS_CANT_CONNECT_SERVER.value: ('서버 접속 오류(C)', 'failed to connect to server'),
            StatusCode.CS_FILE_ALREADY_EXISTS.value: ('동일 파일명 존재', 'same file name found'),
            #StatusCode.CC_FAIL_CREATE_ADM_SOCKET.value: (통합서버(ADM)소켓생성을실패하였습니다.),
            #StatusCode.CC_FAIL_CONNECT_ADM_SERVER.value: (통합서버(ADM)연결에실패하였습니다.),
            #StatusCode.CC_FAIL_CREATE_NS_SOCKET.value: (백업서버(NS)소켓생성을실패하였습니다.),
            #StatusCode.CC_FAIL_CONNECT_NS_SERVER.value: (백업서버(NS)연결에실패하였습니다.),
            StatusCode.CC_FAIL_SEND_PACKET.value: ('패킷 송신 실패', 'send packet error'),
            StatusCode.CC_FAIL_RECV_PACKET.value: ('패킷 수신 실패', 'receive packet error'),
            StatusCode.CC_FAIL_MAKE_HEADER.value: ('헤더 생성 오류', 'failed to create header'),
            StatusCode.CC_FAIL_ADD_NODE.value: ('노드추가 오류(C)', 'failed to add node'),
            StatusCode.CC_WRONG_ORDER_MARK.value: ('잘못된 패킷(OrderMark)', 'invalid packet(OrderMark)'),
            StatusCode.CC_MISMATCH_COMMAND.value: ('프로토콜 명령어 불일치', 'protocol command mismatch'),
            StatusCode.CC_DISCONNECTED_SERVER.value: ('서버 연결 해제', 'disconnected from server'),
            StatusCode.CC_FAIL_CONNECT_IIS_SERVER.value: ('서버 연결 실패', 'connection failure'),
            StatusCode.CC_FAIL_DELETE_MDB.value: ('MDB 파일 삭제 실패', 'failed to delete MDB file'),
            StatusCode.CC_BAD_HTTP.value: ('지원하지 않는 프로토콜', 'unsupported protocol'),
            StatusCode.CC_FAIL_CREATE_UPGRADE_INFO_XML.value: ('UPGRADE_INFO.XML 생성 실패', 'failed to create upgrade XML file'),
            StatusCode.CC_FAIL_ENCODE_BASE64.value: ('BASE64 인코딩 오류', 'BASE64 encoding error'),
            StatusCode.CC_FAIL_DECODE_BASE64.value: ('BASE64 디코딩 오류', 'BASE64 decoding error'),
            StatusCode.CC_LIC_ERROR.value: ('라이선스오류', 'license error'),
            StatusCode.CC_FAIL_FOLDER_INPUT_PWD.value: ('', ''),
            StatusCode.CC_FAIL_FOLDER_WRONG_PWD.value: ('', ''),
            StatusCode.SC_SYS_UNKNOWN_EXP_ERR.value: ('시스템 알수없는 에러', 'unknown system error'),
            StatusCode.SC_SYS_CONFIG_ERR.value: ('시스템 설정 오류', 'configuration error'),
            StatusCode.SC_XML_UNKNOWN_EXP_ERR.value: ('XML오류', 'XML error'),
            StatusCode.SC_SQL_UNKNOWN_EXP_ERR.value: ('SQL오류', 'SQL error'),
            StatusCode.SC_SUB_FUNC_RETURN_ERR.value: ('함수 리턴 오류', 'fuction error'),
            StatusCode.CS_RETRY_NETWORK_CONNECT.value: ('재접속중(네트워크 장애)', 'retrying(network failure)...'),
            StatusCode.CS_PREPARE_TRANSFER.value: ('준비중...', 'preparing...'),
            StatusCode.CS_ALREADY_UPLOAD.value: ('다른 프로세스가 전송중', 'uploading by other process'),
            StatusCode.CS_RESUME_UPLOAD.value: ('이어올리기중...', 'continuous transferring...'),
            StatusCode.CS_EXCEPTION_UPLOAD.value: ('전송중 예외 오류', 'error occurred during transferring'),
            StatusCode.CS_DONE_TRANSFER.value: ('전송 완료', 'transfer complete'),
            StatusCode.CS_HASH_OPNE_ERROR.value: ('해시파일 열기 오류(C)', 'failed to open HASH file'),
            StatusCode.CS_HASH_PREPARE.value: ('해시 비교 준비중(H)...', 'preparing HASH file for comparision'),
            StatusCode.CS_HASH_READ_ERROR.value: ('해시파일 읽기 오류(C)', 'failed to read HASH file'),
            StatusCode.CS_END_COMPUTER.value: ('컴퓨터 종료', 'shutdown computer'),
            StatusCode.CS_UPLOADLIST_ERROR.value: ('업로드 리스트 오류', 'upload list error'),
            StatusCode.CS_DOWNLOADLIST_ERROR.value: ('다운로드 리스트 오류', 'download list error'),
            StatusCode.CS_DOWNLOAD_CREATE_FOLDER.value: ('폴더 생성', 'folder creation'),
            StatusCode.CS_DOWNLOAD_OPENFILE.value: ('읽기 전용', 'read-only'),
            StatusCode.CS_DOWNLOAD_DIRECTEDIT.value: ('직접 편집', 'direct edit'),
            StatusCode.CS_DOWNLOAD_SKIP.value: ('동일파일스킵(C)', 'file skipped'),
            StatusCode.CS_DISK_GETSIZE_ERROR.value: ('디스크 용량 얻기 실패(C)', ''),
            StatusCode.CS_DISK_SIZE_NOTENOUGH.value: ('디스크용량부족(C)', ''),
            StatusCode.CS_DOWNLOAD_CONVERT_ERROR.value: ('파일변환오류(C)', ''),
            StatusCode.CS_WAIT_TRANSFER.value: ('전송중...', 'tramsferring...'),
            StatusCode.CS_DOWNLOAD_CONVERT_WAIT.value: ('변환중...', 'converting...'),
            StatusCode.CS_DOWNLOAD_CONVERT_DONE.value: ('변환 완료...', 'converted'),
            StatusCode.CS_FIND_CONNECT_ERROR.value: ('연결된실행파일을찾는중에오류가발생하였습니다.', ''),
            StatusCode.CS_SAVE_OPENFIE_ERROR.value: ('파일열기정보를저장할수없습니다.', ''),
            StatusCode.CS_BACKUPLIST_ERROR.value: ('백업리스트오류', ''),
            StatusCode.CS_CANCEL_TRANSFER.value: ('전송취소', 'cancel transfer'),
            StatusCode.SC_SYNC_USER_NOT_EXISTS.value: ('동기화사용자ID가존재하지않습니다.', ''),
            StatusCode.SC_SYNC_USER_SAME_ID.value: ('동일한동기화사용자ID가이미존재합니다.', ''),
            StatusCode.SC_SYNC_NODE_NOT_EXISTS.value: ('동기화폴더가존재하지않습니다.', ''),
            StatusCode.SC_MORE_ACTION_EXISTS.value: ('마지막동기화후서버에변경된내용이있습니다.', ''),
            StatusCode.SC_APRVL_ALREADY_PROGRESS.value: ('이미결재진행중임', ''),
            StatusCode.SC_OBJECT_NOT_FOUND.value: ('아이템 찾기 실패', 'item not found'),
            StatusCode.SC_INVALID_REQUEST.value: ('잘못된 요청', 'invalid request'),
            StatusCode.SC_FAIL_CREATE_TEMP_FILE.value: ('임시파일 생성 실패', 'failed to create temporary file'),
            StatusCode.SC_OBJECT_EXISTS.value: ('오브젝트 존재', 'object found'),
            StatusCode.SC_PARENT_OBJECT_NOT_FOUND.value: ('부모 아이템 찾기 실패', 'parent item not found'),
            StatusCode.SC_INVALID_SEEK_POINTER.value: ('파일포인터 오류', 'file pointer error'),
            StatusCode.SC_PERSONAL_INFO_EXIST.value: ('개인정보 포함파일', 'including personal information'),
            StatusCode.SC_PERSONAL_INFO_CHECKING.value: ('개인정보 검색중', 'searching file including personal information'),
            StatusCode.SC_NOT_FOUND_RFILE.value: ('원격파일 찾기 실패', 'remote file not found'),
            StatusCode.SC_NOT_CREATE_DIR.value: ('디렉토리 생성 실패', 'failed to create directory'),
            StatusCode.SC_NOT_CREATE_FILE.value: ('파일 생성 실패', 'failed to create file'),
            StatusCode.SC_NOT_CREATE_PROCESS.value: ('프로세스생성실패', ''),
            StatusCode.SC_NOT_CREATE_SHORTCUT.value: ('바로가기 생성 실패', 'failed to invoke process'),
            StatusCode.SC_FILE_CHANGED.value: ('파일 변경됨', 'file changed'),
            StatusCode.SC_DIR_NOT_EMPTY.value: ('빈 디렉토리가 아님.', 'not empty directory'),
            StatusCode.SC_TARGET_OBJECT_NOT_FOUND.value: ('대상 아이템 없음.', 'target item not found'),
            StatusCode.SC_TARGET_PARENT_OBJECT_NOT_FOUND.value: ('대상 아이템의 부모노드 없음', 'parent node not found'),
            StatusCode.SC_ERR_LONG_NAME.value: ('지원할 수 없는 긴이름', 'long path name'),
            StatusCode.SC_MOVE_FOLDER_TO_DIFFERENT_DB.value: ('폴더이동 오류(다른영역)', 'failed to move folder'),
            StatusCode.SC_SRC_TGT_DBIDX_UNMATCH.value: ('원본과 대상의 DB인덱스 다름', 'DB index mismatched'),
            StatusCode.SC_NODE_MOVED.value: ('노드 이동 완료', ''),
            StatusCode.SC_FOUND_PASSWORD_FOLDER.value: ('암호 폴더 발견', ''),
            StatusCode.SC_NOT_DELETE_PASSWORD_DIR.value: ('암호 폴더 삭제오류', ''),
            StatusCode.SC_NOT_MOVE_PASSWORD_DIR.value: ('암호 폴더 이동오류', ''),
            StatusCode.SC_REJECT_LOGIN_COS_INIT_PASSWORD.value: ('초기패스워드로로그인오류', ''),
            StatusCode.SC_ERR_PUB_NOT_FOUND.value: ('공유정보찾기실패', ''),
            StatusCode.SC_ERR_PUB_GROUP_TYPE.value: ('공유유형조회실패', ''),
            StatusCode.SC_ERR_PREV_POLICY_NOT_FOUND.value: ('이전정책을찾을수없음.관리자페이지에서사용', ''),
            StatusCode.SC_POLICY_STILL_USED.value: ('정책이사용중임.', ''),
            StatusCode.SC_ACTION_ID_NOT_FOUND.value: ('활동ID찾기실패', ''),
            StatusCode.SC_NOT_IMPLEMENTED.value: ('구현되지 않음', 'not implemented'),
            StatusCode.SC_ZERO_BYTE.value: ('대상이 0바이트임', 'zero byte'),
            StatusCode.SC_ERR_MOVE_PARENT_TO_CHILD_NODE.value: ('부모노드를 자식노드로 이동오류', ''),
            StatusCode.SC_FOUND_SAME_PROJECT_NAME.value: ('동일 프로젝트 이름 존재', 'same project name found'),
            StatusCode.SC_FOUND_SAME_SHARE_NAME.value: ('동일 공유이름 존재', 'same sharing name found'),
            StatusCode.SC_ERR_MOVE_SAME_NODE.value: ('같은노드에이동시오류', ''),
            StatusCode.SC_JOB_ALREADY_FINISHED.value: ('이미완료된작업', ''),
            StatusCode.SC_JOB_IN_PROGRESS.value: ('진행중인작업', ''),
            StatusCode.SC_ERR_GET_FILE_PROP.value: ('파일속성조회실패', ''),
            StatusCode.SC_ERR_GET_NODE_PROP.value: ('노드속성조회실패', ''),
            StatusCode.SC_FOUND_SAME_NODE_SHARE.value: ('동일노드공유생성오류', ''),
            StatusCode.SC_SQL_ERROR.value: ('SQL 오류', 'SQL error'),
            StatusCode.SC_DB_ERROR.value: ('DB 오류', 'DB error'),
            StatusCode.SC_SQL_NO_APPLIED.value: ('적용된 데이터 없음', 'not applied'),
            StatusCode.SC_UNSUPPORTED_DB.value: ('지원하지 않는 데이터베이스', 'unsupported database'),
            StatusCode.SC_VC_ENGINE_UNAVAILABLE.value: ('백신 엔진 오류', 'unavailable vaccine engine'),
            StatusCode.SC_INTERNAL_ERROR.value: ('서버 내부 오류', 'internal server error'),
            StatusCode.SC_ERR_MODIFY_SYSTEM_CONFIG.value: ('시스템에 의해 설정된 값은 변경할 수 없습니다.', 'system configuration not modifed'),
            StatusCode.SC_FOUND_LOCK_NODE.value: ('잠금노드 존재', 'locked node found'),
            StatusCode.SC_ERR_FOLDER_PWD_ALREADY_EXIST.value: ('폴더패스워드가기존재함', ''),
            StatusCode.SC_ERR_FOLDER_PWD_NOT_FOUND.value: ('폴더패스워드가없음', ''),
            StatusCode.SC_ERR_FOLDER_PWD_NOT_MATCHED.value: ('폴더패스워드가일치하지않음', ''),
            StatusCode.SC_ERR_NO_NODE_AVAILABLE.value: ('본문검색노드를찾을수없음', ''),
            StatusCode.SC_ERR_CREATE_CI_INDEX.value: ('본문검색인덱싱생성에러', ''),
            StatusCode.SC_ERR_EXCLUDE_CI_FORMAT.value: ('본문검색인덱싱대상이아님', ''),
            StatusCode.SC_ERR_DELETE_CI_INDEX.value: ('본문검색인덱스삭제에러', ''),
            StatusCode.SC_ERR_SEARCH_CI_INDEX.value: ('본문검색인덱스조회에러', ''),
            StatusCode.SC_LDAP_CONNECT_ERROR.value: ('LDAP연결오류', ''),
            StatusCode.SC_ZIP_DOWNLOAD_TOTAL_LIMIT_SIZE.value: ('다중파일압축다운로드전체사이즈제한초과오류', ''),
            StatusCode.SC_ZIP_DOWNLOAD_FILE_LIMIT_SIZE.value: ('다중파일압축다운로드파일사이즈제한초과오류', ''),
            StatusCode.SC_ERR_ZIP_DOWNLOAD_SIZE_LIMIT.value: ('다중파일압축다운로드파일사이즈제한초과오류', ''),
            StatusCode.SC_USAGE_MAX_CHECK_EXCEED.value: ('설정용량최대값초과', ''),
            StatusCode.CS_FAIL_LOAD_META_DAT.value: ('메타데이터로드실패(C)', ''),
            StatusCode.CS_FAIL_LOAD_VOL_SIZE.value: ('볼륨크기로드실패(C)', ''),
            StatusCode.CS_ENCRYPT_INIT_ERROR.value: ('암호화모듈초기화실패(C)', ''),
            StatusCode.CS_ENCRYPT_ERROR.value: ('암호화오류(C)', ''),
            StatusCode.CS_DECRYPT_INIT_ERROR.value: ('복호화모듈초기화실패(C)', ''),
            StatusCode.CS_DECRYPT_ERROR.value: ('복호화오류(C)', 'decryption error'),
            StatusCode.CS_OPEN_READONLY.value: ('읽기전용으로열기(C)', ''),
            StatusCode.CS_UNSUPPORTED_ZIP_MODE.value: ('지원하지않는압축모드(C)', ''),
            StatusCode.CS_UNSUPPORTED_ENC_MODE.value: ('지원하지않는암호화모드(C)', ''),
            StatusCode.CS_FAIL_INSERT_DEFERRED_UPLOAD.value: ('지연업로드정보생성실패(C)', ''),
            StatusCode.CS_NOT_CREATE_FILE.value: ('파일생성오류(C)', ''),
            StatusCode.CS_SYSTEM_FOLDER.value: ('시스템폴더(C)', ''),
            StatusCode.CS_ERR_DECODE_JSON.value: ('JSON디코딩오류(C)', ''),
            StatusCode.CS_ERR_INVALID_HANDLE.value: ('잘못된핸들(C)', ''),
            StatusCode.SC_AUTH_ACCESS.value: ('해당권한이없습니다.', ''),
            StatusCode.SC_WRONG_ACCESS.value: ('잘못된 접근', 'invalid access'),
            StatusCode.SC_LINK_DELETE_INFO.value: ('삭제된링크정보', ''),
            StatusCode.SC_LINK_EXCEED_DAY.value: ('링크설정날짜초과', ''),
            StatusCode.SC_LINK_EXCEED_DOWN.value: ('링크다운횟수초과', ''),
            StatusCode.SC_LINK_DELETE_ITEM_INFO.value: ('삭제된링크아이이템정보', ''),
            StatusCode.SC_LINK_INPUT_PW.value: ('링크패스워드입력', ''),
            StatusCode.SC_LINK_NOT_FOUND_INFO.value: ('링크정보를찾을수없음', ''),
            StatusCode.SC_LINK_WRONG_PW.value: ('링크패스워드틀림', ''),
            StatusCode.SC_FOUND_SUB_PUB.value: ('하위폴더에공유가존재함', ''),
            StatusCode.SC_FOUND_PARENT_PUB.value: ('상위폴더에공유가존재함', ''),
            StatusCode.SC_PUB_NOT_FOUND_INFO.value: ('공유정보를찾지못함', ''),
            StatusCode.SC_PUB_DELETE_INFO.value: ('삭제된공유정보', ''),
            StatusCode.SC_PUB_EXCEED_DAY.value: ('공유날짜초과', ''),
            StatusCode.SC_PUB_INPUT_PW.value: ('공유패스워드입력', ''),
            StatusCode.SC_PUB_WRONG_PW.value: ('공유패스워드틀림', ''),
            StatusCode.SC_PUB_DELETE_ITEM_INFO.value: ('공유아이템정보를찾을수없음.', ''),
            StatusCode.SC_GUEST_SAME_ID.value: ('동일할게스트아이디존재.', ''),
            StatusCode.SC_NOT_FOUND_GUEST_INFO.value: ('게스트정보를찾을수없습니다.', ''),
            StatusCode.SC_ALREADY_BATCH_JOB_INFO.value: ('이미진행중인작업이있습니다.', ''),
            StatusCode.SC_JOB_WATING.value: ('작업이대기입니다.', ''),
            StatusCode.SC_JOB_RUNNING.value: ('작업이수행중입니다.', ''),
            StatusCode.SC_JOB_FINISHED.value: ('작업이완료되었습니다.', ''),
            StatusCode.SC_JOB_ERROR.value: ('작업이오류상태입니다.', ''),
            StatusCode.SC_JOB_CANCELED.value: ('작업이오류상태입니다.', ''),
            StatusCode.SC_PROJECT_FULL_MEMBER.value: ('프로젝트멤버가모두다찾습니다.', ''),
            StatusCode.SC_PROJECT_INPUT_PW.value: ('프로젝트패스워드를입력.', ''),
            StatusCode.SC_PROJECT_WRONG_PW.value: ('프로젝트패스워드를틀림.', ''),
            StatusCode.SC_PROJECT_MEMBER_GROUP_NO_OUT.value: ('프로젝트그룹으로가입되어있어탈퇴불가합니다.', ''),
            StatusCode.SC_PROJECT_ALREADY_ADD.value: ('프로젝트그룹으로이미추가된사용자입니다.', ''),
            StatusCode.SC_POLICY_CHECK_PW.value: ('정책에맞지않는비밀번호', ''),
            StatusCode.SC_ERR_DRM_DOWNLOAD.value: ('DRM다운로드시DRM안걸려있으면나는에러', ''),
            StatusCode.SC_APRVL_AUTH_ACCESS.value: ('결재권한이없거나결재자기한이초과되었습니다.', ''),
        };
    
        @staticmethod
        def getBrief(code, lang='ko'):
            brief = '';
            msgList = MMessage.briefMsgDict[code];
            if msgList != None:
                if lang == 'ko':
                    msg = msgList[0];    
                else:
                    msg = msgList[1];        
            return msg;
            
