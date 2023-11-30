#include <stdio.h>
#include <stdbool.h>
#ifdef _WIN32
#include "snf_win.h"
#else // !_WIN32
#include "snf.h"
#endif // !_WIN32
#include "sn3err.h"
#include "status_code.h"

#if defined(_WIN32)
#define SNF_PREFIX(fname) w##fname
#else // !defined(_WIN32)
#define SNF_PREFIX(fname) fname
#endif // !defined(_WIN32)

int convertSynapErrorToMpiislError(int nErrorCode)
{
	if(1001 == SNF_PREFIX(snf_err_isbadfile)(nErrorCode))
	{
		return MPIISL_ERROR_EXTRACTION_BAD_FILE;
	}
	switch(nErrorCode)
	{
	case 0: // 에러 코드가 정의 되어 있지만 그 값이 0인 경우를 걸러내기 위해 항상 명시적으로 포함한다.
		return 0;
	// MFI ERROR /////////////////////////////////////////////////////////////////////////////
	// SN3MFI 구조체를 위한 메모리 할당 실패
	case ERROR_SN3MFI_FOPEN_RW_MFI_MALLOC_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 파일 메모리가 NULL이거나 메모리 크기가 0 이하임
	case ERROR_SN3MFI_FOPEN_M_NULL_MEMFILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3MFI 구조체를 위한 메모리 할당 실패
	case ERROR_SN3MFI_FOPEN_M_MFI_MALLOC_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// FILE 포인터가 NULL이거나 파일의 크기가 0 이하임
	case ERROR_SN3MFI_FOPEN_F_NULL_FILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// FILE의 내용을 읽기 위한 FILE 크기 만큼의 메모리 할당 실패 
	case ERROR_SN3MFI_FOPEN_F_FILE_MALLOC_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// FILE의 내용을 읽기 위한 FILE 크기 만큼의 메모리 할당 실패 
	case ERROR_SN3MFI_FOPEN_F_MFI_MALLOC_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// FILE 내용 읽기 실패
	case ERROR_SN3MFI_FOPEN_F_FREAD_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// FILE의 경로 문자열이 NULL
	case ERROR_SN3MFI_FOPEN_NULL_FILEPATH:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// FILE의 크기가 0 
	case ERROR_SN3MFI_FOPEN_FILE_SIZE_ZERO:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// FILE 읽기 권한이 없음 
	case ERROR_SN3MFI_FOPEN_NO_READ_ACCESS:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// FILE 정보 읽기 오류(STAT 실패) 
	case ERROR_SN3MFI_FOPEN_READING_FILE_STAT:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// FILE의 내용을 읽기 위한 FILE 크기 만큼의 메모리 할당 실패 
	case ERROR_SN3MFI_FOPEN_FILE_MALLOC_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// FILE 열기 실패 
	case ERROR_SN3MFI_FOPEN_FILE_OPEN_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// FILE 내용 읽기 실패 
	case ERROR_SN3MFI_FOPEN_FILE_READ_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3MFI 구조체를 위한 메모리 할당 실패 
	case ERROR_SN3MFI_FOPEN_MFI_MALLOC_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3MFI 가 NULL 
	case ERROR_SN3MFI_FCLOSE_NULL_MFI:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3MFI 파일 위치 이동 중 SN3MFI 가 NULL 
	case ERROR_SN3MFI_FSEEK_NULL_FILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3MFI 파일 위치 이동 중 잘못된 방향 옵션 설정 
	case ERROR_SN3MFI_FSEEK_BAD_ORIGIN:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3MFI의 내용을 FILE에 쓰기 실패 
	case ERROR_SN3MFI_UNLOAD_F_FWRITE_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3MFI의 내용을 쓰기 위한 FILE 열기 실패 
	case ERROR_SN3MFI_UNLOAD_FILE_OPEN_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3MFI 복제시 NULL 오류.
	case ERROR_SN3MFI_FCOPY_NULL_ERROR:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3MFI 복제 실패.
	case ERROR_SN3MFI_FCOPY_WRITE_ERROR:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3BUF ERROR //////////////////////////////////////////////////////////////////////////
	// SN3BUF 메모리 할당 초기화 실패
	case ERROR_SN3BUF_INIT_BUFFER_MEMORY_ALLOCATION_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3BUF가 NULL일 때 메모리를 해제하는 경우
	case ERROR_SN3BUF_FREE_BUFFER_IS_NULL:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3BUF에 있는 내용을 파일로 쓰기위한 파일 열기 실패
	case ERROR_SN3BUF_UNLOAD_FILE_OPEN_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// NULL인 SN3BUF에 UCS2 문자를 버퍼에 넣으려고 할때 오류
	case ERROR_SN3BUF_PUTC_UCS2_BUFFER_IS_NULL:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3BUF 메모리 재할당 실패
	case ERROR_SN3BUF_PUTC_UCS2_BUFFER_REALLOCATION_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// NULL인 SN3BUF에 UCS2 문자열을 버퍼에 넣으려고 할때 오류
	case ERROR_SN3BUF_PUTS_UCS2_BUFFER_IS_NULL:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// NULL인 문자열을 SN3BUF에 넣으려고 할때 오류
	case ERROR_SN3BUF_PUTS_UCS2_INPUT_IS_NULL:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 임시로 사용할 UCS2 문자열을 할당 실패
	case ERROR_SN3BUF_PUTS_CP949_TMPOUTPUT_ALLOCATION_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// CP949 문자열을 SN3BUF에 기록 중 포인터가 문자열을 넘어감
	case ERROR_SN3BUF_PUTS_CP949_OOPS_OUTPUT_OVERRUN:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3BUF 앞쪽에 UCS2-LE 문자를 넣을 때 SN3BUF의 시작포인트가 0보다 작은 경우
	case ERROR_SN3BUF_UNGETWCH_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// UTF8 텍스트를 SN3BUF에 기록 중 임시로 사용할 UCS2 메모리 할당 실패 
	case ERROR_SN3BUF_PUTS_UTF8_TMPOUTPUT_ALLOCATION_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// UTF8 텍스트를 SN3BUF에 기록 중 임시로 사용되는 UCS2 메모리 부족 
	case ERROR_SN3BUF_PUTS_UTF8_OOPS_OUTPUT_OVERRUN:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// PDF ERROR /////////////////////////////////////////////////////////////////////////////
	// 일반적인 PDF 파일 오류
	case ERROR_SN3PDF:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// PDF 파일의 Stream Object 생성 실패
	case ERROR_SN3PDF_OPEN_INPUT_STREAM:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// PDF 파일의 Stream Object 에서 읽을 수 없는 경우 발생
	case ERROR_SN3PDF_NO_INPUT_STREAM:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// PDF 파일의 Header 정보를 읽지 못 한 경우 발생
	case ERROR_SN3PDF_ERROR_READING_PDF_HEADER:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// PDF 파일의 Xref 의 시작점을 찾지 못 함
	case ERROR_SN3PDF_READING_XREF_START:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// PDF 파일의 Xref 를 읽는 도중 에러 발생
	case ERROR_SN3PDF_READING_XREF:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// PDF 파일의 Page Catalog 정보를 읽지 못 함
	case ERROR_SN3PDF_PAGE_READING_CATALOG:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// PDF 파일의 Page Reference 정보를 읽지 못 함
	case ERROR_SN3PDF_READING_PAGE_REF:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 보안설정이 되어 있는 PDF 파일인 경우 발생
	case ERROR_SN3PDF_ENCRYPTED_PDF:
		return MPIISL_ERROR_EXTRACTION_ENCRYPTED;
	// PDF 문서의 Page Number 가 비정상적인 경우 발생
	case ERROR_SN3PDF_INVALID_PAGE_NUM:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 메모리안의 PDF 문서의 Input Stream Object 생성 실패
	case ERROR_SN3PDF_FILTER_M_INVALID_INPUT_STREAM:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// PDf 문서에서 텍스트 추출 실패
	case ERROR_SN3PDF_FILTER_M_FILTERING_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MSG ERROR /////////////////////////////////////////////////////////////////////////////
	// MSG 정보의 IPM.Note 가 비정상인 경우
	case ERROR_SN3MSG_FILTER_FS_BAD_IPM_TYPE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MSG 의 제목 읽기 실패
	case ERROR_SN3MSG_FILTER_M_FREAD_TITLE_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MP3 ERROR /////////////////////////////////////////////////////////////////////////////
	// MP3 헤더 읽기 실패
	case ERROR_SN3MP3_FILTER_M_FREAD_HEADER_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MP3 헤더 정보가 비정상인 경우
	case ERROR_SN3MP3_FILTER_M_INVALID_MP3_HEADER:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MP3 의 TAG 를 읽기 실패
	case ERROR_SN3MP3_FILTER_M_FREAD_TAG_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MP3 의 TAG 를 찾지 못 하는 경우
	case ERROR_SN3MP3_FILTER_M_NO_TAG_FOUND:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MP3 의 TAG 중 제목 읽기 실패
	case ERROR_SN3MP3_FILTER_M_FREAD_TITLE_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MP3 의 TAG 중 음악가 읽기 실패
	case ERROR_SN3MP3_FILTER_M_FREAD_ARTIST_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MP3 의 TAG 중 앨범정보 읽기 실패
	case ERROR_SN3MP3_FILTER_M_FREAD_ALBUM_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MP3 의 TAG 중 제작년도 읽기 실패
	case ERROR_SN3MP3_FILTER_M_FREAD_YEAR_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MP3 의 TAG 중 주석정보 읽기 실패
	case ERROR_SN3MP3_FILTER_M_FREAD_COMMENTS_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MP3 헤더 읽기 실패
	case ERROR_SN3MP3_DOCINFO_M_FREAD_HEADER_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MP3 헤더 정보가 비정상인 경우
	case ERROR_SN3MP3_DOCINFO_M_INVALID_MP3_HEADER:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MP3 의 TAG 를 읽기 실패
	case ERROR_SN3MP3_DOCINFO_M_FREAD_TAG_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MP3 의 TAG 를 찾지 못 하는 경우
	case ERROR_SN3MP3_DOCINFO_M_NO_TAG_FOUND:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MP3 의 TAG 중 제목 읽기 실패
	case ERROR_SN3MP3_DOCINFO_M_FREAD_TITLE_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MP3 의 TAG 중 음악가 읽기 실패
	case ERROR_SN3MP3_DOCINFO_M_FREAD_ARTIST_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MP3 의 TAG 중 앨범정보 읽기 실패
	case ERROR_SN3MP3_DOCINFO_M_FREAD_ALBUM_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MP3 의 TAG 중 제작년도 읽기 실패
	case ERROR_SN3MP3_DOCINFO_M_FREAD_YEAR_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MP3 의 TAG 중 주석정보 읽기 실패
	case ERROR_SN3MP3_DOCINFO_M_FREAD_COMMENTS_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MHT ERROR /////////////////////////////////////////////////////////////////////////////
	// MHT 파일의 헤더가 비정상인 경우
	case ERROR_SN3MHT_FILTER_M_INVALID_HEADER:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MHT 파일이 지원하지 않는 인코딩으로 되어 있는 경우
	case ERROR_SN3MHT_FILTER_M_UNSUPPORTED_ENCODING:
		return MPIISL_ERROR_EXTRACTION_UNSUPPORTED_VERSION;
	// MHT 파일이 지원하지 않는 charset 을 갖는 경우
	case ERROR_SN3MHT_FILTER_M_UNSUPPORTED_CHARSET:
		return MPIISL_ERROR_EXTRACTION_UNSUPPORTED_VERSION;
	// 정보를 다 읽지 못 하고 MULTIPART BOUNDARY 가 끝난 경우
	case ERROR_SN3MHT_FILTER_M_END_OF_MULTIPART:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MDI ERROR /////////////////////////////////////////////////////////////////////////////
	// 올바른 MDI 파일이 아닌 경우
	case ERROR_SN3MDI_FILTER_M_NOT_MDI_ERROR:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MDI 파일 읽기 실패
	case ERROR_SN3MDI_FILTER_M_FREAD_ERROR:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// LZX ERROR /////////////////////////////////////////////////////////////////////////////
	// 데이터 포맷 에러 
	case ERROR_SN3LZX_DATAFORMAT:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 데이터 
	case ERROR_SN3LZX_ILLEGALDATA:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 메모리 부족 
	case ERROR_SN3LZX_NOMEMORY:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// JTD ERROR /////////////////////////////////////////////////////////////////////////////
	// 헤더의 ID 정보가 올바르지 않는 경우 발생
	case ERROR_DOCUMENT_TEXT_INVALID_HEADER_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 통상 보존형식 텍스트의 ID 정보가 올바르지 않는 경우 발생
	case ERROR_DOCUMENT_TEXT_INVALID_RECORD_HEADER_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 메모리 부족
	case ERROR_JTD_OUT_OF_MEMORY:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 필요한 특수 문자가 없는 경우 발생 
	case ERROR_SN3JTD_ERROR_SPECIAL_DATA:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP3 ERROR ////////////////////////////////////////////////////////////////////////////
	// 비밀번호가 있는 HWP3 문서 필터링 시 발생 
	case ERROR_SN3HWP3_FILTER_M_PASSWORD_EXISTS:
		return MPIISL_ERROR_EXTRACTION_ENCRYPTED;
	// HWP3 문서 초기화 실패 
	case ERROR_SN3HWP3_FILTER_M_INIT_HWP3_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP3 문서 열기 실패 
	case ERROR_SN3HWP3_FILTER_M_HWP3_OPEN_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP3 문서 요약정보 읽기 실패 
	case ERROR_SN3HWP3_DOCINFO_M_FREAD_HWP_ID_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP3 문서 요약정보의 잘못된 파일 헤더 
	case ERROR_SN3HWP3_DOCINFO_M_INVALID_FILE_HEADER:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP3 문서 잘못된 요약정보 사이즈 
	case ERROR_SN3HWP3_DOCINFO_M_INVALID_DOCINFO_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP3 문서 요약정보 읽기 실패 
	case ERROR_SN3HWP3_DOCINFO_M_FREAD_HWP_SUMMARY_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP3 Style 정보를 읽는 도중 오류 발생
	case ERROR_SN3HWP3_FILTER_STYLEINFO_READ_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP3 그림객체 정보의 패러그래프를 읽는 도중 오류 발생
	case ERROR_SN3HWP3_FILTER_TEXTBOX_READ_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP3 v1.20 버전은 지원하지 않는다. (v2.0 부터 지원)
	case ERROR_SN3HWP3_FILTER_V120_NO_FILTER_ASSOCIATED:
		return MPIISL_ERROR_EXTRACTION_UNSUPPORTED_VERSION;
	// GZIP 처리 중 실패
	case ERROR_SN3HWP3_FILTER_GZIP_INIT:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP3 폰트 정보를 읽는 도중 오류 발생
	case ERROR_SN3HWP3_FILTER_FONTINFO_READ_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP3 문단 정보를 읽는 도중 오류 발생
	case ERROR_SN3HWP3_FILTER_PARALIST_READ_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// H2K ERROR /////////////////////////////////////////////////////////////////////////////
	// HWP },요약정보의 메모리 할당 실패 
	case ERROR_SN3H2K_DOCINFO_FS_MALLOC_STREAM_BUFFER_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP },요약정보의 속성셋 메모리 할당 실패 
	case ERROR_SN3H2K_DOCINFO_FS_MALLOC_PROPSET_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP },요약정보의 잘못된 바이트 오더 
	case ERROR_SN3H2K_DOCINFO_FS_WRONG_BYTE_ORDER:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP },요약정보의 잘못된 포맷 버전 
	case ERROR_SN3H2K_DOCINFO_FS_WRONG_FORMAT_VERSION:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP },요약정보의 잘못된 OLE 운영체제종류(0:16bit Win, 1:Macintosh, 2:32bit Win)
	case ERROR_SN3H2K_DOCINFO_FS_WRONG_OS_KIND:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP },요약정보의 잘못된 Reserved 정보 1보다 커야함 
	case ERROR_SN3H2K_DOCINFO_FS_WRONG_RESERVED:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP },요약정보의 잘못된 Section Offset
	case ERROR_SN3H2K_DOCINFO_FS_WRONG_SECTION_OFFSET:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 요약정보의 잘못된 Section Size 
	case ERROR_SN3H2K_DOCINFO_FS_WRONG_SECTION_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 요약정보의 잘못된 Section 내의 Property 개수 
	case ERROR_SN3H2K_DOCINFO_FS_WRONG_NUM_OF_PROPS:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 요약정보의 잘못된 Property ID의 배열
	case ERROR_SN3H2K_DOCINFO_FS_MALLOC_PROPSET_ID_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 요약정보의 잘못된 Property Offset의 배열
	case ERROR_SN3H2K_DOCINFO_FS_MALLOC_PROPSET_OFFSET_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 요약정보의 잘못된 Property 타입 
	case ERROR_SN3H2K_DOCINFO_FS_MALLOC_PROPSET_TYPE_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 요약정보의 잘못된 Property ID 또는 Offset 
	case ERROR_SN3H2K_DOCINFO_FS_WRONG_PROP_ID_OR_OFFSET:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 요약정보의 유니코드 문자열 메모리 할당 실패 
	case ERROR_SN3H2K_DOCINFO_FS_MALLOC_TMPWSTR_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 암호화인 경우
	case ERROR_SN3H2K_FILTER_FS_FILE_ENCRYPTED:
		return MPIISL_ERROR_EXTRACTION_ENCRYPTED;
	// HWP 2000 배포용 파일인 경우
	case ERROR_SN3H2K_FILTER_FS_FILE_DISTRIBUTION:
		return MPIISL_ERROR_EXTRACTION_UNSUPPORTED_VERSION;
	// HWP 2000 레코드 정보 읽기 실패
	case ERROR_SN3H2K_FILTER_READ_RECORD:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 문단 텍스트 정보 읽기 실패
	case ERROR_SN3H2K_FILTER_READ_PARA_TEXT:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 문단 글자정보 읽기 실패
	case ERROR_SN3H2K_FILTER_READ_PARA_CHARSHAPE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 구역 정보 읽기 실패
	case ERROR_SN3H2K_FILTER_READ_SECTION:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 GZIP 초기화 실패
	case ERROR_SN3H2K_FILTER_GZIP_INIT:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 문단헤더 메모리 할당 실패
	case ERROR_SN3H2K_FILTER_PARAREADER_INIT_MEMORY_ALLOCATION:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 글자정보 메모리 할당 실패
	case ERROR_SN3H2K_FILTER_CHAROBJECT_INIT_MEMORY_ALLOCATION:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 도형정보 메모리 할당 실패
	case ERROR_SN3H2K_FILTER_SHAPEOBJECT_INIT_MEMORY_ALLOCATION:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 배포용 문서 헤더 형식 오류.
	case ERROR_SN3H2K_FILTER_READONLY_GZIP_BAD_HEADER:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 배포용 문서 DecryptGZIP 초기화 실패
	case ERROR_SN3H2K_FILTER_READONLY_GZIP_INIT:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 사용자 지정 정보의 메모리 할당 실패 
	case ERROR_SN3H2K_USER_DOCINFO_FS_MALLOC_STREAM_BUFFER_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 사용자 지정 정보의 속성셋 메모리 할당 실패 
	case ERROR_SN3H2K_USER_DOCINFO_FS_MALLOC_PROPSET_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 사용자 지정 정보의 잘못된 바이트 오더 
	case ERROR_SN3H2K_USER_DOCINFO_FS_WRONG_BYTE_ORDER:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 사용자 지정 정보의 잘못된 Property Sets 
	case ERROR_SN3H2K_USER_DOCINFO_FS_WRONG_NUM_PROPERTY_SETS:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 사용자 지정 정보의 잘못된 Property ID의 배열
	case ERROR_SN3H2K_USER_DOCINFO_FS_MALLOC_PROPSET_ID_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 사용자 지정 정보의 잘못된 Property Offset의 배열
	case ERROR_SN3H2K_USER_DOCINFO_FS_MALLOC_PROPSET_OFFSET_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWP 2000 블록 정보 읽기 실패
	case ERROR_SN3H2K_FILTER_WRONG_BLOCK_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// GZ ERROR //////////////////////////////////////////////////////////////////////////////
	// GZ 파일의 잘못된 헤더 정보 
	case ERROR_SN3GZ_FILTER_M_FREAD_LOC_HEADER_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// GZ 파일의 잘못된 파일 시그니처
	case ERROR_SN3GZ_FILTER_M_INVALID_FILE_SIGNATURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// GZ 파일의 잘못된 파일 사이즈
	case ERROR_SN3GZ_FILTER_M_INVALID_FILE_LENGTH:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// Deprecated
	case ERROR_SN3GZ_FILTER_M_FREAD_GZ_NAME_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// Deprecated
	case ERROR_SN3GZ_FILTER_M_INVALID_COMPRESSED_LENGTH:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// GZ 파일의 잘못된 헤더 정보를 오픈할 때 발생
	case ERROR_SN3GZ_FOPEN_M_INVALID_GZ_HEADER:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// GZ 파일을 오픈할 때 MFI가 NULL이 발생하는 경우
	case ERROR_SN3GZ_FOPEN_M_NULL_MFI:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// Deprecated
	case ERROR_SN3GZ_FOPEN_M_FREAD_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// GZ 파일을 오픈할 때 메모리 할당 오류
	case ERROR_SN3GZ_FOPEN_M_MALLOC_ZFILE_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// GZ 파일을 오픈할 때 시그니처를 찾지 못한 경우
	case ERROR_SN3GZ_FOPEN_M_INVALID_SIGNATURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// GZ 파일 처리 중 파일의 끝에 도달함 
	case ERROR_SN3GZ_FOPEN_M_END_OF_FILELIST:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// GZ 파일 닫기 중 SN3GZ_FILE이 NULL 
	case ERROR_SN3GZ_FCLOSE_NULL_ZFILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// GZ 지원되지 않는 압축형식(ZIP 압축 방식이 STORED 혹은 DEFLATED 이 아님)
	case ERROR_SN3GZ_UNZIP_M_NOT_SUPPORTED_COMPRESSION:
		return MPIISL_ERROR_EXTRACTION_UNSUPPORTED_VERSION;
	// GZ 압축해제를 위한 메모리 할당 실패
	case ERROR_SN3GZ_UNZIP_M_UNCOMPRESSED_MALLOC_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// STORED 형식의 GZ 내용을 SN3MFI로부터 읽기 실패
	case ERROR_SN3GZ_UNZIP_M_STORED_DATA_FREAD_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// STORED 형식의 GZ 내용을 SN3MFI로 쓰기 실패
	case ERROR_SN3GZ_UNZIP_M_STORED_DATA_FWRITE_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// DEFLATED 형식의 GZ 내용을 SN3MFI로 쓰기 실패
	case ERROR_SN3GZ_UNZIP_M_DEFLATED_DATA_ZWRITE_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// GZ 파일 닫기 실패
	case ERROR_SN3GZ_UNZIP_M_GGZ_ZCLOSE_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// Deprecated
	case ERROR_SN3GZ_UNZIP_M_IMPOSSIBLE_PATH_FLOW:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// crc32 오류
	case ERROR_SN3GZ_UNZIP_M_CRC32:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// GUL ERROR /////////////////////////////////////////////////////////////////////////////
	// 훈민정음 파일은 아직 구현되지 않음 
	case ERROR_SN3GUL_FILTER_FS_NOT_IMPLEMENTED_YET:
		return MPIISL_ERROR_EXTRACTION_UNSUPPORTED_VERSION;
	// FLT ERROR /////////////////////////////////////////////////////////////////////////////
	// 필터링을 지원하지 않는 파일인 경우
	case ERROR_SN3FLT_FILTER_M_NO_FILTER_ASSOCIATED:
		return MPIISL_ERROR_EXTRACTION_UNKNOWN_FORMAT;
	// 필터링을 지원하지 않는 파일의 요약정보를 가져올 경우
	case ERROR_SN3FLT_DOCINFO_M_NO_FILTER_ASSOCIATED:
		return MPIISL_ERROR_EXTRACTION_UNKNOWN_FORMAT;
	// RAR 분할 압축 파일은 지원하지 않는다.
	case ERROR_SN3RAR_SPLIT_COMPRESSED_FILE:
		return MPIISL_ERROR_EXTRACTION_UNSUPPORTED_VERSION;
	// DWG ERROR /////////////////////////////////////////////////////////////////////////////
	// 파일 사이즈가 최소 사이즈보다 작음 (0x19)
	case ERROR_SN3DWG_FILTER_M_BAD_FILESIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 메모리 할당 실패
	case ERROR_SN3DWG_FILTER_M_MALLOC_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// DWG 헤더정보 읽기 실패
	case ERROR_SN3DWG_HEADER:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// DWG 파일의 지원하지 않는 버전 정보
	case ERROR_SN3DWG_HEADER_VERSION_UNKNOWN:
		return MPIISL_ERROR_EXTRACTION_UNSUPPORTED_VERSION;
	// 블락 데이터 사이즈가 파일 사이즈보다 큰 경우
	case ERROR_SN3DWG_HEADER_BAD_ENTBLOCK:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 섹션 지시번호
	case ERROR_SN3DWG_HEADER_BAD_SECLOC:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 섹션의 마지막 위치정보
	case ERROR_SN3DWG_HEADER_BAD_SENTINEL:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 파일 사이즈
	case ERROR_SN3DWG_HEADER_BAD_FILESIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 R18 영역
	case ERROR_SN3DWG_HEADER_BAD_R18FILEID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 섹션정보 압축해제를 위한 메모리 할당 실패
	case ERROR_SN3DWG_HEADER_MALLOC_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 R18 섹션 맵 헤더
	case ERROR_SN3DWG_R18_BAD_SECTMAP:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 R18 섹션 정보 헤더
	case ERROR_SN3DWG_R18_BAD_SECTINFO:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 R18 NumSectDesc 정보
	case ERROR_SN3DWG_R18_BAD_SECTDESC:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 섹션 메모리 할당 실패
	case ERROR_SN3DWG_SECT_MALLOC_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// Deprecated
	case ERROR_SN3DWG_R18_BAD_NORMSECT:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// R18 섹션 이름을 찾지 못함
	case ERROR_SN3DWG_R18_NO_SECTNAME:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// R18 섹션 버퍼를 찾지 못함
	case ERROR_SN3DWG_R18_NO_SECTBUF:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// R18의 잘못된 압축 사이즈
	case ERROR_SN3DWG_R18_DECOMP_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 R18 Summary Info
	case ERROR_SN3DWG_R18_BAD_SUMMARY:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 CRC
	case ERROR_SN3DWG_BAD_CRC:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 DWG R1315 Object
	case ERROR_SN3DWG_BAD_OBJECTS:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 DWG R1315 Object
	case ERROR_SN3DWG_BAD_OBJECT_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// Deprecated
	// ERROR_SN3DWG_HEADER_BAD_ENTBLOCK와 동일
	//case ERROR_SN3DWG_FILTER_FS_NOT_IMPLEMENTED_YET:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 DWG R2004 섹션데이터
	case ERROR_SN3DWG_BAD_SECTION:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// DOCX ERROR ////////////////////////////////////////////////////////////////////////////
	// 압축 해제된 파일을 위한 SN3MFI 열기 실패
	case ERROR_SN3DOCX_CANNOT_OPEN_UNZIPFILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// DOCX 파일로부터 압축 해제된 파일 열기 실패
	case ERROR_SN3DOCX_CANNOT_ARCHIVE_ZIP:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// DOCX 파일로부터 압축 해제된 XML파일 파싱시 오류 발생
	case ERROR_SN3DOCX_CANNOT_PARSE_XML:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// DOCX 파일 내부의 매크로 필터링 실패
	case ERROR_SN3DOCX_CANNOT_OVBA_MACRO_PARSE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// DOC ERROR /////////////////////////////////////////////////////////////////////////////
	// FIB 정보를 읽는 도중 오류 발생
	case ERROR_SN3DOC_FILTER_FS_FIB_READ_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 지원하지 않는 Word 버전
	case ERROR_SN3DOC_FILTER_FS_BAD_WORD_VERSION:
		return MPIISL_ERROR_EXTRACTION_UNSUPPORTED_VERSION;
	// 암호화된 DOC 파일
	case ERROR_SN3DOC_FILTER_FS_FILE_ENCRYPTED:
		return MPIISL_ERROR_EXTRACTION_ENCRYPTED;
	// CHM ERROR /////////////////////////////////////////////////////////////////////////////
	// CHM 파일을 위한 SN3MFI 열기 실패
	case ERROR_SN3CHM_CANNOT_OPEN_CHMFILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// Deprecated Error 
	case ERROR_SN3ZIP_FILTER_M_INVALID_COMPRESSED_LENGTH:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// ZIP 파일 열기 시 SN3MFI가 NULL 
	case ERROR_SN3ZIP_FOPEN_M_NULL_MFI:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3MFI로 부터 파일의 내용 읽기 실패 
	case ERROR_SN3ZIP_FOPEN_M_FREAD_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3ZIP_FILE 구조체를 위한 메모리 할당 실패 
	case ERROR_SN3ZIP_FOPEN_M_MALLOC_ZFILE_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// ZIP 파일에 ZIP 파일 시그니쳐(0x02014b50)가 없음 
	case ERROR_SN3ZIP_FOPEN_M_INVALID_SIGNATURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// ZIP 파일에 ZIP 파일 시그니쳐(0x02014b50)가 없음 
	case ERROR_SN3ZIP_FOPEN_M_MALLOC_FILENAME_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// ZIP 파일이름을 위한 메모리 할당 실패 
	case ERROR_SN3ZIP_FOPEN_M_MALLOC_EXTRAFIELD_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// ZIP 파일 처리 중 파일의 끝에 도달함 
	case ERROR_SN3ZIP_FOPEN_M_END_OF_FILELIST:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// ZIP 파일 닫기 중 SN3ZIP_FILE가 NULL 
	case ERROR_SN3ZIP_FCLOSE_NULL_ZFILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 지원되지 않는 압축형식(ZIP 압축 방식이 STORED 혹은 DEFLATED 이 아님)
	case ERROR_SN3ZIP_UNZIP_M_NOT_SUPPORTED_COMPRESSION:
		return MPIISL_ERROR_EXTRACTION_UNSUPPORTED_VERSION;
	// ZIP 압축해제를 위한 메모리 할당 실패
	case ERROR_SN3ZIP_UNZIP_M_UNCOMPRESSED_MALLOC_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// STORED 형식의 ZIP 내용을 SN3MFI로부터 읽기 실패
	case ERROR_SN3ZIP_UNZIP_M_STORED_DATA_FREAD_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// STORED 형식의 ZIP 내용을 SN3MFI로 쓰기 실패
	case ERROR_SN3ZIP_UNZIP_M_STORED_DATA_FWRITE_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// DEFLATED 형식의 ZIP 내용을 SN3MFI로 쓰기 실패
	case ERROR_SN3ZIP_UNZIP_M_DEFLATED_DATA_ZWRITE_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// DEFLATED 형식의 ZIP 내용을 SN3MFI로 쓰기 실패
	case ERROR_SN3ZIP_UNZIP_M_GZIP_ZCLOSE_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// Deprecated Error 
	case ERROR_SN3ZIP_UNZIP_M_IMPOSSIBLE_PATH_FLOW:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 깨진 ZIP 파일 
	case ERROR_SN3ZIP_FOPEN_M_BROKEN_ZIP_FILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// zip 암호화인 경우
	case ERROR_SN3ZIP_FILTER_FS_FILE_ENCRYPTED:
		return MPIISL_ERROR_EXTRACTION_ENCRYPTED;
	// ZIP 파일 내에 해당 파일이 없음
	case ERROR_SN3ZIP_FILE_NOT_FOUND:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// ZIP 파일의 central directory signature를 찾지 못함
	case ERROR_SN3ZIP_NOT_FOUND_END_SIG:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// ZIP 파일의 uncompress size 가 0 일 경우
	case ERROR_SN3ZIP_UNCOMPRESS_SIZE_ZERO:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// ZIP 파일 해제중 생긴 오류
	case ERROR_SN3ZIP_UNZIP_STRM_ERROR:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3FMT ERROR ////////////////////////////////////////////////////////////////////////////
	// 암호화된 office 2007 파일  
	case ERROR_SN3FMT_ENCRYPT_OFFICE:
		return MPIISL_ERROR_EXTRACTION_ENCRYPTED;
	// XLSX ERROR ////////////////////////////////////////////////////////////////////////////
	// 압축 해제된 파일을 위한 SN3MFI 열기 실패
	case ERROR_SN3XLSX_CANNOT_OPEN_UNZIPFILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// XLSX 파일로부터 압축 해제된 파일 열기 실패
	case ERROR_SN3XLSX_CANNOT_ARCHIVE_ZIP:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// XLSX 파일로부터 압축 해제된 XML파일 파싱시 오류 발생
	case ERROR_SN3XLSX_CANNOT_PARSE_XML:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// XLSX 텍스트 출력 버퍼가 NULL
	case ERROR_SN3XLSX_OUTPUT_BUFFER_NULL:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// XLSX 메모리 부족
	case ERROR_SN3XLSX_MEMORY_ALLOC_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// XLS ERROR /////////////////////////////////////////////////////////////////////////////
	// 암호화된 XLS 파일  
	case SN3XLS_ERROR_ENCRYPT_EXCEL:
		return MPIISL_ERROR_EXTRACTION_ENCRYPTED;
	case SN3XLS_ERROR_ENCRYPT_HANCELL:
		return MPIISL_ERROR_EXTRACTION_ENCRYPTED;
	case ERROR_SN3XLS_MEMORY_ALLOC_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// TAR ERROR /////////////////////////////////////////////////////////////////////////////
	// TAR 파일 내의 특정 블럭의 크기가 512 미만임
	case ERROR_SN3TAR_FILTER_M_INVALID_BLOCK_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SXX ERROR /////////////////////////////////////////////////////////////////////////////
	// OpenOffice 파일 필터링 중 XML 파싱 오류
	case ERROR_SN3SXX_CANNOT_PARSE_XML:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// OpenOffice 압축 파일을 SN3MFI로 열기 실패
	case ERROR_SN3SXX_CANNOT_OPEN_UNZIPFILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// OpenOffice 압축 파일 내 특정 xml 파일을 찾지 못함 
	case ERROR_SN3SXX_CANNOT_ARCHIVE_ZIP:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 압축 파일이 OpenOffice 파일이 아님 
	case ERROR_SN3SXX_IS_NOT_SXX_FILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 암호화된 OpenOffice 파일 입니다.
	case ERROR_SN3SXX_IS_ENCRYPTED_FILE:
		return MPIISL_ERROR_EXTRACTION_ENCRYPTED;
	// SWF ERROR /////////////////////////////////////////////////////////////////////////////
	// 잘못된 SWF 파일(파일 내 특정 정보가 없음) 
	case ERROR_SN3SWF_LOAD_FILENOT_SWF:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 알 수 없는 SWF 파일 버전
	case ERROR_SN3SWF_LOAD_VERSION_UNKNOWN:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 필터링을 위한 메모리 할당 실패
	case ERROR_SN3SWF_LOAD_MALLOC_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 SWF 파일(파일의 길이가 파일 스펙과 틀림)
	case ERROR_SN3SWF_LOAD_BAD_FILESIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3SUM ERROR //////////////////////////////////////////////////////////////////////////
	// SN3SUM 구조체를 위한 메모리 할당 실패
	case ERROR_SN3SUM_INIT_MEMORY_ALLOCATION_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3SUM 구조체 메모리 해제 시 SN3SUM이 NULL
	case ERROR_SN3SUM_FREE_SUMMARY_IS_NULL:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// SN3SUM 내용을 쓰기 위한 FILE 열기 실패
	case ERROR_SN3SUM_UNLOAD_FILE_OPEN_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MS Office 2007 문서의 문서 정보 읽기 중 문서 파일을 SN3MFI로 열기 실패
	case ERROR_SN3SUM_CANNOT_OPEN_UNZIPFILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MS Office 2007 압축 파일 내 문서정보 XML 파일이 없음
	case ERROR_SN3SUM_CANNOT_ARCHIVE_ZIP:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MS Office 2007 문서정보 XML 파싱 실패
	case ERROR_SN3SUM_CANNOT_PARSE_XML:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// Format NDOC ERROR /////////////////////////////////////////////////////////////////////////// 
	// Encrypt된 NDOC 문서의 헤더정보를 Decrypt할 수 없는경우
	case ERROR_NDOC_CANNOT_DECRYPT_HEADER:
		return MPIISL_ERROR_EXTRACTION_ENCRYPTED;
	// RTF ERROR /////////////////////////////////////////////////////////////////////////////
	// RTF Mark-up 문자 '}'가 잘못 됨
	case ERROR_SN3RTF_FILTER_M_STACK_UNDERFLOW:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// RTF Mark-up 문자 '{'가 '}' 보다 많음
	case ERROR_SN3RTF_FILTER_M_STACK_OVERFLOW:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// RTF 파일 필터링 중 RTF Mark-up 문자 '}'없이 문서의 마지막에 도달함
	case ERROR_SN3RTF_FILTER_M_UNMATCHED_BRACE: // RTF ended during an open group.
	// RTF 파일 내 잘못된 16진수 문자열이 있음
	case ERROR_SN3RTF_FILTER_M_INVALID_HEX: // invalid hex character found in data
	// RTF 파일 내 잘못된 정보가 있음
	case ERROR_SN3RTF_FILTER_M_BAD_TABLE: // RTF table (sym or prop) invalid
	// RTF 파일 파싱 오류
	case ERROR_SN3RTF_FILTER_M_ASSERTION_FAILURE: // Assertion failure
	// RTF 파일 파싱 중 파일의 끝에 도달함
	case ERROR_SN3RTF_FILTER_M_END_OF_FILE: // End of file reached while reading RTF 
	// PPTX ERROR ////////////////////////////////////////////////////////////////////////////
	// 압축 해제된 파일을 위한 SN3MFI 열기 실패
	case ERROR_SN3PPTX_CANNOT_OPEN_UNZIPFILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// DOCX 파일로부터 압축 해제된 파일 열기 실패
	case ERROR_SN3PPTX_CANNOT_ARCHIVE_ZIP:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// PPTX 파일로부터 압축 해제된 XML파일 파싱시 오류 발생
	case ERROR_SN3PPTX_CANNOT_PARSE_XML:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	//////////////////////////////////////////////////////////////////////////////////////////
	// XPS ERROR ////////////////////////////////////////////////////////////////////////////
	// 압축 해제된 파일을 위한 SN3MFI 열기 실패
	case ERROR_SN3XPS_CANNOT_OPEN_UNZIPFILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// XPS 파일로부터 압축 해제된 파일 열기 실패
	case ERROR_SN3XPS_CANNOT_ARCHIVE_ZIP:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// XPS 파일로부터 압축 해제된 XML파일 파싱시 오류 발생
	case ERROR_SN3XPS_CANNOT_PARSE_XML:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	//////////////////////////////////////////////////////////////////////////////////////////
	// PPT ERROR ////////////////////////////////////////////////////////////////////////////
	// PPT의 암호화인 경우 
	case ERROR_SN3PPT_FILTER_FS_FILE_ENCRYPTED:
		return MPIISL_ERROR_EXTRACTION_ENCRYPTED;
	//  잘못된 Atom이 존재하는 경우 오류 발생
	case ERROR_SN3PPT_FOUND_BAD_ATOM:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	//  잘못된 Offset 값을 참조하는 경우
	case ERROR_SN3PPT_INVALID_OFFSET:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 slidelist 정보
	case ERROR_SN3PPT_FOUND_BAD_SLIDE_LIST:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 디렉토리 엔트리
	case ERROR_SN3PPT_FOUND_BAD_DIR_ENTRY:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 Offset
	case ERROR_SN3PPT_FOUND_BAD_OFFSET:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 메모리 할당 실패
	case ERROR_SN3PPT_MEMORY_ALLOC_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 헤더 타입
	case ERROR_SN3PPT_INVALID_HEADER_TYPE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 헤더 길이
	case ERROR_SN3PPT_INVALID_HEADER_LENGTH:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_SN3PPT_INVALID_CUSTREAM:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_SN3PPT_INVALID_LUES:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_SN3PPT_INVALID_MASTER_IDX:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_SN3PPT_FAILD_OLE_DECODE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 잘못된 레코드 헤더
	case ERROR_SN3PPT_WRONG_RECORD_HEADER:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	//////////////////////////////////////////////////////////////////////////////////////////
	// BZIP ERROR  ///////////////////////////////////////////////////////////////////////////
	// BZIPFILE OpenError
	case ERROR_SN3BZIP_CANNOT_OPEN_BZIPFILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// BZIPFILE Read Error
	case ERROR_SN3BZIP_CANNOT_READ_BZIPFILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// BZIPFILE Read Get Unused
	case ERROR_SN3BZIP_CANNOT_READ_UNUSED:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// BZIPFILE Close
	case ERROR_SN3BZIP_CANNOT_CLOSE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// Memory Allocation Fail
	case ERROR_SN3BZIP_MEM_ALLOC_FAILED:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	//////////////////////////////////////////////////////////////////////////////////////////
	// ALZIP ERROR  ///////////////////////////////////////////////////////////////////////////
	// ALZIP Noerror 
	//case ERROR_SN3ALZ_NOERR:
	//	return SYNAP_CATEGORIZED_NO_ERROR;
	// GENERAL ERROR
	case ERROR_SN3ALZ_GENERAL:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 파일열기 실패
	case ERROR_SN3ALZ_CANT_OPEN_FILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 
	case ERROR_SN3ALZ_CANT_OPEN_DEST_FILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 깨진 알집 파일
	case ERROR_SN3ALZ_CORRUPTED_FILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// ALZIP 이 아님.
	case ERROR_SN3ALZ_NOT_ALZ_FILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// alz signature 읽기 실패
	case ERROR_SN3ALZ_CANT_READ_SIG:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// alz 헤더를 읽을 수 없음
	case ERROR_SN3ALZ_CANT_READ_FILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// alz 헤더를 읽을 수 없는 경우
	case ERROR_SN3ALZ_AT_READ_HEADER:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// alz 잘못된 파일 이름 길이
	case ERROR_SN3ALZ_INVALID_FILENAME_LENGTH:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// alz 헤더에서 디렉토리를 읽을 수 없음
	case ERROR_SN3ALZ_CANT_READ_CENTRAL_DIRECTORY_STRUCTURE_HEAD:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// alz 메모리 할당 실패
	case ERROR_SN3ALZ_MEM_ALLOC_FAILED:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// alz BZIP2 파싱 실패
	case ERROR_SN3ALZ_BZIP2_FAILED:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// alz 풀수 없는 압축방식
	case ERROR_SN3ALZ_UNKNOWN_COMPRESSION_METHOD:
		return MPIISL_ERROR_EXTRACTION_UNSUPPORTED_VERSION;
	// alz 로컬파일의 헤더를 읽을 수 없음
	case ERROR_SN3ALZ_CANT_READ_LOCAL_FILE_HEAD:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// alz 암호화인 경우
	case ERROR_SN3ALZ_FILTER_FS_FILE_ENCRYPTED:
		return MPIISL_ERROR_EXTRACTION_ENCRYPTED;
	//////////////////////////////////////////////////////////////////////////////////////////
	// OLE10NATIVE ERROR  ///////////////////////////////////////////////////////////////////////////
	// signature OLE파일이 아님
	case ERROR_SN3OLE10NATIVE_NOT_OLE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// signature native stream을 읽기 실패
	case ERROR_SN3OLE10NATIVE_STREAM_READ_FAIL:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// signature 메모리가 충분하지 못하여 native stream 읽기 실패
	case ERROR_SN3OLE10NATIVE_NOT_ENOUGH_MEM:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// OLENATIVE10 에서 Native Data Block Read 실패	
	case ERROR_SN3OLE10NATIVE_UNKNOWN:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// OLENATIVE10 에서 Native Data Filtering Fail
	case ERROR_SN3OLE10NATIVE_FILTER_FAIL:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// WPD ERROR  ///////////////////////////////////////////////////////////////////////////
	case ERROR_SN3WPD_FAIL_READ_HEADER:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_SN3WPD_BAD_PAIR_FUNC_DOC:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_SN3WPD_INVALID_HEADER_VERSION:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_SN3WPD_NOT_DOCUMENT_TYPE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 7ZIP ERROR  ///////////////////////////////////////////////////////////////////////////
	// GENERAL ERROR
	case ERROR_SN3SEVENZIP_GENERAL:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 파일열기 실패
	case ERROR_SN3SEVENZIP_CANT_OPEN_FILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 
	case ERROR_SN3SEVENZIP_CANT_OPEN_DEST_FILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 깨진 압축 파일
	case ERROR_SN3SEVENZIP_CORRUPTED_FILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// signature 읽기 실패
	case ERROR_SN3SEVENZIP_CANT_READ_SIG:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_SN3SEVENZIP_UNKNOWN_COMPRESSION_METHOD:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// sevenzip 암화화인 경우
	case ERROR_SN3SEVENZIP_FILTER_FS_FILE_ENCRYPTED:
		return MPIISL_ERROR_EXTRACTION_ENCRYPTED;
	// 압축 해제중 CRC 오류가 발생한 경우
	case ERROR_SN3SEVENZIP_FILTER_BAD_CRC:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_SN3SEVENZIP_DATA:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_SN3SEVENZIP_MEM:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_SN3SEVENZIP_UNSUPPORTED:
		return MPIISL_ERROR_EXTRACTION_UNSUPPORTED_VERSION;
	case ERROR_SN3SEVENZIP_PARAM:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_SN3SEVENZIP_INPUT_EOF:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_SN3SEVENZIP_FAIL:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_SN3SEVENZIP_ARCHIVE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_SN3SEVENZIP_UNSUPPORTED_LZMA2:
		return MPIISL_ERROR_EXTRACTION_UNSUPPORTED_VERSION;
	// RAR ERROR  ///////////////////////////////////////////////////////////////////////////
	// GENERAL ERROR
	case ERROR_SN3RAR_GENERAL:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 파일열기 실패
	case ERROR_SN3RAR_CANT_OPEN_FILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 
	case ERROR_SN3RAR_CANT_OPEN_DEST_FILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 깨진 압축 파일
	case ERROR_SN3RAR_CORRUPTED_FILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// signature 읽기 실패
	case ERROR_SN3RAR_CANT_READ_SIG:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_SN3RAR_CANT_READ_FILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_SN3RAR_UNKNOWN_COMPRESSION_METHOD:
		return MPIISL_ERROR_EXTRACTION_UNSUPPORTED_VERSION;
	// rar 암화화인 경우
	case ERROR_SN3RAR_FILTER_FS_FILE_ENCRYPTED:
		return MPIISL_ERROR_EXTRACTION_ENCRYPTED;
	// 압축 해제중 CRC 오류가 발생한 경우
	case ERROR_SN3RAR_FILTER_BAD_CRC:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_SN3RAR_FAIL:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MDB ERROR  ///////////////////////////////////////////////////////////////////////////
	// 필터링 중 암호가 설정된 파일인경우
	case ERROR_SN3MDB_FILTER_M_PASSWORD_EXISTS:
		return MPIISL_ERROR_EXTRACTION_ENCRYPTED;
	// 필터링 중 MDB파일의 테이블이 깨진경우
	case ERROR_SN3MDB_FILTER_M_BROKEN_TABLE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 필터링 중 MDB파일의 테이블 정보를 읽을 수 없는경우
	case ERROR_SN3MDB_FILTER_M_READ_TABLE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// 지원하지 않는 JET DB인경우
	case ERROR_SN3MDB_FOPEN_M_UNKNOWN_JET_VERSION:
		return MPIISL_ERROR_EXTRACTION_UNSUPPORTED_VERSION;
	// MDB의 레코드가 정상적이지 않은 경우
	case ERROR_SN3MDB_FILTER_M_INVALID_RECORD:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MDB파일의 signature를 인식할 수 없는 경우
	case ERROR_SN3MDB_FOPEN_M_INVALID_SIGNATURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MDB파일의 다음 페이지 읽기 실패
	case ERROR_SN3MDB_READ_NEXT_PAGE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// OLE_CONTENTS ERROR  ///////////////////////////////////////////////////////////////////////////
	// signature OLE파일이 아님
	case ERROR_SN3OLE_CONTENTS_NOT_OLE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// signature MFI 을 OLE파일에 MOUNT 할 떄 실패
	case ERROR_SN3OLE_CONTENTS_MOUNT:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// signature OLE파일 stream open 실패
	case ERROR_SN3OLE_CONTENTS_STREAM_OPEN:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// signature OLE파일 stream size check 실패
	case ERROR_SN3OLE_CONTENTS_STREAM_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	/////////////////////////////////////////////////////////////////////////////////////////
	// 파일의 끝이 아니지만 알 수 없는 이유로 파일을 읽기 실패
	case ERROR_DGN_READ:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	//////////////////////////////////////////////////////////////////////////////////////////
	// MACRO ERROR ///////////////////////////////////////////////////////////////////////////
	case ERROR_PROJECT_SYSKIND_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_SYSKIND_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_LCID_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_LCID_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_LCIDINVOKE_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_LCIDINVOKE_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_CODEPAGE_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_CODEPAGE_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_NAME_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_NAME_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_DOCSTRING_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_DOCSTRING_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_DOCSTRING_UNICODE_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_HELPFILE1_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_HELPFILE1_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_HELPFILE2_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_CONTEXT_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_CONTEXT_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_LIBFLAGS_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_LIBFLAGS_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_VERSION_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_VERSION_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_CONSTANTS_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_CONSTANTS_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_CONSTANTS_UNICODE_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_CHUNK_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// REFERENCE
	case ERROR_REFERENCE_NAME_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_REFERENCE_ORIGINAL_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_REFERENCE_CONTROL_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_REFERENCE_CONTROL_INVALID_RESERVED1:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_REFERENCE_CONTROL_INVALID_RESERVED2:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_REFERENCE_CONTROL_INVALID_RESERVED3:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_REFERENCE_CONTROL_INVALID_RESERVED4:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_REFERENCE_CONTROL_INVALID_RESERVED5:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_REFERENCE_REGISTERED_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_REFERENCE_REGISTERED_INVALID_RESERVED1:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_REFERENCE_REGISTERED_INVALID_RESERVED2:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_REFERENCE_PROJECT_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// MODULE
	case ERROR_PROJECT_MODULES_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_MODULES_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_COOKIE_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_PROJECT_COOKIE_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_MODULE_NAME_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_MODULE_NAME_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_MODULE_NAME_UNICODE_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_MODULE_NAME_UNICODE_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_MODULE_STREAMNAME_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_MODULE_STREAMNAME_UNICODE_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_MODULE_DOCSTRING_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_MODULE_DOCSTRING_UNICODE_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_MODULE_OFFSET_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_MODULE_OFFSET_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_MODULE_HELPCONTEXT_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_MODULE_HELPCONTEXT_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_MODULE_COOKIE_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_MODULE_COOKIE_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_MODULE_TYPE_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_MODULE_TYPE_INVALID_SIZE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	case ERROR_MODULE_END_INVALID_ID:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	//HEADER
	case ERROR_COMPRESS_CURRENT_INVALID_HEADER: // cumpressBuffer 의 첫번째 바이트가 0x01 이 아닐 경우
		return MPIISL_ERROR_EXTRACTION_FATAL;
	//////////////////////////////////////////////////////////////////////////////////////////
	// XML 파싱 에러
	case ERROR_SN3XML_STATUS:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// XML 해당 엘리먼트 없음
	case ERROR_SN3XML_NO_ELEMENTS:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	//SN3XML ERROR  ///////////////////////////////////////////////////////////////////////////
	//IWORK ERROR ////////////////////////////////////////////////////////////////////////////
	// xml 파일을 읽을 버퍼 할당 실패
	case ERROR_SN3IWORK_NO_MEMMORY:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// buffer에 xml파일 읽기 실패
	case ERROR_SN3IWORK_CANNOT_READ_FILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// xml DomTree 생성 실패
	case ERROR_SN3IWORK_CANNOT_PARSE_TREE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	//////////////////////////////////////////////////////////////////////////////////////////
	//KEYNOTE ERROR ////////////////////////////////////////////////////////////////////////////
	// 압축 해제된 파일을 위한 SN3MFI 열기 실패
	case ERROR_SN3KEYNOTE_CANNOT_OPEN_UNZIPFILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// KEYNOTE 파일로부터 압축 해제된 파일 열기 실패
	case ERROR_SN3KEYNOTE_CANNOT_ARCHIVE_ZIP:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// KEYNOTE 파일로부터 압축 해제된 XML파일 파싱시 오류 발생
	case ERROR_SN3KEYNOTE_CANNOT_PARSE_XML:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// xml 파일을 읽을 버퍼 할당 실패
	case ERROR_SN3KEYNOTE_NO_MEMMORY:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	//////////////////////////////////////////////////////////////////////////////////////////
	// PAGES ERROR ////////////////////////////////////////////////////////////////////////////
	// 압축 해제된 파일을 위한 SN3MFI 열기 실패
	case ERROR_SN3PAGES_CANNOT_OPEN_UNZIPFILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// PAGES 파일로부터 압축 해제된 파일 열기 실패
	case ERROR_SN3PAGES_CANNOT_ARCHIVE_ZIP:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// PAGES 파일로부터 압축 해제된 XML파일 파싱시 오류 발생
	case ERROR_SN3PAGES_CANNOT_PARSE_XML:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// xml 파일을 읽을 버퍼 할당 실패
	case ERROR_SN3PAGES_NO_MEMMORY:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	//////////////////////////////////////////////////////////////////////////////////////////
	// NUMBERS ERROR ////////////////////////////////////////////////////////////////////////////
	// 압축 해제된 파일을 위한 SN3MFI 열기 실패
	case ERROR_SN3NUMBERS_CANNOT_OPEN_UNZIPFILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// NUMBERS 파일로부터 압축 해제된 파일 열기 실패
	case ERROR_SN3NUMBERS_CANNOT_ARCHIVE_ZIP:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// NUMBERS 파일로부터 압축 해제된 XML파일 파싱시 오류 발생
	case ERROR_SN3NUMBERS_CANNOT_PARSE_XML:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// xml 파일을 읽을 버퍼 할당 실패
	case ERROR_SN3NUMBERS_NO_MEMMORY:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	//////////////////////////////////////////////////////////////////////////////////////////
	// DRM ERROR ////////////////////////////////////////////////////////////////////////////
	// DRM 문서는 지원하지 않습니다.
	case ERROR_SN3FMT_DRM_DOCUMENT:
		return MPIISL_ERROR_EXTRACTION_DRM;
	//////////////////////////////////////////////////////////////////////////////////////////
	// KEYNOTE ERROR ////////////////////////////////////////////////////////////////////////////
	// 압축 해제된 파일을 위한 SN3MFI 열기 실패
	case ERROR_SN3HWPX_CANNOT_OPEN_UNZIPFILE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWPX 파일로부터 압축 해제된 파일 열기 실패
	case ERROR_SN3HWPX_CANNOT_ARCHIVE_ZIP:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	// HWPX 파일로부터 압축 해제된 XML파일 파싱시 오류 발생
	case ERROR_SN3HWPX_CANNOT_PARSE_XML:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	//////////////////////////////////////////////////////////////////////////////////////////
	// XLSB ERROR ////////////////////////////////////////////////////////////////////////////
	case ERROR_SN3XLSB_MEMORY_ALLOC_FAILURE:
		return MPIISL_ERROR_EXTRACTION_FATAL;
	//////////////////////////////////////////////////////////////////////////////////////////
	// COMMON ERROR ////////////////////////////////////////////////////////////////////////////
	// 현재 버전에서 지원하지 않음
	case ERROR_NOT_SUPPORTED_IN_CURRENT_VERSION:
		return MPIISL_ERROR_EXTRACTION_UNSUPPORTED_VERSION;
	default:
		return MPIISL_ERROR_EXTRACTION_UNKNOWN;
	}
}
