/**************************************************************
 *
 *  이 프로그램은 (주)사이냅소프트의 자산입니다.
 *  (주)사이냅소프트의 서면 동의없이 복제하거나
 *  부분 도용할 수 없습니다.
 *
 *  Revisions:
 *
 *  2003/12/01 (version 3.0) Allen
 *  2001/04/22 (version 2.0) Allen
 *  2000/08/25 (version 1.0) Allen
 *
 *  to do list :
 *
 *
 **************************************************************/

/**************************************************************
 * Include Headers
 **************************************************************/

/**************************************************************
 * Local Definitions
 **************************************************************/
 
 /**************************************************************
 * Local ERROR Definitions
 **************************************************************/

// MFI ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief SN3MFI 구조체를 위한 메모리 할당 실패 
*/
#define ERROR_SN3MFI_FOPEN_RW_MFI_MALLOC_FAILURE	10501 
/** @brief 파일 메모리가 NULL이거나 메모리 크기가 0 이하임 
*/
#define	ERROR_SN3MFI_FOPEN_M_NULL_MEMFILE			10502 
/** @brief SN3MFI 구조체를 위한 메모리 할당 실패 
*/
#define	ERROR_SN3MFI_FOPEN_M_MFI_MALLOC_FAILURE		10503 
/** @brief FILE 포인터가 NULL이거나 파일의 크기가 0 이하임 
*/
#define	ERROR_SN3MFI_FOPEN_F_NULL_FILE				10504 
/** @brief FILE의 내용을 읽기 위한 FILE 크기 만큼의 메모리 할당 실패 
*/
#define	ERROR_SN3MFI_FOPEN_F_FILE_MALLOC_FAILURE	10505 
/** @brief FILE의 내용을 읽기 위한 FILE 크기 만큼의 메모리 할당 실패 
*/
#define	ERROR_SN3MFI_FOPEN_F_MFI_MALLOC_FAILURE		10506 
/** @brief FILE 내용 읽기 실패 */
#define	ERROR_SN3MFI_FOPEN_F_FREAD_FAILURE			10507 

/** @brief FILE의 경로 문자열이 NULL 
*/
#define	ERROR_SN3MFI_FOPEN_NULL_FILEPATH			10508 
/** @brief FILE의 크기가 0 
*/
#define	ERROR_SN3MFI_FOPEN_FILE_SIZE_ZERO			10509 
/** @brief FILE 읽기 권한이 없음 
*/
#define	ERROR_SN3MFI_FOPEN_NO_READ_ACCESS			10510 
/** @brief FILE 정보 읽기 오류(STAT 실패) 
*/
#define	ERROR_SN3MFI_FOPEN_READING_FILE_STAT		10511 
/** @brief FILE의 내용을 읽기 위한 FILE 크기 만큼의 메모리 할당 실패 
*/
#define	ERROR_SN3MFI_FOPEN_FILE_MALLOC_FAILURE		10512 
/** @brief FILE 열기 실패 
*/
#define	ERROR_SN3MFI_FOPEN_FILE_OPEN_FAILURE		10513 
/** @brief FILE 내용 읽기 실패 
*/
#define	ERROR_SN3MFI_FOPEN_FILE_READ_FAILURE		10514 
/** @brief SN3MFI 구조체를 위한 메모리 할당 실패 
*/
#define	ERROR_SN3MFI_FOPEN_MFI_MALLOC_FAILURE		10515 

/** @brief SN3MFI 가 NULL 
*/
#define	ERROR_SN3MFI_FCLOSE_NULL_MFI				10516 

/** @brief SN3MFI 파일 위치 이동 중 SN3MFI 가 NULL 
*/
#define	ERROR_SN3MFI_FSEEK_NULL_FILE				10517 

/** @brief SN3MFI 파일 위치 이동 중 잘못된 방향 옵션 설정 
*/
#define	ERROR_SN3MFI_FSEEK_BAD_ORIGIN				10519 

/** @brief SN3MFI의 내용을 FILE에 쓰기 실패 
*/
#define	ERROR_SN3MFI_UNLOAD_F_FWRITE_FAILURE		10520 
/** @brief SN3MFI의 내용을 쓰기 위한 FILE 열기 실패 
*/
#define	ERROR_SN3MFI_UNLOAD_FILE_OPEN_FAILURE		10521 
/** @brief SN3MFI 복제시 NULL 오류.
*/
#define	ERROR_SN3MFI_FCOPY_NULL_ERROR		10522 
/** @brief SN3MFI 복제 실패.
*/
#define	ERROR_SN3MFI_FCOPY_WRITE_ERROR		10523 
/** @brief SN3MFI 초기화 되지 않은 MFI 사용.
*/
#define	ERROR_SN3MFI_UNINITIALIZED_ERROR		10524 

// SN3BUF ERROR //////////////////////////////////////////////////////////////////////////

/** @brief SN3BUF 메모리 할당 초기화 실패
*/
#define	ERROR_SN3BUF_INIT_BUFFER_MEMORY_ALLOCATION_FAILURE	10601

/** @brief SN3BUF가 NULL일 때 메모리를 해제하는 경우
*/
#define	ERROR_SN3BUF_FREE_BUFFER_IS_NULL			10602

/** @brief SN3BUF에 있는 내용을 파일로 쓰기위한 파일 열기 실패
*/
#define	ERROR_SN3BUF_UNLOAD_FILE_OPEN_FAILURE			10603

/** @brief NULL인 SN3BUF에 UCS2 문자를 버퍼에 넣으려고 할때 오류
*/
#define	ERROR_SN3BUF_PUTC_UCS2_BUFFER_IS_NULL			10604
/** @brief SN3BUF 메모리 재할당 실패
*/
#define	ERROR_SN3BUF_PUTC_UCS2_BUFFER_REALLOCATION_FAILURE	10605

/** @brief NULL인 SN3BUF에 UCS2 문자열을 버퍼에 넣으려고 할때 오류
*/
#define	ERROR_SN3BUF_PUTS_UCS2_BUFFER_IS_NULL			10607
/** @brief NULL인 문자열을 SN3BUF에 넣으려고 할때 오류
*/
#define	ERROR_SN3BUF_PUTS_UCS2_INPUT_IS_NULL			10608

/** @brief SN3BUF 포인터가 NULL인 경우
*/
#define	ERROR_SN3BUF_BUFFER_IS_NULL			10609

/** @brief 임시로 사용할 UCS2 문자열을 할당 실패
*/
#define	ERROR_SN3BUF_PUTS_CP949_TMPOUTPUT_ALLOCATION_FAILURE	10611
/** @brief CP949 문자열을 SN3BUF에 기록 중 포인터가 문자열을 넘어감
*/
#define	ERROR_SN3BUF_PUTS_CP949_OOPS_OUTPUT_OVERRUN		10612

/** @brief SN3BUF 앞쪽에 UCS2-LE 문자를 넣을 때 SN3BUF의 시작포인트가 0보다 작은 경우
*/
#define	ERROR_SN3BUF_UNGETWCH_FAILURE				10613

/** @brief UTF8 텍스트를 SN3BUF에 기록 중 임시로 사용할 UCS2 메모리 할당 실패 
*/
#define	ERROR_SN3BUF_PUTS_UTF8_TMPOUTPUT_ALLOCATION_FAILURE	10614 
/** @brief UTF8 텍스트를 SN3BUF에 기록 중 임시로 사용되는 UCS2 메모리 부족 
*/
#define	ERROR_SN3BUF_PUTS_UTF8_OOPS_OUTPUT_OVERRUN		10615 


// OPENFILE ERROR  //////////////////////////////////////////////////////////////////////////

/** @brief OLE 파일 사이즈가 512 byte 의 배수가 아닌 경우
*/
#define ERROR_SN3OLE_ISOLE_BAD_FILE_SIZE			10726

/** @brief OLE 파일 헤더가 정상적이지 않은 경우
*/
#define ERROR_SN3OLE_ISOLE_FREAD_HEADER_FAILURE		10728
/** @brief OLE 파일 헤더는 정상적이나 OLE ID 가 비정상인 경우
*/
#define ERROR_SN3OLE_ISOLE_BAD_OLE_ID				10729

/** @brief OLE 추출 실패(BBD ROOT CHAIN 의 시작점이 비정상인 경우)
*/
#define ERROR_SN3OLE_MOUNT2_BAD_ROOT_CHAIN_START		10734

/** @brief OLE 추출 실패(SBD 의 시작점이 비정상인 경우)
*/
#define ERROR_SN3OLE_MOUNT2_BAD_SBD_STARTBLOCK			10735

/** @brief BBD LIST 구성시 메모리 부족 발생
*/
#define ERROR_SN3OLE_MOUNT2_MALLOC_BBD_LIST_FAILURE		10736

/** @brief ROOT CHAIN 구성시 메모리 부족 발생
*/
#define ERROR_SN3OLE_MOUNT2_MALLOC_ROOT_CHAIN_FAILURE	10737

/** @brief SBD CHAIN 구성시 메모리 부족 발생
*/
#define ERROR_SN3OLE_MOUNT2_MALLOC_SBD_CHAIN_FAILURE	10738

/** @brief OLE 추출 실패(BBD LIST 가 비정상인 경우)
*/
#define ERROR_SN3OLE_MOUNT2_BAD_BBD_LIST				10739

/** @brief OLE 추출 실패(BBD CHAIN 이 비정상인 경우)
*/
#define ERROR_SN3OLE_MOUNT2_BAD_ROOT_CHAIN				10740

/** @brief SBD CHAIN 이 비정상인 경우
*/
#define	ERROR_SN3OLE_MOUNT2_BAD_SBD_CHAIN				10741

/** @brief OLE 추출 실패(MOUNT시 ROOT 를 찾지 못 하는 경우)
*/
#define	ERROR_SN3OLE_MOUNT2_OPEN_ROOT_FAILURE			10743

/** @brief BBD 의 다음 블럭이 비정상인 경우
*/
#define	ERROR_SN3OLE_MOUNT2_BAD_BBD_NEXTBLOCK			10744

/** @brief UMOUNT 시 포인터가 잘못 된 경우
*/
#define ERROR_SN3OLE_UMOUNT_NULL_FILE_SYSTEM			10745

/** @brief Block 주소의 NULL Pointer 에러
*/
#define	ERROR_SN3OLE_BLOCKADDR_NULL_FILE_SYSTEM			10747

/** @brief Block 주소와 BLOCK 개수가 일치 하지 않는 경우
*/
#define ERROR_SN3OLE_BLOCKADDR_BAD_BLOCK_NUMBER			10748

/** @brief ROOT Stroage Open 시에 NULL Pointer 에러
*/
#define ERROR_SN3OLE_OPENROOT_NULL_FILE_SYSTEM			10749

/** @brief ROOT Stroage Open 시에 NULL Pointer 에러
*/
#define ERROR_SN3OLE_OPENROOT_NULL_ROOT_DIR				10750

/** @brief ROOT PPS 가 비정상인 경우
*/
#define	ERROR_SN3OLE_OPENROOT_BAD_ROOT_PPS				10751

/** @brief ROOT DIR Open 시 메모리 부족
*/
#define	ERROR_SN3OLE_OPENROOT_MALLOC_ROOT_DIR_FAILURE	10752

/** @brief PPS 를 읽을 때 NULL Pointer 에러
*/
#define	ERROR_SN3OLE_READPPS_NULL_PPS_BASE				10753

/** @brief PPS 를 읽을 때 NULL Pointer 에러
*/
#define	ERROR_SN3OLE_READPPS_NULL_PPS					10754

/** @brief PPS Block이 비정상인 경우
*/
#define	ERROR_SN3OLE_READPPS_BROKEN_PPS_BLOCK			10755

/** @brief DIRPPS 의 Prev PPS 가 비정상인 경우
*/
#define	ERROR_SN3OLE_DIRPPS_BAD_PPS_PREV				10757

/** @brief DIRPPS 의 Next PPS 가 비정상인 경우
*/
#define	ERROR_SN3OLE_DIRPPS_BAD_PPS_NEXT				10758

/** @brief DIRPPS 에서 File System 접근시 NULL Pointer 에러
*/
#define	ERROR_SN3OLE_DIRPPS_NULL_FILE_SYSTEM			10759

/** @brief DIRPPS 에서 Directory 접근시 NULL Pointer 에러
*/
#define	ERROR_SN3OLE_DIRPPS_NULL_DIRECTORY				10760

/** @brief DIRPPS 에서 PPS Index 나 PPS Level 이 비정상인 경우
*/
#define	ERROR_SN3OLE_DIRPPS_BAD_PPS_INDEX_OR_LEVEL		10761


/** @brief Openfile 에서 File System 접근시  NULL Pointer 에러
*/
#define	ERROR_SN3OLE_FOPEN_NULL_FILE_SYSTEM				10768

/** @brief Openfile 에서 현재 Directory 접근시 NULL Pointer 에러
*/
#define	ERROR_SN3OLE_FOPEN_NULL_CURRENT_DIR				10769

/** @brief Openfile 에서 입력받은 file 명이 NULL 인 경우
*/
#define	ERROR_SN3OLE_FOPEN_NULL_FILE_NAME				10770

/** @brief Openfile 에서 Open 한 파일이 NULL 인 경우
*/
#define	ERROR_SN3OLE_FOPEN_NULL_FILE					10771

/** @brief Openfile 에서 File 을 찾지 못 하는 경우
*/
#define	ERROR_SN3OLE_FOPEN_NO_SUCH_FILE_NAME			10772

/** @brief Openfile 에서 메모리 부족 발생
*/
#define	ERROR_SN3OLE_FOPEN_MALLOC_BLOCK_CHAIN_FAILURE		10773

/** @brief Openfile 에서 Block chain 이 비정상인 경우
*/
#define	ERROR_SN3OLE_FOPEN_BAD_BLOCK_CHAIN					10774

/** @brief Openfile 에서 메모리 부족 발생
*/
#define	ERROR_SN3OLE_FOPEN_MALLOC_FILE_FAILURE				10775

/** @brief User DocInfo 에서 Stream Buffer 구성시 메모리 부족
*/
#define	ERROR_SN3OLE_USER_DOCINFO_FS_MALLOC_STREAM_BUFFER_FAILURE	10821

// TXT ERROR /////////////////////////////////////////////////////////////////////////////
/** @brief TXT 포맷 필터링 시 메모리 할당 실패
*/
#define	ERROR_SN3TXT_MEMORY_ALLOC_FAILURE	20000

// PDF ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief 일반적인 PDF 파일 오류
*/
#define ERROR_SN3PDF								31100
/** @brief PDF 파일의 Stream Object 생성 실패
*/
#define	ERROR_SN3PDF_OPEN_INPUT_STREAM				31101
/** @brief PDF 파일의 Stream Object 에서 읽을 수 없는 경우 발생
*/
#define	ERROR_SN3PDF_NO_INPUT_STREAM				31102
/** @brief PDF 파일의 Header 정보를 읽지 못 한 경우 발생
*/
#define	ERROR_SN3PDF_ERROR_READING_PDF_HEADER		31103
/** @brief PDF 파일의 Xref 의 시작점을 찾지 못 함
*/
#define	ERROR_SN3PDF_READING_XREF_START				31104
/** @brief PDF 파일의 Xref 를 읽는 도중 에러 발생
*/
#define	ERROR_SN3PDF_READING_XREF					31105
/** @brief PDF 파일의 Page Catalog 정보를 읽지 못 함
*/
#define	ERROR_SN3PDF_PAGE_READING_CATALOG			31106
/** @brief PDF 파일의 Page Reference 정보를 읽지 못 함
*/
#define	ERROR_SN3PDF_READING_PAGE_REF				31107
/** @brief 보안설정이 되어 있는 PDF 파일인 경우 발생
*/
#define	ERROR_SN3PDF_ENCRYPTED_PDF					31108
/** @brief PDF 문서의 Page Number 가 비정상적인 경우 발생
*/
#define	ERROR_SN3PDF_INVALID_PAGE_NUM				31109
/** @brief 메모리안의 PDF 문서의 Input Stream Object 생성 실패
*/
#define	ERROR_SN3PDF_FILTER_M_INVALID_INPUT_STREAM	31110
/** @brief PDf 문서에서 텍스트 추출 실패
*/
#define	ERROR_SN3PDF_FILTER_M_FILTERING_FAILURE		31111
/** @brief PDF 파일의 Stream Object 생성 실패
*/
#define ERROR_SN3PDF_MEMORY_ALLOC_FAILURE			31112



// MSG ERROR /////////////////////////////////////////////////////////////////////////////
/** @brief MSG 정보의 IPM.Note 가 비정상인 경우
*/ 
#define	ERROR_SN3MSG_FILTER_FS_BAD_IPM_TYPE				39101 
/** @brief MSG 의 제목 읽기 실패
*/ 
#define	ERROR_SN3MSG_FILTER_M_FREAD_TITLE_FAILURE		39102

// MP3 ERROR /////////////////////////////////////////////////////////////////////////////
/** @brief MP3 헤더 읽기 실패
*/ 
#define	ERROR_SN3MP3_FILTER_M_FREAD_HEADER_FAILURE		30901
/** @brief MP3 헤더 정보가 비정상인 경우
*/ 
#define	ERROR_SN3MP3_FILTER_M_INVALID_MP3_HEADER		30902
/** @brief MP3 의 TAG 를 읽기 실패
*/ 
#define	ERROR_SN3MP3_FILTER_M_FREAD_TAG_FAILURE			30903
/** @brief MP3 의 TAG 를 찾지 못 하는 경우
*/ 
#define	ERROR_SN3MP3_FILTER_M_NO_TAG_FOUND				30904
/** @brief MP3 의 TAG 중 제목 읽기 실패
*/ 
#define	ERROR_SN3MP3_FILTER_M_FREAD_TITLE_FAILURE		30905
/** @brief MP3 의 TAG 중 음악가 읽기 실패
*/ 
#define	ERROR_SN3MP3_FILTER_M_FREAD_ARTIST_FAILURE		30906
/** @brief MP3 의 TAG 중 앨범정보 읽기 실패
*/ 
#define	ERROR_SN3MP3_FILTER_M_FREAD_ALBUM_FAILURE		30907
/** @brief MP3 의 TAG 중 제작년도 읽기 실패
*/ 
#define	ERROR_SN3MP3_FILTER_M_FREAD_YEAR_FAILURE		30908
/** @brief MP3 의 TAG 중 주석정보 읽기 실패
*/ 
#define	ERROR_SN3MP3_FILTER_M_FREAD_COMMENTS_FAILURE	30909

/** @brief MP3 헤더 읽기 실패
*/ 
#define	ERROR_SN3MP3_DOCINFO_M_FREAD_HEADER_FAILURE		30911
/** @brief MP3 헤더 정보가 비정상인 경우
*/ 
#define	ERROR_SN3MP3_DOCINFO_M_INVALID_MP3_HEADER		30912
/** @brief MP3 의 TAG 를 읽기 실패
*/ 
#define	ERROR_SN3MP3_DOCINFO_M_FREAD_TAG_FAILURE		30913
/** @brief MP3 의 TAG 를 찾지 못 하는 경우
*/ 
#define	ERROR_SN3MP3_DOCINFO_M_NO_TAG_FOUND				30914
/** @brief MP3 의 TAG 중 제목 읽기 실패
*/ 
#define	ERROR_SN3MP3_DOCINFO_M_FREAD_TITLE_FAILURE		30915
/** @brief MP3 의 TAG 중 음악가 읽기 실패
*/ 
#define	ERROR_SN3MP3_DOCINFO_M_FREAD_ARTIST_FAILURE		30916
/** @brief MP3 의 TAG 중 앨범정보 읽기 실패
*/ 
#define	ERROR_SN3MP3_DOCINFO_M_FREAD_ALBUM_FAILURE		30917
/** @brief MP3 의 TAG 중 제작년도 읽기 실패
*/ 
#define	ERROR_SN3MP3_DOCINFO_M_FREAD_YEAR_FAILURE		30918
/** @brief MP3 의 TAG 중 주석정보 읽기 실패
*/ 
#define	ERROR_SN3MP3_DOCINFO_M_FREAD_COMMENTS_FAILURE	30919

// MHT ERROR /////////////////////////////////////////////////////////////////////////////
/** @brief MHT 파일의 헤더가 비정상인 경우
*/ 
#define ERROR_SN3MHT_FILTER_M_INVALID_HEADER		33801
/** @brief MHT 파일이 지원하지 않는 인코딩으로 되어 있는 경우
*/ 
#define ERROR_SN3MHT_FILTER_M_UNSUPPORTED_ENCODING	33802
/** @brief MHT 파일이 지원하지 않는 charset 을 갖는 경우
*/ 
#define ERROR_SN3MHT_FILTER_M_UNSUPPORTED_CHARSET	33803
/** @brief 정보를 다 읽지 못 하고 MULTIPART BOUNDARY 가 끝난 경우
*/ 
#define	ERROR_SN3MHT_FILTER_M_END_OF_MULTIPART		33804


// MDI ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief 올바른 MDI 파일이 아닌 경우
*/
#define ERROR_SN3MDI_FILTER_M_NOT_MDI_ERROR	32301
/** @brief MDI 파일 읽기 실패
*/
#define	ERROR_SN3MDI_FILTER_M_FREAD_ERROR		32302

// LZX ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief 데이터 포맷 에러 
*/
#define ERROR_SN3LZX_DATAFORMAT   65001
/** @brief 잘못된 데이터 
*/
#define ERROR_SN3LZX_ILLEGALDATA  65002
/** @brief 메모리 부족 
*/
#define ERROR_SN3LZX_NOMEMORY     65003

// JTD ERROR /////////////////////////////////////////////////////////////////////////////


/** @brief 헤더의 ID 정보가 올바르지 않는 경우 발생
*/
#define ERROR_DOCUMENT_TEXT_INVALID_HEADER_ID			56001

/** @brief 통상 보존형식 텍스트의 ID 정보가 올바르지 않는 경우 발생
*/
#define ERROR_DOCUMENT_TEXT_INVALID_RECORD_HEADER_ID	56002

/** @brief 메모리 부족
*/
#define ERROR_JTD_OUT_OF_MEMORY							56003 

/** @brief 필요한 특수 문자가 없는 경우 발생 
*/
#define ERROR_SN3JTD_ERROR_SPECIAL_DATA					56004 

// HWP3 ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief 비밀번호가 있는 HWP3 문서 필터링 시 발생 
*/
#define	ERROR_SN3HWP3_FILTER_M_PASSWORD_EXISTS				30501 
/** @brief HWP3 문서 초기화 실패 
*/
#define	ERROR_SN3HWP3_FILTER_M_INIT_HWP3_FAILURE			30502 
/** @brief HWP3 문서 열기 실패 
*/
#define	ERROR_SN3HWP3_FILTER_M_HWP3_OPEN_FAILURE			30503 

/** @brief HWP3 문서 요약정보 읽기 실패 
*/
#define	ERROR_SN3HWP3_DOCINFO_M_FREAD_HWP_ID_FAILURE		30504 
/** @brief HWP3 문서 요약정보의 잘못된 파일 헤더 
*/
#define	ERROR_SN3HWP3_DOCINFO_M_INVALID_FILE_HEADER			30505 
/** @brief HWP3 문서 잘못된 요약정보 사이즈 
*/
#define	ERROR_SN3HWP3_DOCINFO_M_INVALID_DOCINFO_SIZE		30506 
/** @brief HWP3 문서 요약정보 읽기 실패 
*/
#define	ERROR_SN3HWP3_DOCINFO_M_FREAD_HWP_SUMMARY_FAILURE	30507 
/** @brief HWP3 Style 정보를 읽는 도중 오류 발생
*/
#define	ERROR_SN3HWP3_FILTER_STYLEINFO_READ_FAILURE			30508 
/** @brief HWP3 그림객체 정보의 패러그래프를 읽는 도중 오류 발생
*/
#define	ERROR_SN3HWP3_FILTER_TEXTBOX_READ_FAILURE			30509 
/** @brief HWP3 v1.20 버전은 지원하지 않는다. (v2.0 부터 지원)
*/
#define ERROR_SN3HWP3_FILTER_V120_NO_FILTER_ASSOCIATED		30510
/** @brief GZIP 처리 중 실패
*/
#define ERROR_SN3HWP3_FILTER_GZIP_INIT						30511
/** @brief HWP3 폰트 정보를 읽는 도중 오류 발생
*/
#define ERROR_SN3HWP3_FILTER_FONTINFO_READ_FAILURE			30512
/** @brief HWP3 문단 정보를 읽는 도중 오류 발생
*/
#define ERROR_SN3HWP3_FILTER_PARALIST_READ_FAILURE			30513
/** @brief HWP3 메모리 할당 실패
*/
#define ERROR_SN3HWP3_FILTER_MALLOC_FAILURE					30514

// H2K ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief HWP 2000 요약정보의 메모리 할당 실패 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_MALLOC_STREAM_BUFFER_FAILURE	33501 
/** @brief HWP 2000 요약정보의 속성셋 메모리 할당 실패 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_MALLOC_PROPSET_FAILURE			33502 
/** @brief HWP 2000 요약정보의 잘못된 바이트 오더 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_WRONG_BYTE_ORDER				33503 
/** @brief HWP 2000 요약정보의 잘못된 포맷 버전 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_WRONG_FORMAT_VERSION			33504 
/** @brief HWP 2000 요약정보의 잘못된 OLE 운영체제종류(0:16bit Win, 1:Macintosh, 2:32bit Win)
*/
#define	ERROR_SN3H2K_DOCINFO_FS_WRONG_OS_KIND					33505 
/** @brief HWP 2000 요약정보의 잘못된 Reserved 정보 1보다 커야함 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_WRONG_RESERVED					33506 
/** @brief HWP 2000 요약정보의 잘못된 Section Offset
*/
#define	ERROR_SN3H2K_DOCINFO_FS_WRONG_SECTION_OFFSET			33507 
/** @brief HWP 2000 요약정보의 잘못된 Section Size 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_WRONG_SECTION_SIZE				33508 
/** @brief HWP 2000 요약정보의 잘못된 Section 내의 Property 개수 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_WRONG_NUM_OF_PROPS				33509 
/** @brief HWP 2000 요약정보의 잘못된 Property ID의 배열
*/
#define	ERROR_SN3H2K_DOCINFO_FS_MALLOC_PROPSET_ID_FAILURE		33510  
/** @brief HWP 2000 요약정보의 잘못된 Property Offset의 배열
*/
#define	ERROR_SN3H2K_DOCINFO_FS_MALLOC_PROPSET_OFFSET_FAILURE	33511 
/** @brief HWP 2000 요약정보의 잘못된 Property 타입 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_MALLOC_PROPSET_TYPE_FAILURE		33512 
/** @brief HWP 2000 요약정보의 잘못된 Property ID 또는 Offset 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_WRONG_PROP_ID_OR_OFFSET			33513 
/** @brief HWP 2000 요약정보의 유니코드 문자열 메모리 할당 실패 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_MALLOC_TMPWSTR_FAILURE			33514 
/** @brief HWP 2000 암호화인 경우
*/
#define	ERROR_SN3H2K_FILTER_FS_FILE_ENCRYPTED					33515 

/** @brief HWP 2000 배포용 파일인 경우
*/
#define	ERROR_SN3H2K_FILTER_FS_FILE_DISTRIBUTION				33516

/** @brief HWP 2000 레코드 정보 읽기 실패
*/
#define	ERROR_SN3H2K_FILTER_READ_RECORD							33521

/** @brief HWP 2000 문단 텍스트 정보 읽기 실패
*/
#define	ERROR_SN3H2K_FILTER_READ_PARA_TEXT						33522

/** @brief HWP 2000 문단 글자정보 읽기 실패
*/
#define	ERROR_SN3H2K_FILTER_READ_PARA_CHARSHAPE					33523

/** @brief HWP 2000 구역 정보 읽기 실패
*/
#define	ERROR_SN3H2K_FILTER_READ_SECTION						33524

/** @brief HWP 2000 GZIP 초기화 실패
*/
#define	ERROR_SN3H2K_FILTER_GZIP_INIT							33525

/** @brief HWP 2000 문단헤더 메모리 할당 실패
*/
#define	ERROR_SN3H2K_FILTER_PARAREADER_INIT_MEMORY_ALLOCATION	33526

/** @brief HWP 2000 글자정보 메모리 할당 실패
*/
#define	ERROR_SN3H2K_FILTER_CHAROBJECT_INIT_MEMORY_ALLOCATION	33527

/** @brief HWP 2000 도형정보 메모리 할당 실패
*/
#define	ERROR_SN3H2K_FILTER_SHAPEOBJECT_INIT_MEMORY_ALLOCATION	33528

/** @brief HWP 2000 배포용 문서 헤더 형식 오류.
*/
#define ERROR_SN3H2K_FILTER_READONLY_GZIP_BAD_HEADER			33529

/** @brief HWP 2000 배포용 문서 DecryptGZIP 초기화 실패
 */
#define ERROR_SN3H2K_FILTER_READONLY_GZIP_INIT					33530

/** @brief HWP 2000 문단 리스트 헤더 오류
 */
#define ERROR_SN3H2K_FILTER_READ_LIST_HEADER					33531

// by Ummi 2012.05.23
/** @brief HWP 2000 사용자 지정 정보의 메모리 할당 실패 
*/
#define	ERROR_SN3H2K_USER_DOCINFO_FS_MALLOC_STREAM_BUFFER_FAILURE	33551 
/** @brief HWP 2000 사용자 지정 정보의 속성셋 메모리 할당 실패 
*/
#define	ERROR_SN3H2K_USER_DOCINFO_FS_MALLOC_PROPSET_FAILURE			33552 
/** @brief HWP 2000 사용자 지정 정보의 잘못된 바이트 오더 
*/
#define	ERROR_SN3H2K_USER_DOCINFO_FS_WRONG_BYTE_ORDER				33553 
/** @brief HWP 2000 사용자 지정 정보의 잘못된 Property Sets 
*/
#define ERROR_SN3H2K_USER_DOCINFO_FS_WRONG_NUM_PROPERTY_SETS		33554
/** @brief HWP 2000 사용자 지정 정보의 잘못된 Property ID의 배열
*/
#define	ERROR_SN3H2K_USER_DOCINFO_FS_MALLOC_PROPSET_ID_FAILURE		33555 
/** @brief HWP 2000 사용자 지정 정보의 잘못된 Property Offset의 배열
*/
#define	ERROR_SN3H2K_USER_DOCINFO_FS_MALLOC_PROPSET_OFFSET_FAILURE	33556 
/** @brief HWP 2000 블록 정보 읽기 실패
*/
#define ERROR_SN3H2K_FILTER_WRONG_BLOCK_SIZE 33557
/** @brief HWP 2000 유효하지 않은 레코드 헤더
 */
#define ERROR_SN3H2K_FILTER_INVALID_RECORD_HEADER					33558

// GZ ERROR //////////////////////////////////////////////////////////////////////////////

/** @brief GZ 파일의 잘못된 헤더 정보 
*/
#define	ERROR_SN3GZ_FILTER_M_FREAD_LOC_HEADER_FAILURE		33701 
/** @brief GZ 파일의 잘못된 파일 시그니처
*/
#define	ERROR_SN3GZ_FILTER_M_INVALID_FILE_SIGNATURE			33702 
/** @brief GZ 파일의 잘못된 파일 사이즈
*/
#define	ERROR_SN3GZ_FILTER_M_INVALID_FILE_LENGTH			33703 
/** @brief Deprecated
*/
#define	ERROR_SN3GZ_FILTER_M_FREAD_GZ_NAME_FAILURE			33704 
/** @brief Deprecated
*/
#define	ERROR_SN3GZ_FILTER_M_INVALID_COMPRESSED_LENGTH		33705 

/** @brief GZ 파일의 잘못된 헤더 정보를 오픈할 때 발생
*/
#define	ERROR_SN3GZ_FOPEN_M_INVALID_GZ_HEADER				33710 
/** @brief GZ 파일을 오픈할 때 MFI가 NULL이 발생하는 경우
*/
#define	ERROR_SN3GZ_FOPEN_M_NULL_MFI						33711 
/** @brief GZ 파일을 오픈할 때 파일 읽기에 실패하는 경우
*/
#define	ERROR_SN3GZ_FOPEN_M_FREAD_FAILURE					33712 
/** @brief GZ 파일을 오픈할 때 메모리 할당 오류
*/
#define	ERROR_SN3GZ_FOPEN_M_MALLOC_ZFILE_FAILURE			33713 
/** @brief GZ 파일을 오픈할 때 시그니처를 찾지 못한 경우
*/
#define	ERROR_SN3GZ_FOPEN_M_INVALID_SIGNATURE				33714 
/** @brief GZ 파일 처리 중 파일의 끝에 도달함 
*/
#define	ERROR_SN3GZ_FOPEN_M_END_OF_FILELIST					33717 
/** @brief GZ 파일 처리중 메모리 할당 오류
*/
#define	ERROR_SN3GZ_MEMORY_ALLOC_FAILURE					33718

/** @brief GZ 파일 닫기 중 SN3GZ_FILE이 NULL 
*/
#define	ERROR_SN3GZ_FCLOSE_NULL_ZFILE						33721 

/** @brief GZ 지원되지 않는 압축형식(ZIP 압축 방식이 STORED 혹은 DEFLATED 이 아님)
*/
#define	ERROR_SN3GZ_UNZIP_M_NOT_SUPPORTED_COMPRESSION		33731 
/** @brief GZ 압축해제를 위한 메모리 할당 실패
*/
#define	ERROR_SN3GZ_UNZIP_M_UNCOMPRESSED_MALLOC_FAILURE		33732 
/** @brief STORED 형식의 GZ 내용을 SN3MFI로부터 읽기 실패
*/
#define	ERROR_SN3GZ_UNZIP_M_STORED_DATA_FREAD_FAILURE		33733 
/** @brief STORED 형식의 GZ 내용을 SN3MFI로 쓰기 실패
*/
#define	ERROR_SN3GZ_UNZIP_M_STORED_DATA_FWRITE_FAILURE		33734 
/** @brief DEFLATED 형식의 GZ 내용을 SN3MFI로 쓰기 실패
*/
#define	ERROR_SN3GZ_UNZIP_M_DEFLATED_DATA_ZWRITE_FAILURE	33737 
/** @brief GZ 파일 닫기 실패
*/
#define	ERROR_SN3GZ_UNZIP_M_GGZ_ZCLOSE_FAILURE				33738 
/** @brief 
*/
#define	ERROR_SN3GZ_UNZIP_M_IMPOSSIBLE_PATH_FLOW			33739 

/** @brief crc32 오류
*/
#define	ERROR_SN3GZ_UNZIP_M_CRC32							33740 

// GUL ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief 훈민정음 파일은 아직 구현되지 않음 
*/
#define	ERROR_SN3GUL_FILTER_FS_NOT_IMPLEMENTED_YET	33401 

// FLT ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief 필터링을 지원하지 않는 파일인 경우
*/
#define	ERROR_SN3FLT_FILTER_M_NO_FILTER_ASSOCIATED	40101

/** @brief 필터링을 지원하지 않는 파일의 요약정보를 가져올 경우
*/
#define	ERROR_SN3FLT_DOCINFO_M_NO_FILTER_ASSOCIATED	40102

/** @brief RAR 분할 압축 파일은 지원하지 않는다.
*/
#define	ERROR_SN3RAR_SPLIT_COMPRESSED_FILE 40103

/** @brief 필터링시 메모리 할당 실패
*/
#define	ERROR_SN3FLT_MEMORY_ALLOC_FAILUER 40105

// DWG ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief 파일 사이즈가 최소 사이즈보다 작음 (0x19)
*/
#define ERROR_SN3DWG_FILTER_M_BAD_FILESIZE		31001
/** @brief 메모리 할당 실패
*/
#define ERROR_SN3DWG_FILTER_M_MALLOC_FAILURE	31002

/** @brief DWG 헤더정보 읽기 실패
*/
#define ERROR_SN3DWG_HEADER					31010

/** @brief DWG 파일의 지원하지 않는 버전 정보
*/
#define ERROR_SN3DWG_HEADER_VERSION_UNKNOWN		31011
/** @brief 블락 데이터 사이즈가 파일 사이즈보다 큰 경우
*/
#define ERROR_SN3DWG_HEADER_BAD_ENTBLOCK		31033
/** @brief 잘못된 섹션 지시번호
*/
#define ERROR_SN3DWG_HEADER_BAD_SECLOC			31013
/** @brief 잘못된 섹션의 마지막 위치정보
*/
#define ERROR_SN3DWG_HEADER_BAD_SENTINEL		31014
/** @brief 잘못된 파일 사이즈
*/
#define ERROR_SN3DWG_HEADER_BAD_FILESIZE		31015
/** @brief 잘못된 R18 영역
*/
#define ERROR_SN3DWG_HEADER_BAD_R18FILEID		31016
/** @brief 섹션정보 압축해제를 위한 메모리 할당 실패
*/
#define ERROR_SN3DWG_HEADER_MALLOC_FAILURE		31017

/** @brief 잘못된 R18 섹션 맵 헤더
*/
#define ERROR_SN3DWG_R18_BAD_SECTMAP			31021
/** @brief 잘못된 R18 섹션 정보 헤더
*/
#define ERROR_SN3DWG_R18_BAD_SECTINFO			31022
/** @brief 잘못된 R18 NumSectDesc 정보
*/
#define ERROR_SN3DWG_R18_BAD_SECTDESC			31023
/** @brief 섹션 메모리 할당 실패
*/
#define ERROR_SN3DWG_SECT_MALLOC_FAILURE		31024
/** @brief Deprecated
*/
#define ERROR_SN3DWG_R18_BAD_NORMSECT			31025
/** @brief R18 섹션 이름을 찾지 못함
*/
#define ERROR_SN3DWG_R18_NO_SECTNAME			31026
/** @brief R18 섹션 버퍼를 찾지 못함
*/
#define ERROR_SN3DWG_R18_NO_SECTBUF				31027
/** @brief R18의 잘못된 압축 사이즈
*/
#define ERROR_SN3DWG_R18_DECOMP_FAILURE			31028
/** @brief 잘못된 R18 Summary Info
*/
#define ERROR_SN3DWG_R18_BAD_SUMMARY			31029

/** @brief 잘못된 CRC
*/
#define ERROR_SN3DWG_BAD_CRC					31030

/** @brief 잘못된 DWG R1315 Object
*/
#define ERROR_SN3DWG_BAD_OBJECTS				31031

/** @brief 잘못된 DWG R1315 Object
*/
#define ERROR_SN3DWG_BAD_OBJECT_SIZE			31032


/** @brief 잘못된 DWG R2004 섹션데이터
*/
#define ERROR_SN3DWG_BAD_SECTION			31034

// DOCX ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief 압축 해제된 파일을 위한 SN3MFI 열기 실패
*/
#define ERROR_SN3DOCX_CANNOT_OPEN_UNZIPFILE	46001
/** @brief DOCX 파일로부터 압축 해제된 파일 열기 실패
*/
#define ERROR_SN3DOCX_CANNOT_ARCHIVE_ZIP	46002
/** @brief DOCX 파일로부터 압축 해제된 XML파일 파싱시 오류 발생
*/
#define ERROR_SN3DOCX_CANNOT_PARSE_XML		46003
/** @brief DOCX 파일 내부의 매크로 필터링 실패
*/
#define ERROR_SN3DOCX_CANNOT_OVBA_MACRO_PARSE  46004

// DOC ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief FIB 정보를 읽는 도중 오류 발생
*/
#define	ERROR_SN3DOC_FILTER_FS_FIB_READ_FAILURE		30101
/** @brief 지원하지 않는 Word 버전
*/
#define	ERROR_SN3DOC_FILTER_FS_BAD_WORD_VERSION		30102
/** @brief 암호화된 DOC 파일
*/
#define ERROR_SN3DOC_FILTER_FS_FILE_ENCRYPTED		30103
/** @brief DOC 파일 필터링 시 메모리 할당 실패
*/
#define ERROR_SN3DOC_FILTER_MALLOC_FAILURE		30104


// CHM ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief CHM 파일을 위한 SN3MFI 열기 실패
*/
#define ERROR_SN3CHM_CANNOT_OPEN_CHMFILE			31304

/** @brief malloc fail
*/
#define ERROR_SN3CHM_FILTER_MALLOC_FAILURE					31323

// ZIP ERROR /////////////////////////////////////////////////////////////////////////////
/** @brief 
*/
#define	ERROR_SN3ZIP_FILTER_M_INVALID_COMPRESSED_LENGTH	35005 
/** @brief ZIP 파일 열기 시 SN3MFI가 NULL 
*/
#define	ERROR_SN3ZIP_FOPEN_M_NULL_MFI			35011 
/** @brief SN3MFI로 부터 파일의 내용 읽기 실패 
*/
#define	ERROR_SN3ZIP_FOPEN_M_FREAD_FAILURE		35012
/** @brief SN3ZIP_FILE 구조체를 위한 메모리 할당 실패 
*/
#define	ERROR_SN3ZIP_FOPEN_M_MALLOC_ZFILE_FAILURE	35013
/** @brief ZIP 파일에 ZIP 파일 시그니쳐(0x02014b50)가 없음 
*/
#define	ERROR_SN3ZIP_FOPEN_M_INVALID_SIGNATURE		35014 
/** @brief ZIP 파일에 ZIP 파일 시그니쳐(0x02014b50)가 없음 
*/
#define	ERROR_SN3ZIP_FOPEN_M_MALLOC_FILENAME_FAILURE	35015 
/** @brief ZIP 파일이름을 위한 메모리 할당 실패 
*/
#define	ERROR_SN3ZIP_FOPEN_M_MALLOC_EXTRAFIELD_FAILURE	35016 
/** @brief ZIP 파일 처리 중 파일의 끝에 도달함 
*/
#define	ERROR_SN3ZIP_FOPEN_M_END_OF_FILELIST		35017 

/** @brief ZIP 파일 닫기 중 SN3ZIP_FILE가 NULL 
*/
#define	ERROR_SN3ZIP_FCLOSE_NULL_ZFILE			35021 

/** @brief 지원되지 않는 압축형식(ZIP 압축 방식이 STORED 혹은 DEFLATED 이 아님)
*/
#define	ERROR_SN3ZIP_UNZIP_M_NOT_SUPPORTED_COMPRESSION		35031 
/** @brief ZIP 압축해제를 위한 메모리 할당 실패
*/
#define	ERROR_SN3ZIP_UNZIP_M_UNCOMPRESSED_MALLOC_FAILURE	35032 
/** @brief STORED 형식의 ZIP 내용을 SN3MFI로부터 읽기 실패
*/
#define	ERROR_SN3ZIP_UNZIP_M_STORED_DATA_FREAD_FAILURE		35033 
/** @brief STORED 형식의 ZIP 내용을 SN3MFI로 쓰기 실패
*/
#define	ERROR_SN3ZIP_UNZIP_M_STORED_DATA_FWRITE_FAILURE		35034 
/** @brief DEFLATED 형식의 ZIP 내용을 SN3MFI로 쓰기 실패
*/
#define	ERROR_SN3ZIP_UNZIP_M_DEFLATED_DATA_ZWRITE_FAILURE	35037 
/** @brief DEFLATED 형식의 ZIP 내용을 SN3MFI로 쓰기 실패
*/
#define	ERROR_SN3ZIP_UNZIP_M_GZIP_ZCLOSE_FAILURE		35038 
/** @brief
*/
#define	ERROR_SN3ZIP_UNZIP_M_IMPOSSIBLE_PATH_FLOW		35039 
/** @brief 깨진 ZIP 파일 
*/
#define	ERROR_SN3ZIP_FOPEN_M_BROKEN_ZIP_FILE			35040 

/** @brief zip 암호화인 경우
*/
#define ERROR_SN3ZIP_FILTER_FS_FILE_ENCRYPTED		35042  // by lightbell 2009.01.07

/** @brief ZIP 파일 내에 해당 파일이 없음
*/
#define ERROR_SN3ZIP_FILE_NOT_FOUND				35051 

/** @brief ZIP 파일의 central directory signature를 찾지 못함
*/
#define ERROR_SN3ZIP_NOT_FOUND_END_SIG			35061 

/** @brief ZIP 파일의 uncompress size 가 0 일 경우
*/
#define ERROR_SN3ZIP_UNCOMPRESS_SIZE_ZERO		35071
/** @brief ZIP 파일 해제중 생긴 오류
*/
#define ERROR_SN3ZIP_UNZIP_STRM_ERROR			35072
/** @brief ZIP 파일 해제중 메모리 할당 실패
*/
#define ERROR_SN3ZIP_MEMORY_ALLOC_FAILURE			35073

/** @bried archive fileinfo 생성 실패
*/
#define ERROR_SN3ARFILIST_INIT_FAILED			36001
/** @bried archive fileinfo 잘못된 인자
 */
#define ERROR_SN3ARFILIST_NULL_LIST				36002
/** @bried archive fileinfo 잘못된 인자
 */
#define ERROR_SN3ARFILIST_WRONG_IDX				36003

// SN3FMT ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief 암호화된 office 2007 파일  
*/
#define ERROR_SN3FMT_ENCRYPT_OFFICE	44001 
/** @brief 메모리 할당 실패
*/
#define ERROR_SN3FMT_MEMORY_ALLOC_FAILURE	44100 

// XLSX ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief 압축 해제된 파일을 위한 SN3MFI 열기 실패
*/
#define ERROR_SN3XLSX_CANNOT_OPEN_UNZIPFILE	45001 
/** @brief XLSX 파일로부터 압축 해제된 파일 열기 실패
*/
#define ERROR_SN3XLSX_CANNOT_ARCHIVE_ZIP	45002 
/** @brief XLSX 파일로부터 압축 해제된 XML파일 파싱시 오류 발생
*/
#define ERROR_SN3XLSX_CANNOT_PARSE_XML		45003 

/** @brief XLSX 텍스트 출력 버퍼가 NULL
*/
#define ERROR_SN3XLSX_OUTPUT_BUFFER_NULL	45004 

/** @brief XLSX 메모리 부족
*/
#define ERROR_SN3XLSX_MEMORY_ALLOC_FAILURE	45005


// XLS ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief 암호화된 XLS 파일  
*/ 
#define SN3XLS_ERROR_ENCRYPT_EXCEL	30010 
/** @brief 
*/
#define SN3XLS_ERROR_ENCRYPT_HANCELL	30011 
/** @brief
*/
#define ERROR_SN3XLS_MEMORY_ALLOC_FAILURE	30012
/** @brief
*/
#define ERROR_SN3XLS_CANT_READ_SST			30013

// TAR ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief TAR 파일 내의 특정 블럭의 크기가 512 미만임
*/
#define	ERROR_SN3TAR_FILTER_M_INVALID_BLOCK_SIZE	33601 
/** @brief TAR 파일 내 메모리 할당 실패
*/
#define	ERROR_SN3TAR_MEMORY_ALLOC_FAILURE			33602


// SXX ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief OpenOffice 파일 필터링 중 XML 파싱 오류
*/
#define ERROR_SN3SXX_CANNOT_PARSE_XML		34001 

/** @brief OpenOffice 압축 파일을 SN3MFI로 열기 실패
*/
#define ERROR_SN3SXX_CANNOT_OPEN_UNZIPFILE	34011 
/** @brief OpenOffice 압축 파일 내 특정 xml 파일을 찾지 못함 
*/
#define ERROR_SN3SXX_CANNOT_ARCHIVE_ZIP		34012 

/** @brief 압축 파일이 OpenOffice 파일이 아님 
*/
#define ERROR_SN3SXX_IS_NOT_SXX_FILE		34021

/** @brief 암호화된 OpenOffice 파일 입니다.
*/
#define ERROR_SN3SXX_IS_ENCRYPTED_FILE		34023


// SWF ERROR /////////////////////////////////////////////////////////////////////////////


/** @brief 잘못된 SWF 파일(파일 내 특정 정보가 없음) 
*/
#define ERROR_SN3SWF_LOAD_FILENOT_SWF			31701 
/** @brief 알 수 없는 SWF 파일 버전
*/
#define ERROR_SN3SWF_LOAD_VERSION_UNKNOWN		31702 
/** @brief 필터링을 위한 메모리 할당 실패
*/
#define ERROR_SN3SWF_LOAD_MALLOC_FAILURE		31703 
/** @brief 잘못된 SWF 파일(파일의 길이가 파일 스펙과 틀림)
*/
#define ERROR_SN3SWF_LOAD_BAD_FILESIZE			31704 

// SN3SUM ERROR //////////////////////////////////////////////////////////////////////////

/** @brief SN3SUM 구조체를 위한 메모리 할당 실패
*/
#define	ERROR_SN3SUM_INIT_MEMORY_ALLOCATION_FAILURE		40201 
/** @brief SN3SUM 구조체 메모리 해제 시 SN3SUM이 NULL
*/
#define	ERROR_SN3SUM_FREE_SUMMARY_IS_NULL				40202 
/** @brief SN3SUM 내용을 쓰기 위한 FILE 열기 실패
*/
#define	ERROR_SN3SUM_UNLOAD_FILE_OPEN_FAILURE			40203 

/** @brief MS Office 2007 문서의 문서 정보 읽기 중 문서 파일을 SN3MFI로 열기 실패
*/
#define ERROR_SN3SUM_CANNOT_OPEN_UNZIPFILE	40301 
/** @brief MS Office 2007 압축 파일 내 문서정보 XML 파일이 없음
*/
#define ERROR_SN3SUM_CANNOT_ARCHIVE_ZIP	40302 
/** @brief MS Office 2007 문서정보 XML 파싱 실패
*/
#define ERROR_SN3SUM_CANNOT_PARSE_XML		40303 

/** @brief SN3SUM 포인터가 NULL인 경우 (snf_sum_init필요)
*/
#define ERROR_SN3SUM_IS_NULL	40304 


// Format NDOC ERROR /////////////////////////////////////////////////////////////////////////// 
/** @brief	Encrypt된 NDOC 문서의 헤더정보를 Decrypt할 수 없는경우
*/
#define ERROR_NDOC_CANNOT_DECRYPT_HEADER	61001

// RTF ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief RTF Mark-up 문자 '}'가 잘못 됨
*/      
#define ERROR_SN3RTF_FILTER_M_STACK_UNDERFLOW    30701 
/** @brief RTF Mark-up 문자 '{'가 '}' 보다 많음
*/      
#define ERROR_SN3RTF_FILTER_M_STACK_OVERFLOW     30702 
/** @brief RTF 파일 필터링 중 RTF Mark-up 문자 '}'없이 문서의 마지막에 도달함
*/      
#define ERROR_SN3RTF_FILTER_M_UNMATCHED_BRACE    30703 
/** @brief RTF 파일 내 잘못된 16진수 문자열이 있음
*/      
#define ERROR_SN3RTF_FILTER_M_INVALID_HEX        30704 
/** @brief RTF 파일 내 잘못된 정보가 있음*/      
#define ERROR_SN3RTF_FILTER_M_BAD_TABLE          30705 
/** @brief RTF 파일 파싱 오류
*/      
#define ERROR_SN3RTF_FILTER_M_ASSERTION_FAILURE  30706 
/** @brief RTF 파일 파싱 중 파일의 끝에 도달함
*/      
#define ERROR_SN3RTF_FILTER_M_END_OF_FILE        30707 


// PPTX ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief 압축 해제된 파일을 위한 SN3MFI 열기 실패
*/
#define ERROR_SN3PPTX_CANNOT_OPEN_UNZIPFILE	47001 
/** @brief DOCX 파일로부터 압축 해제된 파일 열기 실패
*/
#define ERROR_SN3PPTX_CANNOT_ARCHIVE_ZIP	47002 
/** @brief PPTX 파일로부터 압축 해제된 XML파일 파싱시 오류 발생
*/
#define ERROR_SN3PPTX_CANNOT_PARSE_XML		47003
/** @brief PPTX 처리 중 xml parser 초기화 실패
*/
#define ERROR_SN3PPTX_FAILED_TO_INIT_XML_PARSER		47004
/** @brief PPTX 처리 중 메모리 할당 실패
*/
#define ERROR_SN3PPTX_MEMORY_ALLOC_FAILURE		47005
//////////////////////////////////////////////////////////////////////////////////////////


// XPS ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief 압축 해제된 파일을 위한 SN3MFI 열기 실패
*/
#define ERROR_SN3XPS_CANNOT_OPEN_UNZIPFILE	48001 
/** @brief XPS 파일로부터 압축 해제된 파일 열기 실패
*/
#define ERROR_SN3XPS_CANNOT_ARCHIVE_ZIP		48002 
/** @brief XPS 파일로부터 압축 해제된 XML파일 파싱시 오류 발생
*/
#define ERROR_SN3XPS_CANNOT_PARSE_XML		48003 
/** @brief XPS 내 Document 읽기 실패
 */
#define ERROR_SN3XPS_CANNOT_OPEN_DOCUMENT	48004

//////////////////////////////////////////////////////////////////////////////////////////


// PPT ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief	PPT의 암호화인 경우 
*/
#define ERROR_SN3PPT_FILTER_FS_FILE_ENCRYPTED	50000 

/** @brief  잘못된 Atom이 존재하는 경우 오류 발생
*/
#define ERROR_SN3PPT_FOUND_BAD_ATOM				50001 

/** @brief  잘못된 Offset 값을 참조하는 경우
*/
#define ERROR_SN3PPT_INVALID_OFFSET				50002 
/** @brief 잘못된 slidelist 정보
*/
#define ERROR_SN3PPT_FOUND_BAD_SLIDE_LIST	50003 
/** @brief 잘못된 디렉토리 엔트리
*/
#define ERROR_SN3PPT_FOUND_BAD_DIR_ENTRY	50004
/** @brief 잘못된 Offset
*/
#define ERROR_SN3PPT_FOUND_BAD_OFFSET		50005
/** @brief 메모리 할당 실패
*/
#define ERROR_SN3PPT_MEMORY_ALLOC_FAILURE	50006
/** @brief 잘못된 헤더 타입
*/
#define ERROR_SN3PPT_INVALID_HEADER_TYPE	50007
/** @brief 잘못된 헤더 길이
*/
#define ERROR_SN3PPT_INVALID_HEADER_LENGTH	50008
/** @brief
*/
#define ERROR_SN3PPT_INVALID_CUSTREAM		50009
/** @brief
*/
#define ERROR_SN3PPT_INVALID_LUES			50010
/** @brief
*/
#define ERROR_SN3PPT_INVALID_MASTER_IDX		50011
/** @brief
*/
#define ERROR_SN3PPT_FAILD_OLE_DECODE		50012
/** @brief 잘못된 레코드 헤더
 */
#define ERROR_SN3PPT_WRONG_RECORD_HEADER	50013
//////////////////////////////////////////////////////////////////////////////////////////


// BZIP ERROR  ///////////////////////////////////////////////////////////////////////////

/** @brief BZIPFILE OpenError
*/
#define ERROR_SN3BZIP_CANNOT_OPEN_BZIPFILE	57001 

/** @brief BZIPFILE Read Error
*/
#define ERROR_SN3BZIP_CANNOT_READ_BZIPFILE	57002

/** @brief BZIPFILE Read Get Unused
*/
#define ERROR_SN3BZIP_CANNOT_READ_UNUSED	57003

/** @brief BZIPFILE Close
*/
#define ERROR_SN3BZIP_CANNOT_CLOSE	57004

/** @brief Memory Allocation Fail
*/
#define ERROR_SN3BZIP_MEM_ALLOC_FAILED				57005

//////////////////////////////////////////////////////////////////////////////////////////

// ALZIP ERROR  ///////////////////////////////////////////////////////////////////////////

/** @brief ALZIP Noerror 
*/
#define ERROR_SN3ALZ_NOERR						0
/** @brief GENERAL ERROR
*/
#define ERROR_SN3ALZ_GENERAL						58002	
/** @brief 파일열기 실패
*/
#define ERROR_SN3ALZ_CANT_OPEN_FILE				58003	
/** @brief 
*/
#define ERROR_SN3ALZ_CANT_OPEN_DEST_FILE			58004	
/** @brief 깨진 알집 파일
*/
#define ERROR_SN3ALZ_CORRUPTED_FILE				58005	
/** @brief ALZIP 이 아님.
*/
#define ERROR_SN3ALZ_NOT_ALZ_FILE					58006	
/** @brief alz signature 읽기 실패
*/
#define ERROR_SN3ALZ_CANT_READ_SIG				58007	
/** @brief alz 헤더를 읽을 수 없음
*/
#define ERROR_SN3ALZ_CANT_READ_FILE				58008
/** @brief alz 헤더를 읽을 수 없는 경우
*/
#define ERROR_SN3ALZ_AT_READ_HEADER				58009
/** @brief alz 잘못된 파일 이름 길이
*/
#define ERROR_SN3ALZ_INVALID_FILENAME_LENGTH		58010
/** @brief alz 헤더에서 디렉토리를 읽을 수 없음
*/
#define ERROR_SN3ALZ_CANT_READ_CENTRAL_DIRECTORY_STRUCTURE_HEAD	58012

/** @brief alz 메모리 할당 실패
*/
#define ERROR_SN3ALZ_MEM_ALLOC_FAILED				58017
/** @brief alz BZIP2 파싱 실패
*/
#define ERROR_SN3ALZ_BZIP2_FAILED					58020
/** @brief alz 풀수 없는 압축방식
*/
#define ERROR_SN3ALZ_UNKNOWN_COMPRESSION_METHOD	58022

/** @brief alz 로컬파일의 헤더를 읽을 수 없음
*/
#define ERROR_SN3ALZ_CANT_READ_LOCAL_FILE_HEAD	58031

/** @brief alz 암호화인 경우
*/
#define ERROR_SN3ALZ_FILTER_FS_FILE_ENCRYPTED		58032  

//////////////////////////////////////////////////////////////////////////////////////////

// OLE10NATIVE ERROR  ///////////////////////////////////////////////////////////////////////////
/** @brief signature OLE파일이 아님
*/
#define ERROR_SN3OLE10NATIVE_NOT_OLE 59001
/** @brief signature native stream을 읽기 실패
*/
#define ERROR_SN3OLE10NATIVE_STREAM_READ_FAIL 59002
/** @brief signature 메모리가 충분하지 못하여 native stream 읽기 실패
*/
#define ERROR_SN3OLE10NATIVE_NOT_ENOUGH_MEM 59003

/** @brief OLENATIVE10 에서 Native Data Block Read 실패	
*/
#define ERROR_SN3OLE10NATIVE_UNKNOWN	59004

/** @brief OLENATIVE10 에서 Native Data Filtering Fail
*/
#define ERROR_SN3OLE10NATIVE_FILTER_FAIL	59005



//////////////////////////////////////////////////////////////////////////////////////////


//////////////////////////////////////////////////////////////////////////////////////////

// WPD ERROR  ///////////////////////////////////////////////////////////////////////////

/** @brief WPD 파일 헤더 읽기 실패
*/
#define ERROR_SN3WPD_FAIL_READ_HEADER 62000
/** @brief
*/
#define ERROR_SN3WPD_BAD_PAIR_FUNC_DOC 62001
/** @brief WPD 파일 버전 체크에 실패
*/
#define ERROR_SN3WPD_INVALID_HEADER_VERSION 62003
/** @brief WPD 파일이 아닌 경우
*/
#define ERROR_SN3WPD_NOT_DOCUMENT_TYPE 62004

//////////////////////////////////////////////////////////////////////////////////////////


//////////////////////////////////////////////////////////////////////////////////////////

// 7ZIP ERROR  ///////////////////////////////////////////////////////////////////////////

/** @brief GENERAL ERROR
*/
#define ERROR_SN3SEVENZIP_GENERAL						61002	
/** @brief 파일열기 실패
*/
#define ERROR_SN3SEVENZIP_CANT_OPEN_FILE				61003	
/** @brief Deprecated
*/
#define ERROR_SN3SEVENZIP_CANT_OPEN_DEST_FILE			61004	
/** @brief 깨진 압축 파일
*/
#define ERROR_SN3SEVENZIP_CORRUPTED_FILE				61005	
/** @brief signature 읽기 실패
*/
#define ERROR_SN3SEVENZIP_CANT_READ_SIG					61006
/** @brief
*/
#define ERROR_SN3SEVENZIP_UNKNOWN_COMPRESSION_METHOD	61008

/** @brief sevenzip 암호화인 경우
*/
#define ERROR_SN3SEVENZIP_FILTER_FS_FILE_ENCRYPTED		61009  

/** @brief 압축 해제중 CRC 오류가 발생한 경우
*/
#define ERROR_SN3SEVENZIP_FILTER_BAD_CRC				61010
/** @brief 
*/
#define ERROR_SN3SEVENZIP_DATA							61011
/** @brief
*/
#define ERROR_SN3SEVENZIP_MEM							61012
/** @brief 
*/
#define ERROR_SN3SEVENZIP_UNSUPPORTED					61014
/** @brief 
*/
#define ERROR_SN3SEVENZIP_PARAM							61015
/** @brief 
*/
#define ERROR_SN3SEVENZIP_INPUT_EOF						61016
/** @brief 
*/
#define ERROR_SN3SEVENZIP_FAIL							61021
/** @brief 
*/
#define ERROR_SN3SEVENZIP_ARCHIVE						61026
/** @brief LZMA2 형식으로 압축이 되어있는 경우
*/
#define ERROR_SN3SEVENZIP_UNSUPPORTED_LZMA2				61028
/** @brief 
*/
#define ERROR_SN3SEVENZIP_UNSUPPORTED_PPMD				61029
/** @brief 
*/
#define ERROR_SN3SEVENZIP_UNSUPPORTED_BZIP2				61030
//////////////////////////////////////////////////////////////////////////////////////////


//////////////////////////////////////////////////////////////////////////////////////////

// RAR ERROR  ///////////////////////////////////////////////////////////////////////////

/** @brief GENERAL ERROR
*/
#define ERROR_SN3RAR_GENERAL						71002	
/** @brief 파일열기 실패
*/
#define ERROR_SN3RAR_CANT_OPEN_FILE				71003	
/** @brief Deprecated
*/
#define ERROR_SN3RAR_CANT_OPEN_DEST_FILE			71004	
/** @brief 깨진 압축 파일
*/
#define ERROR_SN3RAR_CORRUPTED_FILE				71005	
/** @brief signature 읽기 실패
*/
#define ERROR_SN3RAR_CANT_READ_SIG					71006
/** @brief Deprecated
*/
#define ERROR_SN3RAR_CANT_READ_FILE				71007
/** @brief Deprecated
*/
#define ERROR_SN3RAR_UNKNOWN_COMPRESSION_METHOD	71008

/** @brief rar 암호화인 경우
*/
#define ERROR_SN3RAR_FILTER_FS_FILE_ENCRYPTED		71009

/** @brief 압축 해제중 CRC 오류가 발생한 경우
*/
#define ERROR_SN3RAR_FILTER_BAD_CRC				71010
/** @brief 파일 속성 읽기 실패
*/
#define ERROR_SN3RAR_FAIL							71021
/** @brief 메모리 할당 실패
*/
#define ERROR_SN3RAR_MEM_ALLOC_FAILED			71028


//////////////////////////////////////////////////////////////////////////////////////////

// MDB ERROR  ///////////////////////////////////////////////////////////////////////////

/** @brief 필터링 중 암호가 설정된 파일인경우
*/
#define ERROR_SN3MDB_FILTER_M_PASSWORD_EXISTS		63001

/** @brief 필터링 중 MDB파일의 테이블이 깨진경우
*/
#define ERROR_SN3MDB_FILTER_M_BROKEN_TABLE			63002

/** @brief 필터링 중 MDB파일의 테이블 정보를 읽을 수 없는경우
*/
#define ERROR_SN3MDB_FILTER_M_READ_TABLE			63003

/** @brief 지원하지 않는 JET DB인경우
*/
#define ERROR_SN3MDB_FOPEN_M_UNKNOWN_JET_VERSION	63004

/** @brief MDB의 레코드가 정상적이지 않은 경우
*/
#define	ERROR_SN3MDB_FILTER_M_INVALID_RECORD		63005

/** @brief MDB파일의 signature를 인식할 수 없는 경우
*/
#define	ERROR_SN3MDB_FOPEN_M_INVALID_SIGNATURE		63006

/** @brief MDB파일의 다음 페이지 읽기 실패
*/
#define ERROR_SN3MDB_READ_NEXT_PAGE					63007
/** @brief MDB파일 필터링을 위한 메모리 할당 실패
*/
#define ERROR_SN3MDB_MEMORY_ALLOC_FAILURE					63007
//////////////////////////////////////////////////////////////////////////////////////////

// OLE_CONTENTS ERROR  ///////////////////////////////////////////////////////////////////////////
/** @brief signature OLE파일이 아님
*/
#define ERROR_SN3OLE_CONTENTS_NOT_OLE 72001

/** @brief signature MFI 을 OLE파일에 MOUNT 할 떄 실패
*/
#define ERROR_SN3OLE_CONTENTS_MOUNT 72002

/** @brief signature OLE파일 stream open 실패
*/
#define ERROR_SN3OLE_CONTENTS_STREAM_OPEN 72003

/** @brief signature OLE파일 stream size check 실패
*/
#define ERROR_SN3OLE_CONTENTS_STREAM_SIZE 72004
/////////////////////////////////////////////////////////////////////////////////////////
/** @brief 파일의 끝이 아니지만 알 수 없는 이유로 파일을 읽기 실패
*/
#define ERROR_DGN_READ 73001
//////////////////////////////////////////////////////////////////////////////////////////

// MACRO ERROR ///////////////////////////////////////////////////////////////////////////
/** @brief
*/
#define ERROR_PROJECT_SYSKIND_INVALID_ID   81001
/** @brief
*/
#define ERROR_PROJECT_SYSKIND_INVALID_SIZE 81002
/** @brief
*/
#define ERROR_PROJECT_LCID_INVALID_ID   81011
/** @brief
*/
#define ERROR_PROJECT_LCID_INVALID_SIZE 81012
/** @brief
*/
#define ERROR_PROJECT_LCIDINVOKE_INVALID_ID   81021
/** @brief
*/
#define ERROR_PROJECT_LCIDINVOKE_INVALID_SIZE 81022
/** @brief
*/
#define ERROR_PROJECT_CODEPAGE_INVALID_ID   81031
/** @brief
*/
#define ERROR_PROJECT_CODEPAGE_INVALID_SIZE 81032
/** @brief
*/
#define ERROR_PROJECT_NAME_INVALID_ID   81041
/** @brief
*/
#define ERROR_PROJECT_NAME_INVALID_SIZE 81042
/** @brief
*/
#define ERROR_PROJECT_DOCSTRING_INVALID_ID           81051
/** @brief
*/
#define ERROR_PROJECT_DOCSTRING_INVALID_SIZE         81052
/** @brief
*/
#define ERROR_PROJECT_DOCSTRING_UNICODE_INVALID_SIZE 81053
/** @brief
*/
#define ERROR_PROJECT_HELPFILE1_INVALID_ID   81061
/** @brief
*/
#define ERROR_PROJECT_HELPFILE1_INVALID_SIZE 81062
/** @brief
*/
#define ERROR_PROJECT_HELPFILE2_INVALID_SIZE 81063
/** @brief
*/
#define ERROR_PROJECT_CONTEXT_INVALID_ID   81071
/** @brief
*/
#define ERROR_PROJECT_CONTEXT_INVALID_SIZE 81072
/** @brief
*/
#define ERROR_PROJECT_LIBFLAGS_INVALID_ID   81081
/** @brief
*/
#define ERROR_PROJECT_LIBFLAGS_INVALID_SIZE 81082
/** @brief
*/
#define ERROR_PROJECT_VERSION_INVALID_ID   81091
/** @brief
*/
#define ERROR_PROJECT_VERSION_INVALID_SIZE 81092
/** @brief
*/
#define ERROR_PROJECT_CONSTANTS_INVALID_ID           81101
/** @brief
*/
#define ERROR_PROJECT_CONSTANTS_INVALID_SIZE         81102
/** @brief
*/
#define ERROR_PROJECT_CONSTANTS_UNICODE_INVALID_SIZE 81103
/** @brief
*/
#define ERROR_PROJECT_CHUNK_INVALID_SIZE 81200

// REFERENCE
/** @brief
*/
#define ERROR_REFERENCE_NAME_INVALID_ID   82001
/** @brief
*/
#define ERROR_REFERENCE_ORIGINAL_INVALID_ID 82011
/** @brief
*/
#define ERROR_REFERENCE_CONTROL_INVALID_ID        82021
/** @brief
*/
#define ERROR_REFERENCE_CONTROL_INVALID_RESERVED1 82022
/** @brief
*/
#define ERROR_REFERENCE_CONTROL_INVALID_RESERVED2 82023
/** @brief
*/
#define ERROR_REFERENCE_CONTROL_INVALID_RESERVED3 82024
/** @brief
*/
#define ERROR_REFERENCE_CONTROL_INVALID_RESERVED4 82025
/** @brief
*/
#define ERROR_REFERENCE_CONTROL_INVALID_RESERVED5 82026
/** @brief
*/
#define ERROR_REFERENCE_REGISTERED_INVALID_ID        82031
/** @brief
*/
#define ERROR_REFERENCE_REGISTERED_INVALID_RESERVED1 82032
/** @brief
*/
#define ERROR_REFERENCE_REGISTERED_INVALID_RESERVED2 82033
/** @brief
*/
#define ERROR_REFERENCE_PROJECT_INVALID_ID 82041

// MODULE
/** @brief
*/
#define ERROR_PROJECT_MODULES_INVALID_ID   83001
/** @brief
*/
#define ERROR_PROJECT_MODULES_INVALID_SIZE 83002
/** @brief
*/
#define ERROR_PROJECT_COOKIE_INVALID_ID    83003
/** @brief
*/
#define ERROR_PROJECT_COOKIE_INVALID_SIZE  83004
/** @brief
*/
#define ERROR_MODULE_NAME_INVALID_ID           83011
/** @brief
*/
#define ERROR_MODULE_NAME_INVALID_SIZE         83012
/** @brief
*/
#define ERROR_MODULE_NAME_UNICODE_INVALID_ID   83015
/** @brief
*/
#define ERROR_MODULE_NAME_UNICODE_INVALID_SIZE 83016
/** @brief
*/
#define ERROR_MODULE_STREAMNAME_INVALID_ID         83021
/** @brief
*/
#define ERROR_MODULE_STREAMNAME_UNICODE_INVALID_ID 83022
/** @brief
*/
#define ERROR_MODULE_DOCSTRING_INVALID_ID         83041
/** @brief
*/
#define ERROR_MODULE_DOCSTRING_UNICODE_INVALID_ID 83042
/** @brief
*/
#define ERROR_MODULE_OFFSET_INVALID_ID   83051
/** @brief
*/
#define ERROR_MODULE_OFFSET_INVALID_SIZE 83052
/** @brief
*/
#define ERROR_MODULE_HELPCONTEXT_INVALID_ID   83061
/** @brief
*/
#define ERROR_MODULE_HELPCONTEXT_INVALID_SIZE 83062
/** @brief
*/
#define ERROR_MODULE_COOKIE_INVALID_ID   83071
/** @brief
*/
#define ERROR_MODULE_COOKIE_INVALID_SIZE 83072
/** @brief
*/
#define ERROR_MODULE_TYPE_INVALID_ID   83081
/** @brief
*/
#define ERROR_MODULE_TYPE_INVALID_SIZE 83082
/** @brief
*/
#define ERROR_MODULE_END_INVALID_ID 83091

// HEADER
/** @brief cumpressBuffer 의 첫번째 바이트가 0x01 이 아닐 경우
*/
#define ERROR_COMPRESS_CURRENT_INVALID_HEADER 84001
//////////////////////////////////////////////////////////////////////////////////////////

/** @brief XML 파싱 에러
*/
#define ERROR_SN3XML_STATUS								64001
/** @brief XML 해당 엘리먼트 없음
*/
#define ERROR_SN3XML_NO_ELEMENTS                        64002

// PST ERROR  ///////////////////////////////////////////////////////////////////////////

/** @brief PST 파일 헤더의 dwMagic 가 틀린 경우
 */
#define ERROR_SN3PST_HEADER_DW_MAGIC			89001
/** @brief
*/
#define ERROR_SN3PST_HEADER_ENCODING_TYPE		89002
/** @brief
*/
#define ERROR_SN3PST_HEADER_IB_FILE_EOF			89003
/** @brief
*/
#define ERROR_SN3PST_HEADER_W_MAGIC_CLIENT		89004
/** @brief
*/
#define ERROR_SN3PST_HEADER_B_PLATFORM_CREATE	89005
/** @brief
*/
#define ERROR_SN3PST_HEADER_B_PLATFORM_ACCESS	89006
/** @brief
*/
#define ERROR_SN3PST_HEADER_B_SENTINEL			89007
/** @brief
*/
#define ERROR_SN3PST_HEADER_B_CRYPT_METHOD		89008
/** @reief 사이즈가 2G 이상일 경우 오류
*/
#define ERROR_SN3PST_SIZE_LIMIT					89009
/** @brief
*/
#define ERROR_SN3PST_BREFBBT_BID_INVALID		89100
/** @brief
*/
#define ERROR_SN3PST_BREFNBT_BID_INVALID		89101
/** @brief 
*/
#define ERROR_SN3PST_DATA_READ_FAILED		89200
/** @brief
*/
#define ERROR_SN3PST_EMAIL_DATA_READ_FAILED		89201
/** @brief PST 메모리 Malloc/Realloc 오류
 */
#define ERROR_SN3PST_MEMORY_ALLOC_FAILURE 		89202


// SN3XML ERROR  ///////////////////////////////////////////////////////////////////////////

// IWORK ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief xml 파일을 읽을 버퍼 할당 실패
*/
#define ERROR_SN3IWORK_NO_MEMMORY			90001 
/** @brief buffer에 xml파일 읽기 실패
*/
#define ERROR_SN3IWORK_CANNOT_READ_FILE	90002 
/** @brief xml DomTree 생성 실패
*/
#define ERROR_SN3IWORK_CANNOT_PARSE_TREE	90003 
/** @brief iwork2013/4 잘못된 header
*/
#define ERROR_SN3IWORK2K_INVAILD_HEADER	90010
/** @brief iwork2013/4  Decode error
*/
#define ERROR_SN3IWORK2K_DECODE_ERROR		90011
/** @brief iwork2013/4 잘못된 MessageInfo stream
*/
#define ERROR_SN3IWORK2K_INVALID_MESSAGE_INFO		90012
/** @brief 잘못된 iwork2013 파일
*/
#define ERROR_SN3IWORK2013_INVALID_FILE		90013
//////////////////////////////////////////////////////////////////////////////////////////

// KEYNOTE ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief 압축 해제된 파일을 위한 SN3MFI 열기 실패
*/
#define ERROR_SN3KEYNOTE_CANNOT_OPEN_UNZIPFILE	91001 
/** @brief KEYNOTE 파일로부터 압축 해제된 파일 열기 실패
*/
#define ERROR_SN3KEYNOTE_CANNOT_ARCHIVE_ZIP		91002 
/** @brief KEYNOTE 파일로부터 압축 해제된 XML파일 파싱시 오류 발생
*/
#define ERROR_SN3KEYNOTE_CANNOT_PARSE_XML		91003 
/** @brief xml 파일을 읽을 버퍼 할당 실패
*/
#define ERROR_SN3KEYNOTE_NO_MEMMORY				91004

//////////////////////////////////////////////////////////////////////////////////////////

// PAGES ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief 압축 해제된 파일을 위한 SN3MFI 열기 실패
*/
#define ERROR_SN3PAGES_CANNOT_OPEN_UNZIPFILE	92001 
/** @brief PAGES 파일로부터 압축 해제된 파일 열기 실패
*/
#define ERROR_SN3PAGES_CANNOT_ARCHIVE_ZIP		92002 
/** @brief PAGES 파일로부터 압축 해제된 XML파일 파싱시 오류 발생
*/
#define ERROR_SN3PAGES_CANNOT_PARSE_XML			92003 
/** @brief xml 파일을 읽을 버퍼 할당 실패
*/
#define ERROR_SN3PAGES_NO_MEMMORY				92004

//////////////////////////////////////////////////////////////////////////////////////////

// NUMBERS ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief 압축 해제된 파일을 위한 SN3MFI 열기 실패
*/
#define ERROR_SN3NUMBERS_CANNOT_OPEN_UNZIPFILE	93001 
/** @brief NUMBERS 파일로부터 압축 해제된 파일 열기 실패
*/
#define ERROR_SN3NUMBERS_CANNOT_ARCHIVE_ZIP		93002 
/** @brief NUMBERS 파일로부터 압축 해제된 XML파일 파싱시 오류 발생
*/
#define ERROR_SN3NUMBERS_CANNOT_PARSE_XML		93003 
/** @brief xml 파일을 읽을 버퍼 할당 실패
*/
#define ERROR_SN3NUMBERS_NO_MEMMORY				93004

//////////////////////////////////////////////////////////////////////////////////////////

// DRM ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief DRM 문서는 지원하지 않습니다.
*/
#define ERROR_SN3FMT_DRM_DOCUMENT				94001

//////////////////////////////////////////////////////////////////////////////////////////

// KEYNOTE ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief 압축 해제된 파일을 위한 SN3MFI 열기 실패
*/
#define ERROR_SN3HWPX_CANNOT_OPEN_UNZIPFILE	95001 
/** @brief HWPX 파일로부터 압축 해제된 파일 열기 실패
*/
#define ERROR_SN3HWPX_CANNOT_ARCHIVE_ZIP		95002 
/** @brief HWPX 파일로부터 압축 해제된 XML파일 파싱시 오류 발생
*/
#define ERROR_SN3HWPX_CANNOT_PARSE_XML		95003 
/** @brief HWPX 처리 중 xml parser 초기화 실패
*/
#define ERROR_SN3HWPX_FAILED_TO_INIT_XML_PARSER		95004
 
//////////////////////////////////////////////////////////////////////////////////////////

// XLSB ERROR ////////////////////////////////////////////////////////////////////////////
/** @brief XLSB 메모리 할당 실패
*/
#define ERROR_SN3XLSB_MEMORY_ALLOC_FAILURE	96001
//////////////////////////////////////////////////////////////////////////////////////////

// DICOM ERROR ////////////////////////////////////////////////////////////////////////////
/** @brief 
*/
#define ERROR_SN3DICOM_QA_PARSE_FAILURE	98000
//////////////////////////////////////////////////////////////////////////////////////////

// COMMON ERROR ////////////////////////////////////////////////////////////////////////////
/** @brief 현재 버전에서 지원하지 않음
*/
#define ERROR_NOT_SUPPORTED_IN_CURRENT_VERSION		97000

/**************************************************************
 * Function Declarations
 **************************************************************/
/***************************************************************/

/***************************************************************/
