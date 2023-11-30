/***************************************************************
 *
 *	SYNAP NEXT Filter
 *	Copyright (C) since 2001 Synapsoft Corp. Confidential.
 *
 *	Author Email:
 *    iverson13@synapsoft.co.kr
 *
 *  History:
 *    2004/08/09 - Original Version
 *    2004/12/14 - Mobidic (mobidic@synapsoft.co.kr)
 *    2013/04/12 - UmmI (iverson13@synapsoft.co.kr)
 *
 *	이 프로그램은 (주)사이냅소프트 자산입니다.
 *  (주)사이냅소프트의 서면 동의없이 복제하거나
 *  부분 도용할 수 없습니다.
 *
 **************************************************************/

#ifndef SNF_H
#define SNF_H

/***************************************************************
 * Include Headers
 **************************************************************/
#include <stdio.h>

/***************************************************************
 * File Format Code
 **************************************************************/
#define SN3FMT_ALZIP_START		120100
#define SN3FMT_ALZIP_END		120200

#define SN3FMT_BZIP_START		19300
#define SN3FMT_BZIP_END			19321

#define SN3FMT_CHM_START		90100
#define SN3FMT_CHM_END			90200

#define SN3FMT_DOC_START		60000
#define SN3FMT_DOC_END			60100

#define SN3FMT_DOCX_START		300100
#define SN3FMT_DOCX_END			300200

#define SN3FMT_DWG_START		70000
#define SN3FMT_DWG_END			70100

#define SN3FMT_GUL_START		60400
#define SN3FMT_GUL_END			60500

#define SN3FMT_GZ_START			18000
#define SN3FMT_GZ_END			18100

#define SN3FMT_H2K_START		60300
#define SN3FMT_H2K_ENCRYPTED	60305
#define SN3FMT_H2K_END			60310

#define SN3FMT_HTM_START		37500
#define SN3FMT_HTM_END			37900

#define SN3FMT_HWD_START		39100
#define SN3FMT_HWD_END			39200

#define SN3FMT_HWN_START		140200
#define SN3FMT_HWN_END			140300

#define SN3FMT_HWP3_START		60310
#define SN3FMT_HWP3_ENCRYPTED	60320
#define SN3FMT_HWP3_END			60390

#define SN3FMT_HWX_START		140100
#define SN3FMT_HWX_END			140200

#define SN3FMT_IWD_START		60600
#define SN3FMT_IWD_END			60700

#define SN3FMT_JTD_START		600800
#define SN3FMT_JTD_END			600900

#define SN3FMT_MDB_START		160100
#define SN3FMT_MDB_END			160200

#define SN3FMT_MDI_START		100100
#define SN3FMT_MDI_END			100200

#define SN3FMT_MHT_START		38000
#define SN3FMT_MHT_END			38300

#define SN3FMT_MP3_START		10000
#define SN3FMT_MP3_END			10600

#define SN3FMT_MSG_START		200100
#define SN3FMT_MSG_END			200200

#define SN3FMT_PDF_START		35200
#define SN3FMT_PDF_ENCRYPTED	35220
#define SN3FMT_PDF_END			35300

#define SN3FMT_PPT_START		60100
#define SN3FMT_PPT_END			60200

#define SN3FMT_PPTX_START		300500
#define SN3FMT_PPTX_END			300600

#define SN3FMT_PPTM_START	311000
#define SN3FMT_PPTM_END		311020
#define SN3FMT_XLSM_START	321000
#define SN3FMT_XLSM_END		321030
#define SN3FMT_XLAM_START	321030
#define SN3FMT_XLAM_END		321060

#define SN3FMT_XPS_START	300600
#define SN3FMT_XPS_PIECE	300601
#define SN3FMT_XPS_END		300700

#define SN3FMT_MSO_ENCXML_START 300700
#define SN3FMT_MSO_ENCXML_END 300800

#define SN3FMT_OLE10NATIVE_START	130100
#define SN3FMT_OLE10NATIVE_END		130200

#define SN3FMT_OLE_PACKAGE_START	130300
#define SN3FMT_OLE_PACKAGE_END	130400

#define SN3FMT_OLE_OCXDATA_START	130500
#define SN3FMT_OLE_OCXDATA_END	130600

#define SN3FMT_OLE_CONTENTS_START	170100
#define SN3FMT_OLE_CONTENTS_END		170200

#define SN3FMT_SHOW_START	300800
#define SN3FMT_SHOW_END		300900

#define SN3FMT_NXL_START	300900
#define SN3FMT_NXL_END		301000

#define SN3FMT_CELL_START	301000
#define SN3FMT_CELL_END		301100

#define SN3FMT_CELL2014_START	301100
#define SN3FMT_CELL2014_END		301200

#define SN3FMT_HWPX_START	301200
#define SN3FMT_HWPX_END		301300

#define SN3FMT_RTF_START		37300
#define SN3FMT_RTF_END			37400

#define SN3FMT_7Z_START			150100
#define SN3FMT_7Z_END			150200

#define SN3FMT_SWF_START		20800
#define SN3FMT_SWF_END			20900

#define SN3FMT_SXC_START		80200
#define SN3FMT_SXC_ENCRYPTED_START     80250
#define SN3FMT_SXC_ENCRYPTED_END       80300
#define SN3FMT_SXC_END			80300

#define SN3FMT_SXI_START		80300
#define SN3FMT_SXI_ENCRYPTED_START     80350
#define SN3FMT_SXI_ENCRYPTED_END       80400
#define SN3FMT_SXI_END			80400

#define SN3FMT_SXW_START		80100
#define SN3FMT_SXW_ENCRYPTED_START     80150
#define SN3FMT_SXW_ENCRYPTED_END       80200
#define SN3FMT_SXW_END			80200

#define SN3FMT_NDOC_START		90000
#define SN3FMT_NDOC_ENCRYPT		90010
#define SN3FMT_NDOC_END			90100

#define SN3FMT_NDOC2_START		90500
#define SN3FMT_NDOC2_ENCRYPT	90510
#define SN3FMT_NDOC2_END		90600

#define SN3FMT_NPPT_START		90300
#define SN3FMT_NPPT_END			90400

#define SN3FMT_NXLS_START		90400
#define SN3FMT_NXLS_END			90500

#define SN3FMT_TAR_START		17900
#define SN3FMT_TAR_END			18000

#define SN3FMT_TXT_START		50000
#define SN3FMT_TXT_END			51000

#define SN3FMT_TXT_ASCII     50000
#define SN3FMT_TXT_ASCII_NON_ISO 50001 
#define SN3FMT_TXT_ASCII_EBDIC 50002 
#define SN3FMT_TXT_ASCII_INEBDIC 50003
#define SN3FMT_TXT_UTF8      50100
#define SN3FMT_TXT_UCS2LE    50200
#define SN3FMT_TXT_UCS4LE    50201
#define SN3FMT_TXT_UCS2BE    50300
#define SN3FMT_TXT_UCS4BE    50301
#define SN3FMT_TXT_UCS42143  50302
#define SN3FMT_TXT_UCS43412  50303
#define SN3FMT_TXT_EUCJP     50400
#define SN3FMT_TXT_EUCKR     50401
#define SN3FMT_TXT_GB18030   50500
#define SN3FMT_TXT_CP1251    50600
#define SN3FMT_TXT_ISO8859   50610
#define SN3FMT_TXT_ISO8859_1   50611
#define SN3FMT_TXT_ISO8859_2   50612
#define SN3FMT_TXT_ISO8859_3   50613
#define SN3FMT_TXT_ISO8859_4   50614
#define SN3FMT_TXT_ISO8859_5   50615
#define SN3FMT_TXT_ISO8859_6   50616
#define SN3FMT_TXT_ISO8859_7   50617
#define SN3FMT_TXT_ISO8859_8   50618
#define SN3FMT_TXT_ISO8859_9   50619
#define SN3FMT_TXT_ISO8859_10   50620
#define SN3FMT_TXT_ISO8859_11   50621
#define SN3FMT_TXT_ISO8859_13   50623
#define SN3FMT_TXT_ISO8859_14   50624
#define SN3FMT_TXT_ISO8859_15   50625
#define SN3FMT_TXT_ISO8859_16   50626
#define SN3FMT_TXT_SJIS      50700
#define SN3FMT_TXT_BIG5      50800
#define SN3FMT_TXT_ISO2022JP 50900

#define SN3FMT_VTT_START	52000
#define SN3FMT_VTT_END		52100

#define SN3FMT_WPD_START		110402
#define SN3FMT_WPD_END			119999

#define SN3FMT_XLS_START		60200
#define SN3FMT_XLS_END			60300

#define SN3FMT_XLSX_START		300300
#define SN3FMT_XLSX_END			300400

#define SN3FMT_XML_START		37900
#define SN3FMT_XML_END			38000

#define SN3FMT_XML_HWP_START	37950
#define SN3FMT_XML_HWP_END		37960

#define SN3FMT_EVERNOTE_START	37960
#define SN3FMT_EVERNOTE_END		37970

#define SN3FMT_XML_OFFICE_START	37910
#define SN3FMT_XML_OFFICE_END	37930

#define SN3FMT_ZIP_START		13100
#define SN3FMT_ZIP_END			13200

#define SN3FMT_RAR_START		13000
#define SN3FMT_RAR_END			13002

#define SN3FMT_DGN_START		180100
#define SN3FMT_DGN_END			180200

#define SN3FMT_OVBA_START		190100
#define SN3FMT_OVBA_END			190200

#define SN3FMT_DCM_START		190300
#define SN3FMT_DCM_END			190400

#define SN3FMT_PST_START		190500
#define SN3FMT_PST_END			190600

#define SN3FMT_KEYNOTE_START	190700
#define SN3FMT_KEYNOTE_END		190800

#define SN3FMT_PAGES_START		190900
#define SN3FMT_PAGES_END		191000

#define SN3FMT_NUMBERS_START	191100
#define SN3FMT_NUMBERS_END		191200

#define SN3FMT_DRM_START		191300
#define SN3FMT_DRM_END			191400

#define SN3FMT_FASOO_DRM_START	191500
#define SN3FMT_FASOO_DRM_END	191600

#define SN3FMT_BAT_START	29300
#define SN3FMT_BAT_END		29400

#define SN3FMT_XDW_START	191600
#define SN3FMT_XDW_END		191700

#define SN3FMT_WRI_START	191700
#define SN3FMT_WRI_END		191800

#define SN3FMT_EMS_START	191800
#define SN3FMT_EMS_END		191900

#define SN3FMT_EGG_START	191900
#define SN3FMT_EGG_END		192000

#define SN3FMT_PAGES_13_START	192000
#define SN3FMT_PAGES_13_END		192100

#define SN3FMT_KEYNOTE_13_START	192200
#define SN3FMT_KEYNOTE_13_END	192300

#define SN3FMT_NUMBERS_13_START	192400
#define SN3FMT_NUMBERS_13_END	192500

#define SN3FMT_SOFTCAMP_DRM_START	192500
#define SN3FMT_SOFTCAMP_DRM_END		192600

#define SN3FMT_PAGES_14_START	192600
#define SN3FMT_PAGES_14_END		192700

#define SN3FMT_KEYNOTE_14_START	192700
#define SN3FMT_KEYNOTE_14_END	192800

#define SN3FMT_NUMBERS_14_START	192800
#define SN3FMT_NUMBERS_14_END	192900

#define SN3FMT_ISO_START	192900
#define SN3FMT_ISO_END		193000

#define SN3FMT_MP4_START	193200
#define SN3FMT_MP4_END		193300

#define SN3FMT_MO_START	193300
#define SN3FMT_MO_END	193310

#define SN3FMT_BIFF2_START	193500 // BIFF 2.0 ~ 8.0
#define SN3FMT_BIFF2_END	193600

#define SN3FMT_NSF_START	193600
#define SN3FMT_NSF_END		193700

#define SN3FMT_EDB_START	193700
#define SN3FMT_EDB_END		193800

#define SN3FMT_VCF_START	193900
#define SN3FMT_VCF_END		194000

#define SN3FMT_HDR_START	194000
#define SN3FMT_HDR_END		194100

#define SN3FMT_VMDK_START	194100
#define SN3FMT_VMDK_END		194200

#define SN3FMT_PBL_START	194200
#define SN3FMT_PBL_END		194300

#define SN3FMT_XLSB_START	301300
#define SN3FMT_XLSB_END		301400

#define SN3FMT_POTX_START	301400
#define SN3FMT_POTX_END		301430
#define SN3FMT_POTM_START	301430
#define SN3FMT_POTM_END		301460
#define SN3FMT_PPSX_START	301460
#define SN3FMT_PPSX_END		301490
#define SN3FMT_PPSM_START	301490
#define SN3FMT_PPSM_END		301520
#define SN3FMT_PPAM_START	301590
#define SN3FMT_PPAM_END		301595
#define SN3FMT_THMX_START	301595
#define SN3FMT_THMX_END		301600

#define SN3FMT_DOC_ENCRYPTED_START	60050
#define SN3FMT_DOC_ENCRYPTED_END	60100

#define SN3FMT_PPT_ENCRYPTED_START	60150
#define SN3FMT_PPT_DEFAULT_ENCRYPTED	60160
#define SN3FMT_PPT_ENCRYPTED_END	60200

#define SN3FMT_XLS_ENCRYPTED_START	60250
#define SN3FMT_XLS_DEFAULT_ENCRYPTED	60260
#define SN3FMT_XLS_ENCRYPTED_END	60300

#define SN3FMT_JPEG_START	26600
#define SN3FMT_JPEG_END		26700

#define SN3FMT_PNG_START	23000
#define SN3FMT_PNG_END		23200

#define SN3FMT_GIF_START	23200
#define SN3FMT_GIF_END		23300

#define SN3FMT_BMP_START	24600
#define SN3FMT_BMP_END		24601

#define SN3FMT_ICON_START	33500
#define SN3FMT_ICON_END		33600

/***************************************************************
 * CHECK FILE TYPE
 **************************************************************/
#define SN3FILETYPE_ALL			0xffffffffffffffffLL
#define SN3FILETYPE_MP3			0x0000000000000001LL
#define SN3FILETYPE_ZIP			0x0000000000000002LL
#define SN3FILETYPE_TAR			0x0000000000000008LL

#define SN3FILETYPE_GZ			0x0000000000000010LL
#define SN3FILETYPE_TXT			0x0000000000000020LL
#define SN3FILETYPE_RTF			0x0000000000000040LL
#define SN3FILETYPE_HTM			0x0000000000000080LL

#define SN3FILETYPE_XML			0x0000000000000100LL
#define SN3FILETYPE_MHT			0x0000000000000200LL
#define SN3FILETYPE_PDF			0x0000000000000800LL

#define SN3FILETYPE_HWD			0x0000000000001000LL
#define SN3FILETYPE_DOC			0x0000000000002000LL
#define SN3FILETYPE_PPT			0x0000000000004000LL
#define SN3FILETYPE_XLS			0x0000000000008000LL

#define SN3FILETYPE_H2K			0x0000000000010000LL
#define SN3FILETYPE_HWP3		0x0000000000020000LL
#define SN3FILETYPE_CHM			0x0000000000080000LL

#define SN3FILETYPE_DWG			0x0000000000100000LL
#define SN3FILETYPE_SXW			0x0000000000200000LL
#define SN3FILETYPE_SXC			0x0000000000400000LL
#define SN3FILETYPE_SXI			0x0000000000800000LL

#define SN3FILETYPE_MDI			0x0000000001000000LL
#define SN3FILETYPE_MSG			0x0000000002000000LL
#define SN3FILETYPE_DOCX		0x0000000004000000LL
#define SN3FILETYPE_XLSX		0x0000000008000000LL

#define SN3FILETYPE_PPTX		0x0000000010000000LL
#define SN3FILETYPE_SWF			0x0000000020000000LL
#define SN3FILETYPE_JTD			0x0000000040000000LL
#define SN3FILETYPE_WPD			0x0000000080000000LL

#define SN3FILETYPE_BZIP		0x0000000100000000LL
#define SN3FILETYPE_ALZIP		0x0000000200000000LL
#define SN3FILETYPE_OLE10NATIVE	0x0000000400000000LL
#define SN3FILETYPE_HWX			0x0000000800000000LL

#define SN3FILETYPE_HWN			0x0000001000000000LL
#define SN3FILETYPE_OFFICE_XML	0x0000002000000000LL
#define SN3FILETYPE_HWP_HML		0x0000004000000000LL
#define SN3FILETYPE_7Z			0x0000008000000000LL

#define SN3FILETYPE_NDOC		0x0000010000000000LL
#define SN3FILETYPE_MDB			0x0000020000000000LL
#define SN3FILETYPE_RAR			0x0000040000000000LL

#define SN3FILETYPE_OLE_CONTENTS	0x0000080000000000LL

#define SN3FILETYPE_DGN			0x0000100000000000LL
#define SN3FILETYPE_OVBA		0x0000200000000000LL
#define SN3FILETYPE_DCM			0x0000400000000000LL

#define SN3FILETYPE_NPPT		0x0000800000000000LL
#define SN3FILETYPE_NXLS		0x0001000000000000LL

#define SN3FILETYPE_PST			0x0002000000000000LL

#define SN3FILETYPE_KEYNOTE		0x0004000000000000LL
#define SN3FILETYPE_PAGES		0x0008000000000000LL
#define SN3FILETYPE_NUMBERS		0x0010000000000000LL

#define SN3FILETYPE_SHOW		0x0020000000000000LL
#define SN3FILETYPE_NXL			0x0040000000000000LL
#define SN3FILETYPE_CELL		0x0080000000000000LL

#define SN3FILETYPE_BAT			0x0100000000000000LL
#define SN3FILETYPE_XPS			0x0200000000000000LL
#define SN3FILETYPE_HWPX		0x0400000000000000LL

#define SN3FILETYPE_KEYNOTE13	0x1000000000000000L
#define SN3FILETYPE_PAGES13		0x2000000000000000L
#define SN3FILETYPE_NUMBERS13	0x4000000000000000L

#define SN3FILETYPE_XLSB		0x0800000000000000L

/***************************************************************
 * CHECK FILTERING OPTIONS
 **************************************************************/
#define SN3OPTION_ARCHIVE_EXTRACT		0x000001
#define SN3OPTION_ARCHIVE_FILELIST		0x000002
#define SN3OPTION_EXTENSION_CHECK		0x000008

#define SN3OPTION_EXTENSION_NO_CHECK	0x000010
#define SN3OPTION_EMBEDED_OLE_FILTER	0x000020
#define SN3OPTION_MAIL_ATTACH_FILTER	0x000080

#define SN3OPTION_ARCHIVE_NOFILENAME	0x000100
#define SN3OPTION_EMBEDED_ATTACH_FILTER	0x000200
#define SN3OPTION_PPT_EXTRACTALL		0x000800

#define SN3OPTION_EXCEL_SEPARATE		0x001000
#define SN3OPTION_COMPRESSION_SIZE_LIMIT					0x002000
#define SN3OPTION_EXCEL_NOLIMIT					0x004000
#define SN3OPTION_COMPRESSION_ARCHIVE_LEVEL_LIMIT			0x008000

#define SN3OPTION_COMPRESSION_EXTRACT_SIZE_LIMIT			0x010000
#define SN3OPTION_NO_USE_SPACE_REMOVER						0x020000
#define SN3OPTION_COMPRESSION_IGNORE_FILE_ERROR				0x040000
#define SN3OPTION_EMBEDED_OLE_SEPARATE						0x080000

#define SN3OPTION_DEF_TXT_ENCODING							0x100000
#define SN3OPTION_BODY_EXTRACT								0x200000
#define SN3OPTION_SHOW_MAILMETATAG							0x400000
#define SN3OPTION_WITHPAGE									0x800000

#define SN3OPTION_PST_EMAIL									0x01000000
#define SN3OPTION_PST_EMAIL_ATTACH							0x02000000
#define SN3OPTION_PST_CALENDAR								0x04000000
#define SN3OPTION_PST_CONTACT								0x08000000

#define SN3OPTION_MACRO_NOT_USED							0x10000000
#define SN3OPTION_EXCEL_SEPARATE_EMPTY_CELL					0x20000000
#define SN3OPTION_SHOW_ARCHIVE_FILEPATH						0x40000000
#define SN3OPTION_SHOW_ARCHIVE_RETURNCODE					0x80000000

#ifdef SN3_OS_MS_WIN32
#define SN3OPTION_COMPRESSION_IGNORE_EXTENSION_LIST			0x100000000L	// 압축파일 내 파일 확장자 제거 옵션
#define SN3OPTION_NO_WITHPAGE								0x200000000L	// PDF 페이지 문자열 제거 옵션
#define SN3OPTION_ANNOTATION_SEPARATE						0x400000000L	// Annotation Marking
#define SN3OPTION_HTM_NO_SEPCIAL_CHAR						0x800000000L	// HTM파일 &lt; &gt;를 태그처럼 처리하는 옵션
#define SN3OPTION_EXCEL_USE_FILTERCACHE						0x1000000000L	// XLS파일 cache data 필터링 on/off 옵션
#define SN3OPTION_EXCEL_USE_FILTERPHONETIC					0x2000000000L	// XLS파일 윗주 필터링 on/off 옵션
#define SN3OPTION_ARCHIVE_RETURNCODE_CHECK					0x4000000000L	// 압축 파일의 리턴코드가 SN3OK 가 아니면 40101 리턴
#define SN3OPTION_DB_EMPTY_SEPARATE							0x8000000000L
#define SN3OPTION_DONT_USE_EXCEPTION_HANDLING				0x10000000000L	// out of exception handling
#define SN3OPTION_EXTRACT_HYPERLINK							0x20000000000L  // 하이퍼링크 추출(only PDF)
#define SN3OPTION_EXCEL_FILTER_FORMULA						0x40000000000L  // 엑셀파일에서 수식 함수문장을 추출하는 옵션
#define SN3OPTION_MAIL_MULTI_FILTER							0x80000000000L // EML, MHT 내의 모든 내용을 다 추출하는 옵션
#define SN3OPTION_USE_NUMBER_FORMAT							0x100000000000L // 표시형식 모듈을 이용하여 렌더링
#define SN3OPTION_BOOKMARKER								0x200000000000L // 책갈피 필터링 옵션 
#define SN3OPTION_PDF_BOOKMARKER							0x200000000000L // PDF 책갈피 필터링 옵션
#define SN3OPTION_PDF_COORD_BASED_OUTPUT					0x400000000000L // PDF 좌표 기준 출력
#define SN3OPTION_XML_TAG_FILTER							0x800000000000L // XML 파일 태그 필터링 옵션
#define SN3OPTION_WITHPAGE_SHEETNAME						0x1000000000000L // 'SHEET:시트이름' 필터링 옵션
#define SN3OPTION_IGNORE_REPEATED_IMAGE						0x2000000000000L // 반복되는 이미지는 무시하는 옵션
#else
#define SN3OPTION_COMPRESSION_IGNORE_EXTENSION_LIST			0x100000000LL
#define SN3OPTION_NO_WITHPAGE								0x200000000LL
#define SN3OPTION_ANNOTATION_SEPARATE						0x400000000LL
#define SN3OPTION_HTM_NO_SEPCIAL_CHAR						0x800000000LL
#define SN3OPTION_EXCEL_USE_FILTERCACHE						0x1000000000LL
#define SN3OPTION_EXCEL_USE_FILTERPHONETIC					0x2000000000LL
#define SN3OPTION_ARCHIVE_RETURNCODE_CHECK					0x4000000000LL
#define SN3OPTION_DB_EMPTY_SEPARATE							0x8000000000LL
#define SN3OPTION_DONT_USE_EXCEPTION_HANDLING				0x10000000000LL	// out of exception handling
#define SN3OPTION_EXTRACT_HYPERLINK							0x20000000000LL  // 하이퍼링크 추출(only PDF)
#define SN3OPTION_EXCEL_FILTER_FORMULA						0x40000000000LL  // 엑셀파일에서 수식 함수문장을 추출하는 옵션
#define SN3OPTION_MAIL_MULTI_FILTER							0x80000000000LL // EML, MHT 내의 모든 내용을 다 추출하는 옵션
#define SN3OPTION_USE_NUMBER_FORMAT							0x100000000000LL // 표시형식 모듈을 이용하여 렌더링
#define SN3OPTION_BOOKMARKER								0x200000000000LL // 책갈피 필터링 옵션 
#define SN3OPTION_PDF_BOOKMARKER							0x200000000000LL // PDF 책갈피 필터링 옵션
#define SN3OPTION_PDF_COORD_BASED_OUTPUT					0x400000000000LL // PDF 좌표 기준 출력
#define SN3OPTION_XML_TAG_FILTER							0x800000000000LL // XML 파일 태그 필터링 옵션
#define SN3OPTION_WITHPAGE_SHEETNAME						0x1000000000000LL // 'SHEET:시트이름' 필터링 옵션
#define SN3OPTION_IGNORE_REPEATED_IMAGE						0x2000000000000LL // 반복되는 이미지는 무시하는 옵션
#endif



/***************************************************************
 * Encoding Character 
 **************************************************************/
#define SN3UCS_INVALID		-1
#define SN3UCS_UNICODE		0
#define	SN3UCS_MSCP949		1
#define	SN3UCS_UTF8			11

#define	SN3UCS_EUCJP		12
#define	SN3UCS_SJIS			13
#define	SN3UCS_BIG5			14
#define	SN3UCS_GB2312		15
#define	SN3UCS_ISO2022JP	16


/***************************************************************
 * Local Definition
 **************************************************************/
#define SN3OK	0
#define ERROR_SN3_NOT_HAVE_LICENSE	11111;

#define	SN3_SEEK_SET	SEEK_SET
#define	SN3_SEEK_CUR	SEEK_CUR
#define	SN3_SEEK_END	SEEK_END

#define	SN3MFI_SEEK_SET		SN3_SEEK_SET
#define	SN3MFI_SEEK_CUR		SN3_SEEK_CUR
#define	SN3MFI_SEEK_END		SN3_SEEK_END

/***************************************************************
 * User define callback function
 **************************************************************/
#define SN3_USER_STOP 30001
#define SN3_USER_CONTINUE SN3OK


#define  __int64 long long

typedef	unsigned char		__uint8;
typedef	unsigned short		__uint16;
typedef	__uint16			__ucs2;
typedef	unsigned int		__uint32;
#ifndef BUILD_aCC
typedef signed int			__int32;
#endif
typedef signed int			__sint32;
typedef unsigned __int64	__uint64;

typedef struct SN3MFI SN3MFI;
typedef struct SN3BUF SN3BUF;
typedef struct SN3ARFILIST SN3ARFILIST;


/**
* @brief	옵션들이 사용할 param을 저장하는 구조체 (배포)
*/
typedef struct t_SN3OPTION_PARAM{ 
	__int64 MaxCompressionFileSize;		/**< 필터링할 압축파일의 최대크기(<일 때만 필터링) -1 : 제한 없음 */
	__int64 MaxFileSizeToExtract;		/**< 필터링할 압축된 파일의 최대 크기(<일 때만 필터링) -1 : 제한없음 */
	__int32 MaxArchiveLevel;			/**< 필터링할 압축 깊이(<일 때만 필터링) -1 : 제한없음 */
	__int32 MinArchiveSizeLimitLevel;	/**< 제한이 적용될 최소 압축 깊이(>일 때만 제한) */
	__int32 TextEncoding;				/**< 기본 텍스트 인코딩 (텍스트 파일 해석용) */
	__int32 DefaultEncoding;			/**< 기본 인코딩 */
	__int32 ArchiveFileNameEncoding;	/**< 압축파일 내 파일 이름 인코딩 */
	__int32 MaxCellLimitXLSX;			/**< xlsx 셀 갯수 제한 */
	const char *ignoreExtList;			/**< 무시 대상 확장자 목록 */
}SN3OPTION_PARAM;

/**
 * @brief	문서정보를 담을 구조체
 */
typedef struct t_SN3SUM {
	__int32 	Format;			/**< SN3 파일포맷 */
	__int32 	Format2;		/**< SN3 파일포맷 */
	__ucs2* Title;				/**< 제목 */
	__ucs2* Subject;			/**< 주제 */
	__ucs2* Author;				/**< 저자 */
	__ucs2* Date;				/**< 날짜 정보 */
	__ucs2* Keywords;			/**< 키워드 */
	__ucs2* Comments;			/**< 설명 */
	__ucs2* Template;			/**< 템플릿 */
	__ucs2* LastAuthor;			/**< 최종 수정자 */
	__ucs2* RevNumber;			/**< 문서 버전 */
	__ucs2* AppName;			/**< 응용프로그램명 */
	__ucs2* CreateDTM;			/**< 생성일자 */
	__ucs2* LastSaveDTM;		/**< 문서 최종 수정일자 */
	__ucs2* AppVersion;			/**< 응용프로그램 버전 */
	__ucs2* contentStatus;		/**< 콘텐츠 상태 */
	__ucs2* pages;				/**< 페이지 수 */
	__ucs2* language;			/**< 언어 */
	__ucs2* words;				/**< 단어 수 */
	__ucs2* paragraphs;			/**< 문단 수 */
	__ucs2* lines;				/**< 라인 수 */
	__ucs2* characters;			/**< 문자 수 */
} SN3SUM;

/**
 * @brief	마커 콜백 - 상태값
 */
typedef enum {
	FILE_START_STATE = 1,	/**< FILE의 시작 상태 */
	FILE_END_STATE = 2,		/**< FILE의 끝 상태 */
	OLE_START_STATE = 3,	/**< OLE의 시작 상태 */
	OLE_END_STATE = 4,		/**< OLE의 끝 상태 */
	PAGE_START_STATE = 5,	/**< PAGE의 시작 상태 */
	PAGE_END_STATE = 6,		/**< PAGE의 끝 상태 */
	UNZIP_FILE_STATE = 9,	/**< 압축 파일 내 개별 파일 unzip 상태 */
	ATTACHMENT_FILE_STATE = 10,	/**< 첨부파일 마커 콜백 시점 */
} SN3BUF_STATE_TYPE;

/**
 * @brief	마커 콜백 - 스킵 명령어
 */
typedef enum {
	NO_SKIP = 0,		/**< default */
	MARKER_SKIP = 1,	/**< 마커값 스킵 */
	CONTENT_SKIP = 2,	/**< 필터링 스킵 */
	ALL_SKIP = 3		/**< 마커값과 필터링 모두 스킵 */
} SN3BUF_SKIP_TYPE;

/**
 * @brief	마커정보를 담은 구조체
 */
typedef struct t_SN3MARKER {
	int state;				/**< 상태값(시작, 끝) */
	__ucs2* marker;			/**< 마커값(파일이름, 페이지번호, ole마커값) */
	SN3MFI* unzipMFI;		/**< unzip file stream */
	int depth;				/**< 압축 파일 내 개별 파일의 depth */
	int ret;				/**< 압축 (첨부) 파일의 필터링 결과 코드 */
}SN3MARKER;

/**
 * @brief	이미지 정보를 담은 구조체
 */
typedef struct t_SN3IMGINFO {
	__int32 index;			/**< 이미지 index */
	__int32 formatCode;		/**< 이미지 포맷코드 */
	__uint32 width;			/**< 이미지 너비 */
	__uint32 height;		/**< 이미지 높이 */
} SN3IMGINFO;

/**
* @brief	구분자 타입
*/
typedef enum {
	SNF_GBL_SEPTYPE_NONE = 0,					/**< 없음 */
	SNF_GBL_SEPTYPE_EXCEL_CELL = 1,				/**< 엑셀 cell */
	SNF_GBL_SEPTYPE_EXCEL_ROW = 2,				/**< 엑셀 row */
	SNF_GBL_SEPTYPE_EXCEL_FORMULA_START = 3,	/**< 엑셀 수식 시작 */
	SNF_GBL_SEPTYPE_EXCEL_FORMULA_END = 4,		/**< 엑셀 수식 끝 */
	SNF_GBL_SEPTYPE_OLE_START = 5,				/**< ole 시작 */
	SNF_GBL_SEPTYPE_OLE_END = 6,				/**< ole 끝 */
	SNF_GBL_SEPTYPE_ANNOTATION_START = 7,		/**< 주석 시작 */
	SNF_GBL_SEPTYPE_ANNOTATION_END = 8,			/**< 주석 끝 */
	SNF_GBL_SEPTYPE_EXCEL_PIVOT_START = 9,		/**< 엑셀 피벗테이블 시작 */
	SNF_GBL_SEPTYPE_EXCEL_PIVOT_END = 10,		/**< 엑셀 피벗테이블 끝 */
	SNF_GBL_SEPTYPE_EXCEL_CACHE_START = 11,		/**< 엑셀 캐시 시작 */
	SNF_GBL_SEPTYPE_EXCEL_CACHE_END = 12,		/**< 엑셀 캐시 끝 */
	SNF_GBL_SEPTYPE_BOOKMARKER_START = 13,		/**< 북마커 시작 */
	SNF_GBL_SEPTYPE_BOOKMARKER_END = 14,		/**< 북마커 끝 */
	SNF_GBL_SEPTYPE_HYPERLINK_START = 15,		/**< 하이퍼링크 시작 */
	SNF_GBL_SEPTYPE_HYPERLINK_END = 16,			/**< 하이퍼링크 끝 */
} SNF_GBL_SEPTYPE;

/***************************************************************
 * Function Declarations
 ***************************************************************/
#ifdef __cplusplus
extern "C" {
#endif //__cplusplus

/**************************************************************
*                  SNF(V4 이상) API 함수                      *
***************************************************************/

// Config //////////////////////////////////////////////////////
/**
* 현재 설정 정보를 출력한다.
*/
void snf_gbl_showcfg();
/**
 * 필터 구동 환경 설정을 한다.
 * @param pKeyStr 라이센스 번호. 이제는 사용하지 않아 NULL 또는 ""입력.
 * @param Option  필터 제어 옵션. Or로 중복 지정 가능하다.
 * @param FileType 필터링 대상 파일 설정. SN3FILETYPE_ALL을 제외하고 Or로 중복 지정 가능하다.
 * @param BaseBufSize 메모리 버퍼 크기.
 */
void snf_gbl_setcfg(const char * pKeyStr, __uint64 FileType, __uint64 Option, size_t BaseBufSize);
/**
 * 필터 구동 환경 및 압축파일 필터 옵션을 설정한다.
 * @param pKeyStr 라이센스 번호. 이제는 사용하지 않아 NULL 또는 ""입력.
 * @param FileType 필터링 대상 파일 설정.
 * @param Option  필터 제어 옵션
 * @param BaseBufSize 필터링시 사용되는 버퍼 크기.
 * @param opt	  압축 파일 필터링, 압축 해제 관련 SN3OPTION_PARAM 구조체
 */
void snf_gbl_setcfgEx(const char * pKeyStr, __uint64 FileType, __uint64 Option, size_t BaseBufSize, SN3OPTION_PARAM opt);
/**
* 필터링시 작업 디렉토리를 활용한다.
* @details 이 API로 작업 디렉토리를 사용하면 압축 파일 해제시 메모리가 아니라 임시 파일을 활용하게 된다.
*		   성능에는 약간의 패널티가 있지만 메모리 사용량이 줄어든다.
* @param workDir 작업 디렉토리 경로 (이미 존재하는 디렉토리여야 함)
* @param enc 1이면 작업 디렉토리에 임시 파일 생성 시 파일 내용을 암호화
* @param minSize 해당 값보다 큰 파일만 임시 파일을 사용하게 된다. 100MB 이상 값 권장.
* @return 필터링 성공 시 SN3OK, 실패시 오류코드를 반환한다.
*/
int snf_gbl_set_work_dir(const __uint8* pWorkDir, int enc, __int64 minSize);
/**
* type에 맞는 구분자를 세팅한다.
* @param type 설정할 구분자 종류
* @param separator 구분자
* @return 필터의 구분자를 정상적으로 설정한 경우 SN3OK, 실패시 오류코드를 반환한다.
*/
int snf_gbl_set_separator(const SNF_GBL_SEPTYPE type, const __ucs2* separator);

// Utility /////////////////////////////////////////////////////
/**
* 필터 이름을 구한다.
* @return	필터 이름을 리턴한다.
*/
char* snf_ver_program();
/**
* 필터 버전을 구한다.
* @return	필터 버전을 리턴한다.
*/
char* snf_ver_version();

/**
 * MFI 포인터로부터 파일 포맷을 알아낸다.
 * MFI의 현재 위치를 기억했다가 다시 되돌린다.
 * @param	pMFI	MFI 포인터
 * @param   pFormat	포맷코드가 저장된다.
 * @return	정상적인경우 SN3OK 반환.
 *			오류가발생한경우는 해당 오류코드를 반환.
 */
int snf_fmt_detect_m(SN3MFI *pMFI, int *pFormat);
/**
 * 파일의 로컬경로로부터 파일 포맷을 알아낸다.
 * @param	pFilePath	FILE 경로
 * @param   pFormat	포맷코드가 저장된다.
 * @return	정상적인경우 SN3OK 반환.
 *			오류가 발생한 경우는 해당 오류코드를 반환.
 */
int snf_fmt_detect(__uint8 *pFilePath, int *pFormat);
/**
* 파일의 로컬경로로부터 파일 포맷을 알아낸다.
* @param	pFilePath	FILE 경로(유니코드 경로)
* @param   pFormat	포맷코드가 저장된다.
* @return	정상적인경우 SN3OK 반환.
* 오류가 발생한 경우는 해당 오류코드를 반환.
*/
int snf_fmt_wdetect(__ucs2 *pFilePath, int *pFormat);
/**
 * FormatCode 로부터 포맷의 이름을 찾는다.
 * @param	pFormatCode	포맷코드
 * @return	성공한경우 포맷의 이름을 반환하고
 *          실패한경우 오류코드를 반환한다.
 */
char* snf_fmt_format_name(int pFormatCode);

/**
 * FormatCode 로부터 포맷의 이름을 찾는다. 실제 지원하는 포맷만 찾는다.
 * @param	pFormatCode	포맷코드
 * @return	성공한경우 포맷의 이름을 반환하고
 *          실패한경우 오류코드를 반환한다.
 */
char* snf_fmt_formatcodeByName(int _formatCode);

/**
* 파일 경로를 이용해 실제 필터링이 가능한 파일인지 true/false 리턴
* @param pFilePath  FILE 경로
* @return 필터링이 가능하면 1, 아니면 0을 반환한다.
*/
int snf_fmt_isFilterFormat(__uint8 *pFilePath);
/**
* MFI에 담긴 값이 실제 필터링이 가능한지 true/false 리턴
* @param pMFI  MFI 포인터
* @return 필터링이 가능하면 1, 아니면 0을 반환한다.
*/
int snf_fmt_isFilterFormat_m(SN3MFI *pMFI);

/**
 * Next 에러코드가 (ERROR_SN3XXX_) 잘못된 파일(깨진 파일)의 경우인지 확인한다.
 * @param	nErr	에러코드
 * @return	잘못된 파일(깨진 파일) 경우 양의 정수를 반환.
 *          아닐경우 0을 반환
 */
int snf_err_isbadfile(int nErr);

/**
 * 유니코드(UCS2-LE) 문자열을 cp949 문자열로 변형.
 * @param	wstr	변환될 UCS2 문자열. 반드시 0x0000으로 끝나야 한다.
 * @return	정상적으로 변환된경우 cp949의 포인터를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
char* snf_ucs_ucs2cp949(__ucs2 *wstr);
/**
* @brief MS-CP949 문자열 포인터를 입력 받아 ucs2 문자열 포인터를 반환
*
* MS-CP949 문자열을 ucs2 문자열로 변환한다.
* 반환 받은 포인터는 반드시 sn3utl_free() 를 이용해 해제해야 한다.
*
* @param pUtf8 입력 utf8 문자열.
* @see sn3utf8_to_ucs2(), sn3utf8_to_ucs2_loop(), sn3utl_free()
* @return ucs2 문자열 포인터
*/
__ucs2* snf_cp949_to_ucs2_str(__uint8 *pCp949);
/**
* 변환시킨 유니코드 문자열을 메모리 해제한다.
* @param	pMem  메모리 해제할 유니코드 문자열
*/
void snf_utl_free(void *pMem);
/**
 * UCS2-LE 문자열의 길이를 반환한다.
 * @param	string	유니코드 문자열의 포인터
 * @return	입력된 유니코드 문자열의 길이를 반환.
 */
size_t snf_ucs_wcslen(__ucs2 *string );
/**
* 유니코드 문자열을 디코딩한다.
* @param wstr 입력 UTF-8
* @param encoding 인코딩 종류
* @return 디코딩된 결과가 ucs2 문자열로 반환
*/
__uint8* snf_ucs_decode_str(__ucs2 *wstr, int encoding);
/**
* ucs2 문자열을 지정한 utf8 문자열 포인터로 변환한다.
* @param wstr 입력
* @param wlen 입력 길이
* @param dest 출력할 utf 문자열
* @param dlen 출력 길이
* @param encoding 인코딩 종류
* @return 성공: SN3OK, 실패: ERROR_UTF8_FROM_UCS2_LOOP_FULL_OUTPUT
*/
int snf_ucs_decode(__ucs2 *wstr, int wlen, __uint8* dest, int dlen, int encoding);

/**
* @brief utf8 문자열 포인터를 입력 받아 ucs2 문자열 포인터를 반환
*
* utf8 문자열을 ucs2 문자열로 변환한다.
* 반환 받은 포인터는 반드시 sn3utl_free() 를 이용해 해제해야 한다.
*
* @param pUtf8 입력 utf8 문자열.
* @see sn3utf8_to_ucs2(), sn3utf8_to_ucs2_loop(), sn3utl_free()
* @return ucs2 문자열 포인터
*/
__ucs2* snf_utf8_to_ucs2_str(__uint8 *pUtf8);

// SN3MFI ///////////////////////////////////////////////////////
// mfi open&close
/**
 * SN3MFI 객체를 생성(메모리할당)하고 Default 값으로 초기화 한다.
 * @param	ppMFI	SN3MFI 포인터의 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_mfi_fopen_rw(SN3MFI **ppMFI);
/**
 * SN3MFI 객체를 생성(메모리할당)하고 메모리 파일의 내용으로 초기화 한다.
 * @param	pMemFile 메모리 파일 포인터
 * @param pMemSize 메모리 파일의 크기
 * @param ppMFI SN3MFI 포인터의 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_mfi_fopen_m(__uint8 *pMemFile, __int64 pMemSize, SN3MFI **ppMFI);
/**
 * SN3MFI 메모리 파일의 내용의 소유권을 이전받아 MFI를 초기화 한다.
 * @param	pMemFile malloc으로 할당받은 메모리 파일 포인터
 * @param pMemSize 메모리 파일의 크기
 * @param ppMFI SN3MFI 포인터의 포인터
 * @return	정상적으로 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_mfi_fopen_move_m(__uint8 *pMemFile, __int64 pMemSize, SN3MFI **ppMFI);
/**
 * SN3MFI 객체를 생성(메모리할당)하고 파일의 내용으로 초기화 한다.
 * @param	pFilePath 파일명
 * @param ppMFI SN3MFI 포인터의 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_mfi_fopen(__uint8 *pFilePath, SN3MFI **ppMFI);
/**
 * SN3MFI 객체를 생성(메모리할당)하고 파일의 내용으로 초기화 한다.
 * @param	pFilePath 멀티바이트 파일명
 * @param ppMFI SN3MFI 포인터의 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_mfi_wfopen(__ucs2 *pFilePath, SN3MFI **ppMFI);
/**
 * SN3MFI 객체를 파괴(메모리반환)한다.
 * @param pMFI SN3MFI 포인터
 * @return	정상적으로 메모리가 반환된 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_mfi_fclose(SN3MFI *pMFI);

// mfi misc
/**
 * SN3MFI 객체의 현재 파일 포지션을 처음으로 보낸다.
 * @param pMFI SN3MFI 포인터
 */
void snf_mfi_rewind(SN3MFI *pMFI);
/**
 * SN3MFI 객체의 파일 포지션을 설정 플래그에 따라 특정 위치로 설정한다.
 * 가능한 설정 플래그는 SN3MFI_SEEK_SET, SN3MFI_SEEK_CUR, SN3MFI_SEEK_END
 * 중 하나여야 한다.
 * @param pMFI SN3MFI 포인터
 * @param pOffset 새 포지션
 * @param pOrigin 포지션 설정 플래그
 * @return	pMFI의 파일 포지션이 제대로 설정될 수 있다면 SN3OK를
 *					아니면 해당 오류를 반환.
 */
__int64 snf_mfi_fseek(SN3MFI *pMFI, __int64 pOffset, int pOrigin);
/**
 * SN3MFI 객체의 파일 크기를 리턴한다.
 * @param pMFI SN3MFI 포인터
 * @return	pMFI의 파일 크기 반환.
 */
size_t snf_mfi_fsize(SN3MFI *pMFI);
/**
 * SN3MFI 객체의 파일 포지션을 리턴한다.
 * @param pMFI SN3MFI 포인터
 * @return	pMFI의 파일 포지션.
 */
__int64 snf_mfi_ftell(SN3MFI *pMFI);
/**
 * SN3MFI 객체의 파일 포지션이 마지막에 도달했는지 검사한다.
 * @param pMFI SN3MFI 포인터
 * @return	pMFI의 파일 포지션이 마지막에 도달했으면 1을
 *					아니면 0을 반환.
 */
int snf_mfi_feof(SN3MFI *pMFI);
/**
 * SN3MFI 객체의 현재 파일 포지션부터 끝까지 특정 파일에 기록한다.
 * @param pMFI SN3MFI 포인터
 * @param pFilePath 기록 대상 파일명
 * @return	쓰기 오류면 해당 오류를
 *					아니면 SN3OK를 반환.
 */
int snf_mfi_unload(SN3MFI *pMFI, __uint8 *pFilePath);

// mfi read
/**
* SN3MFI 객체의 현재 파일 포지션의 내용을 읽고
* 파일 포지션을 1 증가시킨다.
* @param pMFI SN3MFI 포인터
* @return	파일 포지션이 파일의 끝이라면 EOF를
* 아니면 읽은 내용을 반환.
*/
int snf_mfi_fgetc(SN3MFI *pMFI);
/**
 * SN3MFI 객체의 현재 파일 포지션의 바로 이전 내용을 읽고
 * 파일 포지션을 1 감소시킨다.
 * @param pMFI SN3MFI 포인터
 * @param ch 리턴받을 값
 * @return	파일 포지션이 처음이라면 EOF를
 *					아니면 ch를 반환.
 */
int snf_mfi_fungetc(SN3MFI *pMFI, int ch);
/**
 * SN3MFI 객체의 현재 파일 포지션부터 pSize*pCount 만큼의 내용을
 * 버퍼에 기록한 후 읽은 바이트 수 만큼 파일 포지션을 1 증가시킨다.
 * 읽을 바이트수가 현재의 파일 포지션에서 마지막까지의 바이트수보다 크면
 * 읽을 바이트수를 재조정한다.
 * @param pMFI SN3MFI 포인터
 * @param pBuffer __uint8형 쓰기 버퍼 포인터
 * @param pSize pBuffer의 데이타형 크기
 * @param pCount 읽을 개수
 * @return	실제 읽어들인 개수를 반환.
 */
__int64 snf_mfi_fread(SN3MFI *pMFI, __uint8 *pBuffer, size_t pSize, size_t pCount);

// mfi write
/**
 * SN3MFI 객체의 현재 파일 포지션에 값을 기록하고 포지션을 1 증가시킨다.
 * SN3MFI 객체의 pFile이 NULL이면
 * SN3MFI_REALLOC_SIZE 만큼의 메모리를 새로 할당하고,
 * 기록 후의 포지션이 Limit을 넘으면
 * SN3MFI_REALLOC_SIZE 만큼의 메모리를 추가로 할당한다.
 * @param pMFI SN3MFI 포인터
 * @param ch 기록할 데이터
 * @return	메모리 오류가 나면 EOF를
 *					제대로 기록되었으면 ch를 반환.
 */
int snf_mfi_fputc(SN3MFI *pMFI, int ch);
/**
 * SN3MFI 객체의 현재 파일 포지션부터 입력받은 버퍼의 내용을 기록한다.
 * SN3MFI 객체의 pFile이 NULL이면
 * 필요한 만큼의 메모리를 새로 할당하고,
 * 기록 후의 포지션이 Limit을 넘으면
 * 필요한 만큼의 메모리를 추가로 할당한다.
 * 기록후 읽은 바이트수 만큼 파일 포지션을 증가시킨다.
 * @param pMFI SN3MFI 포인터
 * @param pBuffer 파일에 기록할 버퍼
 * @param pSize pBuffer의 데이타형 크기
 * @param pCount 기록할 개수
 * @return	메모리 오류가 나면 0을
 *					기록되었으면 기록한 개수를 반환.
 */
size_t snf_mfi_fwrite(SN3MFI *pMFI, __uint8 *pBuffer, size_t pSize, size_t pCount);


// SN3BUF //////////////////////////////////////////////////////
// Buffer init & free
/**
 * UCS2-LE 버퍼를 초기화 한다.
 * @param	pBuf	버퍼 포인터의 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_buf_init(SN3BUF **pBuf);
/**
 * UCS2-LE 버퍼의 메모리를 반환한다.
 * @param	pBuf	버퍼의 포인터
 * @return	정상적으로 메모리를 반환한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_buf_free(SN3BUF *pBuf);

// Buffer misc
/**
 * 버퍼가 비어있는지 확인한다.
 * @param	pBuf	버퍼의 포인터
 * @return	비어있다면 1
 *          비어있지 않다면 0 을 반환
 */
int snf_buf_isempty(SN3BUF *pBuf);
/**
 * UCS2-LE 버퍼의 크기를 반환한다.
 * @param	pBuf	버퍼의 포인터
 * @return	버퍼의 크기를 반환.
 */
size_t snf_buf_size(SN3BUF *pBuf);
/**
* 버퍼의 UTF8 길이를 가져온다.
* @param  pBuf	버퍼의 포인터
* @return 버퍼의 UTF8 길이(size_t)를 반환.
*/
size_t snf_buf_get_utf8_len( const SN3BUF *pBuf );
/**
* 버퍼를 비운다.
* @param  pBuf  버퍼의 포인터
* @return 버퍼를 비운 후 SN3OK 반환
*/
int snf_buf_clear(SN3BUF *pBuf);
/**
* 첫번째 매개변수 버퍼 뒤에 두번째 매개변수 버퍼를 붙인다.
* @param  pBuf  버퍼의 포인터
* @param  pBufAdd  덧붙일 버퍼의 포인터
* @return 정상적으로 버퍼가 덧붙여졌다면 SN3OK반환.
*		  문제가 있는 경우에는 해당 오류코드 반환.
*/
int snf_buf_append(SN3BUF *pBuf, SN3BUF *pBufAdd);

// Buffer Unloading
/**
 * UCS2-LE 버퍼의 내용을 지정한 encoding 형태로 MFI에 출력한다.
 * @param	pBuf	버퍼의 포인터
 * @param	pMFI	MFI의 포인터
 * @param	pEncoding	Endocding 타입
 * @return	정상적으로 메모리를 반환한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_buf_unload_m(SN3BUF *pBuf, SN3MFI *pMFI, __int32 pEncoding);
/**
 * UCS2-LE 버퍼의 내용을 지정한 encoding 형태로
 * 지정경로의 로컬파일에 출력한다.
 * @param	pBuf	버퍼의 포인터
 * @param	pFilePath   출력 파일경로
 * @param	pEncoding	Encoding 타입
 * @return	정상적으로 메모리를 반환한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_buf_unload(SN3BUF *pBuf, __uint8 *pFilePath, __int32 pEncoding);
/**
 * UCS2-LE 버퍼의 내용을 지정한 encoding 형태로
 * 지정경로의 로컬파일에 출력한다.
 * @param	pBuf	버퍼의 포인터
 * @param	pFilePath   출력 파일경로 (유니코드 경로)
 * @param	pEncoding	Encoding 타입
 * @return	정상적으로 메모리를 반환한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_buf_wunload(SN3BUF *pBuf, __ucs2 *pFilePath, __int32 pEncoding);

// Buffer Put (UCS2 Version)
/**
 * UCS2-LE 문자를 버퍼에 넣는다. 버퍼에는 항상 정상적인
 * 유니코드 문자가 LE 형태로 있어야한다. SN3NOCHAR나
 * SN3NULL 등도 들어갈 수 없다. 버퍼크기가 부족하면 버퍼를 늘린다.
 * @param	pBuf	버퍼의 포인터
 * @param	ch		UCS2 문자
 * @return	정상적으로 입력된 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_buf_putc_ucs2_raw(SN3BUF *pBuf, __ucs2 ch);
/**
 * UCS2-LE 문자를 버퍼에 넣는다. 버퍼에는 항상 정상적인
 * 유니코드 문자가 LE 형태로 있어야한다. SN3NOCHAR나
 * SN3NULL 등도 들어갈 수 없다. 버퍼크기가 부족하면 버퍼를 늘린다.
 * @param	pBuf	버퍼의 포인터
 * @param	ch		UCS2 문자
 * @return	정상적으로 입력된 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_buf_putc_ucs2(SN3BUF *pBuf, __ucs2 ch);
/**
 * UCS2-LE 문자열을 버퍼에 넣는다. UCS2-LE 문자열의 끝에
 * SN3NULL이 꼭 있어야하며, 버퍼에 SN3NULL은 들어가지 않는다.
 * 문자열 중에 SN3NOCHAR 등이 있으면 무시하고 진행한다.
 * @param	pBuf	버퍼의 포인터
 * @param	str		UCS2 문자열
 * @return	정상적으로 입력된 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_buf_puts_ucs2(SN3BUF *pBuf, __ucs2 *str);
/**
 * UCS2-BE 문자열을 버퍼에 넣는다. UCS2-BE 문자열의 끝에
 * SN3NULL이 꼭 있어야하며, 버퍼에 SN3NULL은 들어가지 않는다.
 * 문자열 중에 SN3NOCHAR 등이 있으면 무시하고 진행한다.
 * @param	pBuf	버퍼의 포인터
 * @param	str		UCS2 문자열
 * @return	정상적으로 입력된 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_buf_puts_ucs2_be(SN3BUF *pBuf, __ucs2 *str);
/**
 * 버퍼에 newline 문자를 입력.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @return	정상적으로 입력된경우 SN3OK 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_buf_put_newline(SN3BUF *pBuf);
/**
 * 버퍼에 공백 문자를 입력.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @return	정상적으로 입력된경우 SN3OK 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_buf_put_space(SN3BUF *pBuf);

// Buffer Peek & Get (UCS2 Version)
/**
 * 버퍼에 제일 처음에 입력된 문자를 확인한다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @return	정상적으로 수행되었다면
 *          첫번째 문자(__ucs2)를 반환.
 *          버퍼가 비어있다면 SN3NOCHAR 반환.
 */
__ucs2 snf_buf_peekstart(SN3BUF *pBuf);
/**
 * 버퍼에 제일 마지막에 입력된 문자를 확인한다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @return	정상적으로 수행되었다면
 *          마지막문자(__ucs2)를 반환.
 *          버퍼가 비어있다면 SN3NOCHAR 반환.
 */
__ucs2 snf_buf_peekend(SN3BUF *pBuf);
/**
 * 버퍼의 가장 앞에 있는 UCS2-LE 문자를 읽어온다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @return	버퍼에서 읽어낸 유니코드를 반환
 *          버퍼에 비었으면 SN3NOCHAR를 반환
 */
__ucs2 snf_buf_getwch(SN3BUF *pBuf);
/**
 * 버퍼의 앞쪽에 UCS2-LE 문자를 넣는다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @param	ch		넣을 유니코드 문자
 * @return	별문제 없으면 SN3OK,
 *          버퍼의 앞쪽이 꽉찼으면 오류코드를 반환
 */
int snf_buf_ungetwch(SN3BUF *pBuf, __ucs2 ch);
/**
 * 버퍼에서 UCS2-LE 문자열을 읽어온다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @param	buf		받아올 버퍼의 포인터
 * @param	buf_size	받아올 버퍼의 크기
 * @return	읽어서 채운 유니코드 갯수(size_t)를 반환
 *          문제가 있다면 0을 반환.
 */
size_t snf_buf_get_ucs2(SN3BUF *pBuf, __ucs2 *buf, int buf_size);

// Buffer Put & Get (CP949 Version)
/**
 * MS-CP949 문자를 버퍼에 넣는다.
 * @param	pBuf	버퍼의 포인터
 * @param	ch		MS-CP949 문자
 * @return	정상적으로 입력된 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_buf_putc_cp949(SN3BUF *pBuf, __uint16 ch);
/**
 * MS-CP949 문자열을 버퍼에 넣는다. 문자열이 꼭 NULL로 끝나야한다.
 * @param	pBuf	버퍼의 포인터
 * @param	str		MS-CP949 문자열
 * @return	정상적으로 입력된 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_buf_puts_cp949(SN3BUF *pBuf, __uint8 *str);
/**
 * 버퍼에서 MS-CP949 문자열을 읽어온다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @param	buf		받아올 버퍼의 포인터
 * @param	buf_size	받아올 버퍼의 크기
 * @return	읽어서 채운 바이트수(size_t)를 반환
 *          문제가 있거나 더이상 가져올게 없으면 0을 반환.
 */
size_t snf_buf_get_cp949(SN3BUF *pBuf, __uint8 *buf, int buf_size);

// Buffer position
/**
 * 버퍼의 포지션을 셋팅 한다.
 * pos 가 0 보다 작은 경우 시작점으로 채워진 값보다 큰경우는 마지막으로 이동.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @param	pos		지정한 버퍼의 포지션
 * @return
 */
void snf_buf_setpos(SN3BUF *pBuf, size_t pos);
/**
 * 버퍼의 포지션을 시작점으로 옮겨준다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @return  버퍼가 비어있다면 0, 비어있지 않다면 버퍼의 시작점을 반환.
 */
size_t snf_buf_getpos(SN3BUF *pBuf);
/**
 * 버퍼의 포지션을 시작점으로 옮겨준다.
 * @param	pBuf	유니코드 버퍼의 포인터
 */
void snf_buf_rewind(SN3BUF *pBuf);

// Text getter
/**
 * 버퍼에서 지정한 인코딩으로 문자열을 읽어온다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @param	buf		받아올 버퍼의 포인터
 * @param	buf_size	받아올 버퍼의 크기
 * @param	encoding	저장할 인코딩
 * @return	읽어서 채운 바이트수(size_t)를 반환
 *          문제가 있거나 더이상 가져올게 없으면 0을 반환.
 */
size_t snf_buf_get_text(SN3BUF *pBuf, __uint8 *buf, int buf_size, int encoding);
/**
 * 버퍼에서 지정한 인코딩으로 문자열을 읽어온다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @param	buf		받아올 버퍼의 포인터
 * @param	buf_size	받아올 버퍼의 크기
 * @param	encoding	저장할 인코딩
 * @return	읽어서 채운 바이트수(size_t)를 반환
 *          문제가 있거나 더이상 가져올게 없으며 0을 반환.
 */
size_t snf_buf_get_text_le(SN3BUF *pBuf, __uint8 *buf, int buf_size, int encoding);


// SN3SUM //////////////////////////////////////////////////////
/**
 * SN3SUM 객체를 초기화한다.
 * @param	ppSum SN3SUM 포인터의 포인터
 * @return	제대로 메모리를 할당하면 SN3OK를 반환하고
 *					오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_sum_init(SN3SUM **ppSum);
/**
 * SN3SUM 객체의 메모리를 해제한다.
 * @param	pSum SN3SUM 포인터
 * @return	제대로 메모리를 해제하면 SN3OK를 반환하고
 *					오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_sum_free(SN3SUM *pSum);
/**
 * SN3SUM의 내용을 화면에 출력한다.
 * @param	pSum SN3SUM 포인터
 * @return	SN3OK를 반환한다.
 */
int snf_sum_show(SN3SUM *pSum);

// Summary Unloading ...
/**
 * SN3SUM의 내용을 SN3MFI에 인코딩 방식에 맞게 저장한다.
 * @param	pSum SN3SUM 포인터
 * @param	pMFI SN3MFI 포인터
 * @param	pEncoding 인코딩 방식
 * @return	SN3SUM 내용이 정상적으로 저장되면 SN3OK를,
 *				  오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_sum_unload_m(SN3SUM *pSum, SN3MFI *pMFI, __int32 pEncoding);
/**
 * SN3SUM의 내용을 FILE에 인코딩 방식에 맞게 저장한다.
 * @param	pSum SN3SUM 포인터
 * @param	pFile FILE 포인터
 * @param	pEncoding 인코딩 방식
 * @return	파일에 제대로 저장했으면 SN3OK를 반환하고
 *					오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_sum_unload_f(SN3SUM *pSum, FILE *pFile, __int32 pEncoding);
/**
 * SN3SUM의 내용을 파일에 인코딩 방식에 맞게 저장한다.
 * @param	pSum SN3SUM 포인터
 * @param	pFilePath 파일명
 * @param	pEncoding 인코딩 방식
 * @return	파일에 제대로 저장했으면 SN3OK를 반환하고
 *					오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_sum_unload(SN3SUM *pSum, __uint8 *pFilePath, __int32 pEncoding);
/**
 * SN3SUM의 내용을 파일에 인코딩 방식에 맞게 저장한다.
 * @param	pSum SN3SUM 포인터
 * @param	pFilePath 파일명
 * @param	pEncoding 인코딩 방식
 * @return	파일에 제대로 저장했으면 SN3OK를 반환하고
 *					오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_sum_wunload(SN3SUM *pSum, __ucs2 *pFilePath, __int32 pEncoding);

// Docinfo
/**
* 파일의 요약정보를 출력한다.
* @param  pFilePath 파일명
* @param  pSum	SN3SUM 포인터
* @return 요약정보가 정상적으로 출력되면 SN3OK가 반환되고
*			도중에 오류가 발생하면 해당 오류코드를 반환한다.
*/
int snf_flt_docinfo(__uint8 *pFilePath, SN3SUM *pSum);
/**
* 유니코드 경로의 파일의 요약정보를 출력한다.
* @param  pFilePath 파일명
* @param  pSum	SN3SUM 포인터
* @return 요약정보가 정상적으로 출력되면 SN3OK가 반환되고
*			도중에 오류가 발생하면 해당 오류코드를 반환한다.
*/
int snf_flt_wdocinfo(__ucs2 *pFilePath, SN3SUM *pSum);
/**
* 메모리에 있는 파일의 요약정보를 출력한다.
* @param  pMFI SN3MFI 포인터
* @param  pSum	SN3SUM 포인터
* @return 요약정보가 정상적으로 출력되면 SN3OK가 반환되고
*			도중에 오류가 발생하면 해당 오류코드를 반환한다.
*/
int snf_flt_docinfo_m(SN3MFI *pMFI, SN3SUM *pSum);
/**
 * 특정 파일의 DocumentSummaryInformation을 SN3BUF에 저장한다.
 * @param	pFilePath 파일명
 * @param	pBuf SN3BUF의 포인터
 * @return	SummaryInformation의 내용을 제대로 SN3BUF에 저장하면 SN3OK를 반환하고
 *			오류가 발생하면 해당 오류코드를 반환.
 */
int snf_flt_docinfoEx(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * 특정 파일의 DocumentSummaryInformation을 SN3BUF에 저장한다.
 * @param	pFilePath 파일명
 * @param	pBuf SN3BUF의 포인터
 * @return	SummaryInformation의 내용을 제대로 SN3BUF에 저장하면 SN3OK를 반환하고
 *			오류가 발생하면 해당 오류코드를 반환.
 */
int snf_flt_wdocinfoEx(__ucs2 *pFilePath, SN3BUF *pBuf);
/**
 * 메모리에 담긴 파일의 DocumentSummaryInformation을 SN3BUF에 저장한다.
 * @param	pMFI SN3MFI 포인터
 * @param	pBuf SN3BUF의 포인터
 * @return	SummaryInformation의 내용을 제대로 SN3BUF에 저장하면 SN3OK를 반환하고
 *			오류가 발생하면 해당 오류코드를 반환.
 */
int snf_flt_docinfoEx_m(SN3MFI *pMFI, SN3BUF *pBuf);

// Filter (FilePath) ///////////////////////////////////////////
/**
 * 파일 필터링 후 결과 텍스트를 버퍼에 기록한다.
 * @param	pFilePath	대상 파일 경로
 * @param   pBuf  추출한 텍스트가 저장될 SN3BUF 포인터
 * @param   WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	성공: SN3OK, 실패: 해당 에러코드
 */
int snf_flt_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
* 파일 필터링 후 결과 텍스트를 파일에 기록한다. (len을 wcslen()으로 구함)
* @param pFilePath 입력파일 경로
* @param pOutPath 출력파일 경로. NULL일 경우 stdout에 기록
* @param WithPage 페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
* @param encoding 출력 텍스트 인코딩
* @return 성공: SN3OK, 실패: 해당 에러코드
*/
int snf_flt_filter_ex(__uint8 *pFilePath, __uint8 *pOutPath, int WithPage, int encoding);
/**
 * 파일 필터링 후 결과 텍스트를 버퍼에 기록한다.
 * @param	pFilePath	대상 파일 경로
 * @param   pBuf  추출한 텍스트가 저장될 SN3BUF 포인터
 * @param   WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	성공: SN3OK, 실패: 해당 에러코드
 */
int snf_flt_wfilter(__ucs2 *pFilePath, SN3BUF *pBuf, int WithPage);

/**
 * alz 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	alz 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage	 페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_alz_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * bzip 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	bzip 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_bzip_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * chm 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	chm 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_chm_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * doc 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	doc 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_doc_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * docx 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	docx 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_docx_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * dwg 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	dwg 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_dwg_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * GZ(GNU Zip) 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	GZ 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_gz_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * h2k 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	h2k 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_h2k_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * htm / html 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	htm / html 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_htm_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwn 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	hwn 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_hwn_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwd 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	hwd 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_hwd_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwp3 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	hwp3 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_hwp3_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwx 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	hwx 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_hwx_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * jtd 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	jtd 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_jtd_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * mdb 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	mdb 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_mdb_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * mdi 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	mdi 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_mdi_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * mht 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	mht 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_mht_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * mp3 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	mp3 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_mp3_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * msg 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	msg 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_msg_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * pdf 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	pdf 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_pdf_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * ppt 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	ppt 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_ppt_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * pptx 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	pptx 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_pptx_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * ppam 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	ppam 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_ppam_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * thmx 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	thmx 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_thmx_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * rtf 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	rtf 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_rtf_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * 7zip 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	7zip 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_sevenzip_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * swf 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	swf 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_swf_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * sxx 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	sxx 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_sxx_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * tar 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	tar 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_tar_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * txt 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	txt 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_txt_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * vtt 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	vtt 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_vtt_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * wpd 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	wpd 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_wpd_filter( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xls 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	xls 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_xls_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xlsx 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	xlsx 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_xlsx_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwp 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	hwp 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_xml_hwp_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xml office 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	xml office 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_xml_office_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * zip 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	zip 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_zip_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * rar 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	rar 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_rar_filter( __uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * ndoc 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	ndoc 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_ndoc_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * KEYNOTE 파일을 버퍼에 필터링 한다.
 * @param	pFilePath Keynote 파일 경로
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_keynote_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * PAGES 파일을 버퍼에 필터링 한다.
 * @param	pFilePath pages 파일 경로
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_pages_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * NUMBERS 파일을 버퍼에 필터링 한다.
 * @param	pFilePath numbers 파일 경로
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_numbers_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * pst 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	pst 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_pst_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwpx 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	hwpx 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_hwpx_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * 넥셀(nxl) 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	nxl 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_nxl_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * 한컴 엑셀 파일(cell)을 버퍼에 필터링 한다.
 * @param	pFilePath	cell 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_cell_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * 한쇼(show) 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	show 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_show_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xps 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	xps 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_xps_filter(__uint8 *pFilePath, SN3BUF *pBuf);

/**
 * keynote'13 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	keynote'13 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_keynote13_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * pages13 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	pages13 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_pages13_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * numbers13 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	numbers13 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_numbers13_filter(__uint8 *pFilePath, SN3BUF *pBuf);

/**
 * keynote14 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	keynote14 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_keynote14_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * pages14 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	pages14 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_pages14_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * numbers14 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	numbers14 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_numbers14_filter(__uint8 *pFilePath, SN3BUF *pBuf);

/**
 * xlsb 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	xlsb 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_xlsb_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * DICOM 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	DICOM 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_dicom_filter(__uint8 *pFilePath, SN3BUF *pBuf);

/**
 * nsf 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	nsf 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_nsf_filter(__uint8* pFilePath, SN3BUF* pBuf);
/**
 * edb 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	edb 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_edb_filter(__uint8* pFilePath, SN3BUF* pBuf);

// Filter (MFI) ////////////////////////////////////////////////
/**
 * 메모리에 담긴 파일 포맷 필터링 후 포맷에 맞게 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI 소스 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_flt_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);

/**
 * alz 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI alz 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_alz_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * bzip 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI bzip 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_bzip_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * chm 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI chm 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_chm_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * doc 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI doc 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_doc_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * docx 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI docx 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_docx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * dwg 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI dwg 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_dwg_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * GZ 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI GZ 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_gz_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * h2k 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI h2k 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_h2k_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * htm 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI htm 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_htm_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * hwn 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI hwm 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_hwn_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * hwd 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI hwd 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_hwd_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * hwp3 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI hwp3 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_hwp3_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * hwx 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI hwx 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_hwx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * jtd 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI jtd 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_jtd_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * mdb 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI mdb 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_mdb_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * mdi 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI mdi 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_mdi_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * mht 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI mht 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_mht_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * mp3 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI mp3 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_mp3_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * msg 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI msg 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_msg_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * pdf 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI pdf 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_pdf_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * ppt 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI ppt 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_ppt_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * pptx 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI pptx 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_pptx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * rtf 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI rtf 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_rtf_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * 7zip 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI 7zip 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_sevenzip_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * swf 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI swf 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_swf_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * sxx 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI sxx 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_sxx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * tar 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI tar 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage 페이지 구분자 출력 여부.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_tar_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * txt 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI txt 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_txt_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * vtt 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI vtt 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_vtt_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * wpd 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI wpd 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_wpd_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xls 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI xls 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_xls_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xlsx 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI xlsx 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_xlsx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf );
/**
 * hwp 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI hwp 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_xml_hwp_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xml office 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI xml office 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_xml_office_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * zip 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI zip 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_zip_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * rar 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI rar 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_rar_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * ndoc 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI ndoc 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_ndoc_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * egg 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI egg 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_egg_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * KEYNOTE 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI keynote 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_keynote_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * PAGES 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI pages 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_pages_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * NUMBERS 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI numbers 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_numbers_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * pst 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI pst 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_pst_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
* pst 파일 내용을 void형 이중 포인터에 기록한다. wsnf_pst_email_close()를 쌍으로 사용해 메모리 누수를 막아야 한다.
* @param	pMFI pst파일이 담긴 메모리 포인터
* @param	ctx 파일 내용이 담길 void형 이중 포인터
* @return	제대로 필터링하면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
*/
int snf_pst_email_open(SN3MFI *pMFI, void **ctx);
/**
* void형 포인터에 담긴 이메일 노드 개수를 반환한다.
* @param	ctx 이메일 정보가 담긴 변수 포인터
* @return	매개변수가 가리키는 포인터의 이메일 노드 개수를 반환한다.
*/
int snf_pst_email_count(void *ctx);
/**
* 메모리에 담긴 아웃룩 파일 정보를 버퍼에 필터링한다.
* @param	pMFI pst 파일이 담긴 메모리 포인터
* @param	pBuf 정보를 담을 버퍼 포인터
* @param	ctx  이메일 정보가 담긴 변수 포인터
* @param	idx	버퍼에 담을 이메일 인덱스
* @return	버퍼에 성공적으로 필터링 시 SN3OK를, 문제가 있는 경우 해당 에러코드 반환한다.
*/
int snf_pst_filter_email_m(SN3MFI *pMFI, SN3BUF *pBuf, void *ctx, int idx);
/**
* wsnf_pst_email_close()에서 동적으로 만들었던 SN3PST_API_CONTEXT 객체를 삭제한다.
* @param	ctx 이메일 정보가 담긴 변수 포인터
*/
void snf_pst_email_close(void *ctx);

/**
 * hwpx 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI hwpx 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_hwpx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * nxl 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI nxl 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_nxl_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * 한셀(cell) 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI cell 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_cell_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * 한쇼(show) 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI show 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_show_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xps 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI xps 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_xps_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);

/**
 * xlsb 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI xlsb 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_xlsb_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);

/**
 * keynote14 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI keynote14 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_keynote14_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * pages14 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI pages14 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_pages14_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * numbers14 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI numbers14 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_numbers14_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);

/**
 * DICOM 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI DICOM 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_dicom_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);

/**
 * nsf 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI nsf 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_nsf_filter_m(SN3MFI* pMFI, SN3BUF* pBuf);
/**
 * edb 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI edb 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_edb_filter_m(SN3MFI* pMFI, SN3BUF* pBuf);

// Filter (MFI) with Format Code ///////////////////////////////
/**
 * 메모리에서 인자로 들어오는 번호에 해당하는 포맷 파일을 버퍼에 필터링한다.
 * @param	pMFI 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @param	FileFormat 파일 포맷 해당 번호
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_flt_filter_c( SN3MFI *pMFI, SN3BUF *pBuf, int WithPage, int FileFormat);
/**
 * 메모리에서 인자로 들어오는 인코딩으로 txt 파일을 버퍼에 필터링한다.
 * @param	pMFI 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	FileFormat 인코딩 번호
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int snf_txt_filter_c( SN3MFI *pMFI, SN3BUF *pBuf, int FileFormat);


// File(sheet,table) list (FilePath) ///////////////////////////
/**
 * alz파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pFilePath	alz 파일 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_alz_filelist( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * GZ파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pFilePath	gz 파일 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_gz_filelist(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * mdb파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pFilePath	mdb 파일 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_mdb_filelist( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * 7zip파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pFilePath	7zip 파일 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_sevenzip_filelist( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * tar파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pFilePath	tar 파일 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_tar_filelist(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xls파일의 시트 목록을 출력한다.
 *
 * @param	pFilePath	xls 파일 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_xls_sheetlist ( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xlsx파일의 시트 목록을 출력한다.
 *
 * @param	pFilePath	xlsx 파일 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_xlsx_sheetlist ( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * zip파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pFilePath	zip 파일 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_zip_filelist(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * rar파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pFilePath	rar 파일 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_rar_filelist(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xlsb파일의 시트 목록을 출력한다.
 *
 * @param	pFilePath	xlsb 파일 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_xlsb_sheetlist(__uint8 *pFilePath, SN3BUF *pBuf);

// File(sheet,table) list (MFI) ////////////////////////////////
/**
 * alz파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	alz 파일이 담긴 메모리 포인터
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_alz_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * GZ파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	gz 파일이 담긴 메모리 포인터
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_gz_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * mdb파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	mdb 파일이 담긴 메모리 포인터
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_mdb_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * 7zip파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	7zip 파일이 담긴 메모리 포인터
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_sevenzip_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * tar파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	tar 파일이 담긴 메모리 포인터
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_tar_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xls파일의 시트 목록을 출력한다.
 *
 * @param	pMFI	xls 파일이 담긴 메모리 포인터
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_xls_sheetlist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xlsx파일의 시트 목록을 출력한다.
 *
 * @param	pMFI	xlsx 파일이 담긴 메모리 포인터
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_xlsx_sheetlist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * zip파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	zip 파일이 담긴 메모리 포인터
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_zip_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * rar파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	rar 파일이 담긴 메모리 포인터
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_rar_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xlsb파일의 시트 목록을 출력한다.
 *
 * @param	pMFI	xlsb 파일이 담긴 메모리 포인터
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_xlsb_sheetlist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * egg파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	egg 파일이 담긴 메모리 포인터
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int snf_egg_filelist_m( SN3MFI *pMFI, SN3BUF *pBuf);
// File(sheet,table) raw list (MFI) ////////////////////////////////
/**
* 아카이브 파일 리스트(SN3ARFILIST)를 매개변수에 동적 할당한다.
* @param	ppList	SN3ARFILIST를 동적 할당받을 더블 포인터
* @return	매개변수에 정상적으로 메모리를 할당받은 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
*/
int snf_arfilist_init(SN3ARFILIST** ppList);
/**
* 아카이브 파일 리스트(SN3ARFILIST)를 매개변수에서 메모리 해제한다.
* @param	ppList	매모리 해제할 SN3ARFILIST 포인터
*/
void snf_arfilist_free(SN3ARFILIST* pList);
/**
* 아카이브 파일 리스트(SN3ARFILIST)에서 idx번째 raw파일의 이름을 반환한다.
* @param	pList 이름을 추출할 SN3ARFILIST 포인터
* @param	idx	추출할 파일의 파일 목록 내 위치 (0-based)
* @return	SN3ARFLIST의 idx번째 파일의 이름이 ucs2 문자열로 리턴된다.실패 시 에러코드 반환.
*/
__uint8* snf_arfilist_name(SN3ARFILIST* pList, int idx);
/**
* 아카이브 파일 리스트(SN3ARFILST)의 idx번째 출력용 파일 이름을 반환한다.
* pBuf에 출력용 파일 이름이 덧붙여지고, 필요하면 snf_buf_clear()로 버퍼를 비워줘야 한다.
* @param	pList 이름을 추출할 SN3ARFILIST 포인터
* @param	idx	추출할 파일의 파일 목록 내 위치 (0-based)
* @param	pBuf 파일 이름이 담긴 SN3BUF 포인터
* @return	성공 시 SN3OK를, 실패하면 에러코드를 반환한다.
*/
int snf_arfilist_printname(SN3ARFILIST* pList, int idx, SN3BUF* pBuf);
/**
* SN3ARFILIST가 갖고 있는 파일 목록 개수를 반환한다.
* @param	pList SN3ARFILIST 포인터
* @return	성공 시 SN3OK를, 실패하면 에러코드를 반환한다.
*/
int snf_arfilist_count(SN3ARFILIST* pList);

/**
* alz 압축 파일 내에 압축된 파일의 목록을 얻는다.
* 압축 파일 내 모든 압축된 파일의 경로를 추출해 SN3ARFILST에 저장한다.
* @param	pMFI 대상 파일의 SN3MFI 포인터
* @param	pList 파일 목록이 담긴 SN3ARFILIST 포인터
* @return	성공하면 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int snf_alz_filelistEx_m(SN3MFI* pMFI, SN3ARFILIST* pList);
/**
* 7zip 압축 파일 내에 압축된 파일의 목록을 얻는다.
* 압축 파일 내 모든 압축된 파일의 경로를 추출해 SN3ARFILST에 저장한다.
* @param	pMFI 대상 파일의 SN3MFI 포인터
* @param	pList 파일 목록이 담긴 SN3ARFILIST 포인터
* @return	성공하면 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int snf_sevenzip_filelistEx_m(SN3MFI* pMFI, SN3ARFILIST* pList);
/**
* tar 압축 파일 내에 압축된 파일의 목록을 얻는다.
* 압축 파일 내 모든 압축된 파일의 경로를 추출해 SN3ARFILST에 저장한다.
* @param	pMFI 대상 파일의 SN3MFI 포인터
* @param	pList 파일 목록이 담긴 SN3ARFILIST 포인터
* @return	성공하면 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int snf_tar_filelistEx_m(SN3MFI* pMFI, SN3ARFILIST* pList);
/**
* zip 압축 파일 내에 압축된 파일의 목록을 얻는다.
* 압축 파일 내 모든 압축된 파일의 경로를 추출해 SN3ARFILST에 저장한다.
* @param	pMFI 대상 파일의 SN3MFI 포인터
* @param	pList 파일 목록이 담긴 SN3ARFILIST 포인터
* @return	성공하면 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int snf_zip_filelistEx_m(SN3MFI* pMFI, SN3ARFILIST* pList);
/**
* rar 압축 파일 내에 압축된 파일의 목록을 얻는다.
* 압축 파일 내 모든 압축된 파일의 경로를 추출해 SN3ARFILST에 저장한다.
* @param	pMFI 대상 파일의 SN3MFI 포인터
* @param	pList 파일 목록이 담긴 SN3ARFILIST 포인터
* @return	성공하면 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int snf_rar_filelistEx_m(SN3MFI* pMFI, SN3ARFILIST* pList);
/**
* egg 압축 파일 내에 압축된 파일의 목록을 얻는다.
* 압축 파일 내 모든 압축된 파일의 경로를 추출해 SN3ARFILST에 저장한다.
* @param	pMFI 대상 파일의 SN3MFI 포인터
* @param	pList 파일 목록이 담긴 SN3ARFILIST 포인터
* @return	성공하면 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int snf_egg_filelistEx_m(SN3MFI* pMFI, SN3ARFILIST* pList);

// Extract file from Archive ///////////////////////////////////
/**
* alz 압축 파일 내에 지정된 압축 파일을 풀어 SN3MFI에 쓴다.
* @param	pMFI 압축 파일이 열린 SN3MFI 포인터
* @param	pUzFile 압축 해제된 파일이 쓰여질 SN3MFI 포인터
* @param	pFileNm 압축 해제할 파일의 경로
* @return	성공 시 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int snf_alz_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* 7zip 압축 파일 내에 지정된 압축 파일을 풀어 SN3MFI에 쓴다.
* @param	pMFI 압축 파일이 열린 SN3MFI 포인터
* @param	pUzFile 압축 해제된 파일이 쓰여질 SN3MFI 포인터
* @param	pFileNm 압축 해제할 파일의 경로
* @return	성공 시 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int snf_sevenzip_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* tar 압축 파일 내에 지정된 압축 파일을 풀어 SN3MFI에 쓴다.
* @param	pMFI 압축 파일이 열린 SN3MFI 포인터
* @param	pUzFile 압축 해제된 파일이 쓰여질 SN3MFI 포인터
* @param	pFileNm 압축 해제할 파일의 경로
* @return	성공 시 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int snf_tar_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* zip 압축 파일 내에 지정된 압축 파일을 풀어 SN3MFI에 쓴다.
* @param	pMFI 압축 파일이 열린 SN3MFI 포인터
* @param	pUzFile 압축 해제된 파일이 쓰여질 SN3MFI 포인터
* @param	pFileNm 압축 해제할 파일의 경로
* @return	성공 시 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int snf_zip_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* rar 압축 파일 내에 지정된 압축 파일을 풀어 SN3MFI에 쓴다.
* @param	pMFI 압축 파일이 열린 SN3MFI 포인터
* @param	pUzFile 압축 해제된 파일이 쓰여질 SN3MFI 포인터
* @param	pFileNm 압축 해제할 파일의 경로
* @return	성공 시 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int snf_rar_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* bzip 압축 파일 내에 지정된 압축 파일을 풀어 SN3MFI에 쓴다.
* @param	pMFI 압축 파일이 열린 SN3MFI 포인터
* @param	pUzFile 압축 해제된 파일이 쓰여질 SN3MFI 포인터
* @return	성공 시 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int snf_bzip_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile);
/**
* egg 압축 파일 내에 지정된 압축 파일을 풀어 SN3MFI에 쓴다.
* @param	pMFI 압축 파일이 열린 SN3MFI 포인터
* @param	pUzFile 압축 해제된 파일이 쓰여질 SN3MFI 포인터
* @return	성공 시 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int snf_egg_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileName);

// User Callback Function Define ///////////////////////////////////
/**
 * 사용자 정의 함수를 세팅한다.
 * @param pBuf			   버퍼의 포인터
 * @param snf_buf_user_func 사용자 정의 함수 포인터
 */
void snf_buf_set_user_func( SN3BUF *pBuf, void(* sn3buf_user_func)(SN3BUF* pBuf, void* pUserData) );
/**
 * 사용자 명령을 세팅한다.
 *
 * @param pBuf				버퍼의 포인터
 * @param snf_user_command	사용자 명령
 *
 */
void snf_buf_set_user_command(SN3BUF *pBuf, int sn3_user_command);
/**
 * 사용자 데이터를 세팅한다.
 *
 * @param pBuf			버퍼의 포인터
 * @param pUserData		사용자 데이터 포인터
 */
void snf_buf_set_user_data(SN3BUF *pBuf, void* pUserData);
/**
* 사용자 콜백 40101 에러파일에 대한 callback setter 함수
*
* @param pBuf						버퍼의 포인터
* @param sn3buf_unknownfile_func	callback 함수
*/;
int  snf_buf_set_unknownfile_func(SN3BUF *pBuf, bool(*sn3buf_unknownfile_func)(SN3MFI* pMFI, SN3MFI* pNewMFI));

// User Marker Callback Function Define
#ifdef __cplusplus
/**
 * 사용자 콜백 마크 함수를 세팅한다.
 *
 * @param pBuf				버퍼의 포인터
 * @param snf_buf_marker_func 사용자 콜백 마커 함수 포인터
 */
void snf_buf_set_marker_func(SN3BUF *pBuf, int(* sn3buf_marker_func)(SN3BUF* pBuf, void* pMarkerData, SN3MARKER *pMarker)=NULL);
#else
/**
 * 사용자 콜백 마크 함수를 세팅한다.
 *
 * @param pBuf				버퍼의 포인터
 * @param snf_buf_marker_func 사용자 콜백 마커 함수 포인터
 */
void snf_buf_set_marker_func(SN3BUF *pBuf, int(* sn3buf_marker_func)(SN3BUF* pBuf, void* pMarkerData, SN3MARKER *pMarker));
#endif //__cplusplus
/**
 * 사용자 콜백 마크를 세팅한다.
 *
 * @param pBuf			버퍼의 포인터
 * @param pUserData		사용자 데이터 포인터
 */
void snf_buf_set_marker_data(SN3BUF *pBuf, void* pMarkerData);
/**
 * 사용자 콜백 마커 SKIP 상태의 Setter 함수
 *
 * @param pBuf				버퍼의 포인터
 * @param snf_skip_command	스킵명령
 */
void snf_buf_set_skip_command(SN3BUF *pBuf, int sn3_skip_command);
/**
 * 사용자 콜백 마커 SKIP 상태의 Getter 함수
 *
 * @param pBuf			버퍼의 포인터
 * @return int			스킵명령
 */
int snf_buf_get_skip_command(SN3BUF *pBuf);

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

/**************************************************************
*                  SN3(V3 이하) API 함수                      *
***************************************************************/

// Config //////////////////////////////////////////////////////
/**
* 현재 설정 정보를 출력한다.
*/
void sn3gbl_showcfg();
/**
 * 필터 구동 환경 설정을 한다.
 * @param pKeyStr 라이센스 번호. 이제는 사용하지 않아 NULL 또는 ""입력.
 * @param FileType 필터링 대상 파일 설정. SN3FILETYPE_ALL을 제외하고 Or로 중복 지정 가능하다.
 * @param Option  필터 제어 옵션. Or로 중복 지정 가능하다.
 * @param BaseBufSize 메모리 버퍼 크기.
 */
void sn3gbl_setcfg(const char * pKeyStr, __uint64 FileType, __uint64 Option, size_t BaseBufSize);
/**
 * 필터 구동 환경 및 압축파일 필터 옵션을 설정한다.
 * @param pKeyStr 라이센스 번호. 이제는 사용하지 않아 NULL 또는 ""입력.
 * @param FileType 필터링 대상 파일 설정.
 * @param Option  필터 제어 옵션
 * @param BaseBufSize 필터링시 사용되는 버퍼 크기.
 * @param opt	  압축 파일 필터링, 압축 해제 관련 SN3OPTION_PARAM 구조체
 */
void sn3gbl_setcfgEx(const char * pKeyStr, __uint64 FileType, __uint64 Option, size_t BaseBufSize, SN3OPTION_PARAM opt);

// Utility /////////////////////////////////////////////////////
/**
* 필터 이름을 구한다.
* @return	필터 이름을 리턴한다.
*/
char* sn3ver_program();
/**
* 필터 버전을 구한다.
* @return	필터 버전을 리턴한다.
*/
char* sn3ver_version();

/**
* 파일 포맷 코드를 구한다.
* @param	pMFI	파일 포맷을 구하려는 문서의 메모리 구조체 포인터
* @param	pFormat 파일 포맷코드가 기록될 int형 포인터. 파일 포맷 검사가 실패하면 기록되지 않는다.
* @return	성공 시 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int sn3fmt_detect_m(SN3MFI *pMFI, int *pFormat);
/**
* 파일의 로컬 경로를 이용해서 포맷 코드를 구한다.
* @param	pFilePath 포맷코드를 구하려는 문서 파일의 경로.
* @param	pFormat 파일 포맷코드가 저장된다. 파일 포맷 검사가 실패하면 기록되지 않는다.
* @return	성공 시 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int sn3fmt_detect(__uint8 *pFilePath, int *pFormat);
/**
 * 파일의 로컬경로로 부터 파일 포맷을 구한다.
 * @param	pFilePath	FILE 경로 (유니코드 경로)
 * @param   pFormat	포맷코드가 저장된다. 파일 포맷 검사 실패 시 기록되지 않는다.
 * @return	성공 시 SN3OK를, 실패 시 해당 오류코드를 반환.
 */
int sn3fmt_wdetect(__ucs2 *pFilePath, int *pFormat);
/**
 * FormatCode 로 부터 포맷의 이름을 찾는다.
 * @param	pFormatCode	포맷코드
 * @return	성공한경우 포맷의 이름을,
 *          실패한경우 오류코드를 반환한다.
 */
char* sn3fmt_format_name(int pFormatCode);

/**
 * FormatCode 로 부터 포맷의 이름을 찾는다. 실제 지원하는 포맷만 찾는다.
 * @param	pFormatCode	포맷코드
 * @return	성공한경우 포맷의 이름을,
 *          실패한경우 오류코드를 반환한다.
 */
char* sn3fmt_formatcodeByName(int _formatCode);

/**
* 파일 경로를 이용해 실제 필터링이 가능한 파일인지 true/false 리턴
* @param pFilePath  FILE 경로
* @return 필터링이 가능하면 1, 아니면 0을 반환한다.
*/
int sn3fmt_isFilterFormat(__uint8 *pFilePath);
/**
* MFI에 담긴 값이 실제 필터링이 가능한지 true/false 리턴
* @param pMFI  MFI 포인터
* @return 필터링이 가능하면 1, 아니면 0을 반환한다.
*/
int sn3fmt_isFilterFormat_m(SN3MFI *pMFI);

/**
 * Next 에러코드가 (ERROR_SN3XXX_) 잘못된 파일(깨진 파일)의 경우인지 확인한다.
 * @param	nErr	에러코드
 * @return	잘못된 파일(깨진 파일) 경우 양의 정수를 반환.
 *          아닐경우 0을 반환
 */
int sn3err_isbadfile(int nErr);

/**
 * 유니코드(UCS2-LE) 문자열을 cp949 문자열로 변형.
 * @param	wstr	유니코드 문자열
 * @return	정상적으로 변환된경우 cp949의 포인터를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
char* sn3ucs_ucs2cp949(__ucs2 *wstr);
/**
 * MS-CP949문자열을 UCS2-LE문자열로 변환한다.
 * 변환된 유니코드 문자열은 나중에 꼭 free 시켜줘야 한다.
 * @param	pCp949	MS-CP949문자열을 담고 있는 곳의 포인터
 * @return	정상적으로 변환되었을 경우 변환된 __ucs2 *를 반환
 *          변환에 문제가 있다면 NULL을 반환
 */
__ucs2* sn3cp949_to_ucs2_str(__uint8 *pCp949);
/**
* 변환시킨 유니코드 문자열을 메모리 해제한다.
* @param	pMem  메모리 해제할 유니코드 문자열
*/
void sn3utl_free(void *pMem);
/**
 * UCS2-LE 문자열의 길이를 반환한다.
 * @param	string	유니코드 문자열의 포인터
 * @return	입력된 유니코드 문자열의 길이를 반환.
 */
size_t sn3ucs_wcslen(__ucs2 *string );
/**
* 유니코드 문자열을 디코딩한다.
* @param wstr 입력 UTF-8
* @param encoding 인코딩 종류
* @return 디코딩된 결과가 ucs2 문자열로 반환
*/
__uint8* sn3ucs_decode_str(__ucs2 *wstr, int encoding);
/**
* ucs2 문자열을 입력 받아 지정한 utf8 문자열 포인터로 변환한다.
* @param wstr 입력
* @param wlen 입력 길이
* @param dest 출력할 utf 문자열
* @param dlen 출력 길이
* @param encoding 인코딩 종류
* @return 성공: SN3OK, 실패: ERROR_UTF8_FROM_UCS2_LOOP_FULL_OUTPUT
*/
int sn3ucs_decode(__ucs2 *wstr, int wlen, __uint8* dest, int dlen, int encoding);

/**
* @brief utf8 문자열을 ucs2 문자열로 변환
* @details utf8 문자열을 입력 받으면 ucs2 문자열을 반환한다.
*		   반환 받은 포인터는 반드시 sn3utl_free() 를 이용해 해제해야한다.
*
* @param pUtf8 입력 utf8 포인터
* @see sn3utf8_to_ucs2(), sn3utf8_to_ucs2_loop(), sn3utl_free()
* @return ucs2 문자열 포인터
*/
__ucs2* sn3utf8_to_ucs2_str(__uint8 *pUtf8);


// SN3MFI ///////////////////////////////////////////////////////
// mfi open&close
/**
 * SN3MFI 객체를 생성(메모리할당)하고 Default 값으로 초기화 한다.
 * @param	ppMFI	SN3MFI 포인터의 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3mfi_fopen_rw(SN3MFI **ppMFI);
/**
 * SN3MFI 객체를 생성(메모리할당)하고 메모리 파일의 내용으로 초기화 한다.
 * @param	pMemFile 메모리 파일 포인터
 * @param pMemSize 메모리 파일의 크기
 * @param ppMFI SN3MFI 포인터의 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3mfi_fopen_m(__uint8 *pMemFile, __int64 pMemSize, SN3MFI **ppMFI);
/**
 * SN3MFI 객체를 생성(메모리할당)하고 메모리 파일의 내용으로 초기화 한다.
 * @param	pMemFile 메모리 파일 포인터
 * @param pMemSize 메모리 파일의 크기
 * @param ppMFI SN3MFI 포인터의 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3mfi_fopen(__uint8 *pFilePath, SN3MFI **ppMFI);
/**
 * SN3MFI 객체를 생성(메모리할당)하고 파일의 내용으로 초기화 한다.
 * @param	pFilePath 멀티바이트 파일명
 * @param ppMFI SN3MFI 포인터의 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3mfi_wfopen(__ucs2 *pFilePath, SN3MFI **ppMFI);
/**
 * SN3MFI 객체를 파괴(메모리반환)한다.
 * @param pMFI SN3MFI 포인터
 * @return	정상적으로 메모리가 반환된 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3mfi_fclose(SN3MFI *pMFI);

// mfi misc
/**
 * SN3MFI 객체의 현재 파일 포지션을 처음으로 보낸다.
 * @param pMFI SN3MFI 포인터
 */
void sn3mfi_rewind(SN3MFI *pMFI);
/**
 * SN3MFI 객체의 파일 포지션을 설정 플래그에 따라 특정 위치로 설정한다.
 * 가능한 설정 플래그는 SN3MFI_SEEK_SET, SN3MFI_SEEK_CUR, SN3MFI_SEEK_END
 * 중 하나여야 한다.
 * @param pMFI SN3MFI 포인터
 * @param pOffset 새 포지션
 * @param pOrigin 포지션 설정 플래그
 * @return	pMFI의 파일 포지션이 제대로 설정될 수 있다면 SN3OK를
 *					아니면 해당 오류를 반환.
 */
__int64 sn3mfi_fseek(SN3MFI *pMFI, __int64 pOffset, int pOrigin);
/**
 * SN3MFI 객체의 파일 크기를 리턴한다.
 * @param pMFI SN3MFI 포인터
 * @return	pMFI의 파일 크기 반환.
 */
size_t sn3mfi_fsize(SN3MFI *pMFI);
/**
 * SN3MFI 객체의 파일 포지션을 리턴한다.
 * @param pMFI SN3MFI 포인터
 * @return	pMFI의 파일 포지션.
 */
__int64 sn3mfi_ftell(SN3MFI *pMFI);
/**
 * SN3MFI 객체의 파일 포지션이 마지막에 도달했는지 검사한다.
 * @param pMFI SN3MFI 포인터
 * @return	pMFI의 파일 포지션이 마지막에 도달했으면 1을
 *					아니면 0을 반환.
 */
int sn3mfi_feof(SN3MFI *pMFI);
/**
 * SN3MFI 객체의 현재 파일 포지션부터 끝까지 특정 파일에 기록한다.
 * @param pMFI SN3MFI 포인터
 * @param pFilePath 기록 대상 파일명
 * @return	쓰기 오류면 해당 오류를
 *					아니면 SN3OK를 반환.
 */
int sn3mfi_unload(SN3MFI *pMFI, __uint8 *pFilePath);

// mfi read
/**
*SN3MFI 객체의 현재 파일 포지션의 내용을 읽고
* 파일 포지션을 1 증가시킨다.
* @param pMFI SN3MFI 포인터
* @return	파일 포지션이 파일의 끝이라면 EOF를
* 아니면 읽은 내용을 반환.
*/
int sn3mfi_fgetc(SN3MFI *pMFI);
/**
 * SN3MFI 객체의 현재 파일 포지션의 바로 이전 내용을 읽고
 * 파일 포지션을 1 감소시킨다.
 * @param pMFI SN3MFI 포인터
 * @param ch 리턴받을 값
 * @return	파일 포지션이 처음이라면 EOF를
 *					아니면 ch를 반환.
 */
int sn3mfi_fungetc(SN3MFI *pMFI, int ch);
/**
 * SN3MFI 객체의 현재 파일 포지션부터 pSize*pCount 만큼의 내용을
 * 버퍼에 기록한 후 읽은 바이트 수 만큼 파일 포지션을 1 증가시킨다.
 * 읽을 바이트수가 현재의 파일 포지션에서 마지막까지의 바이트수보다 크면
 * 읽을 바이트수를 재조정한다.
 * @param pMFI SN3MFI 포인터
 * @param pBuffer __uint8형 쓰기 버퍼 포인터
 * @param pSize pBuffer의 데이타형 크기
 * @param pCount 읽을 개수
 * @return	실제 읽어들인 개수를 반환.
 */
__int64 sn3mfi_fread(SN3MFI *pMFI, __uint8 *pBuffer, size_t pSize, size_t pCount);

// mfi write
/**
 * SN3MFI 객체의 현재 파일 포지션에 값을 기록하고 포지션을 1 증가시킨다.
 * SN3MFI 객체의 pFile이 NULL이면
 * SN3MFI_REALLOC_SIZE 만큼의 메모리를 새로 할당하고,
 * 기록 후의 포지션이 Limit을 넘으면
 * SN3MFI_REALLOC_SIZE 만큼의 메모리를 추가로 할당한다.
 * @param pMFI SN3MFI 포인터
 * @param ch 기록할 데이터
 * @return	메모리 오류가 나면 EOF를
 *					제대로 기록되었으면 ch를 반환.
 */
int sn3mfi_fputc(SN3MFI *pMFI, int ch);
/**
 * SN3MFI 객체의 현재 파일 포지션부터 입력받은 버퍼의 내용을 기록한다.
 * SN3MFI 객체의 pFile이 NULL이면
 * 필요한 만큼의 메모리를 새로 할당하고,
 * 기록 후의 포지션이 Limit을 넘으면
 * 필요한 만큼의 메모리를 추가로 할당한다.
 * 기록후 읽은 바이트수 만큼 파일 포지션을 증가시킨다.
 * @param pMFI SN3MFI 포인터
 * @param pBuffer 파일에 기록할 버퍼
 * @param pSize pBuffer의 데이타형 크기
 * @param pCount 기록할 개수
 * @return	메모리 오류가 나면 0을
 *					기록되었으면 기록한 개수를 반환.
 */
size_t sn3mfi_fwrite(SN3MFI *pMFI, __uint8 *pBuffer, size_t pSize, size_t pCount);


// SN3BUF //////////////////////////////////////////////////////
// Buffer init & free
/**
 * UCS2-LE 버퍼를 초기화 한다.
 * @param	pBuf	버퍼 포인터의 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3buf_init(SN3BUF **pBuf);
/**
 * UCS2-LE 버퍼의 메모리를 반환한다.
 * @param	pBuf	버퍼의 포인터
 * @return	정상적으로 메모리를 반환한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3buf_free(SN3BUF *pBuf);

// Buffer misc
/**
 * 버퍼가 비어있는지 확인한다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @return	비어있다면 1
 *          비어있지 않다면 0 을 반환
 */
int sn3buf_isempty(SN3BUF *pBuf);
/**
 * UCS2-LE 버퍼의 크기를 반환한다.
 * @param	pBuf	버퍼의 포인터
 * @return	버퍼의 크기를 반환.
 */
size_t sn3buf_size(SN3BUF *pBuf);
/**
* 버퍼를 비운다.
* @param  pBuf  버퍼의 포인터
* @return 버퍼를 비운 후 SN3OK 반환
*/
int sn3buf_clear(SN3BUF *pBuf);
/**
* 첫번째 매개변수 버퍼 뒤에 두번째 매개변수 버퍼를 붙인다.
* @param  pBuf  버퍼의 포인터
* @param  pBufAdd  덧붙일 버퍼의 포인터
* @return 정상적으로 버퍼가 덧붙여졌다면 SN3OK반환.
*		  문제가 있는 경우에는 해당 오류코드 반환.
*/
int sn3buf_append(SN3BUF *pBuf, SN3BUF *pBufAdd);

// Buffer Unloading
/**
 * UCS2-LE 버퍼의 내용을 지정한 encoding 형태로 MFI에 출력한다.
 * @param	pBuf	버퍼의 포인터
 * @param	pMFI	MFI의 포인터
 * @param	pEncoding	Endocding 타입
 * @return	정상적으로 메모리를 반환한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3buf_unload_m(SN3BUF *pBuf, SN3MFI *pMFI, __int32 pEncoding);
/**
 * UCS2-LE 버퍼의 내용을 지정한 encoding 형태로
 * 지정경로의 로컬파일에 출력한다.
 * @param	pBuf	버퍼의 포인터
 * @param	pFilePath   출력 파일경로
 * @param	pEncoding	Endocding 타입
 * @return	정상적으로 메모리를 반환한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3buf_unload(SN3BUF *pBuf, __uint8 *pFilePath, __int32 pEncoding);
/**
 * UCS2-LE 버퍼의 내용을 지정한 encoding 형태로
 * 지정경로의 로컬파일에 출력한다.
 * @param	pBuf	버퍼의 포인터
 * @param	pFilePath   출력 파일경로 (유니코드 경로)
 * @param	pEncoding	Endocding 타입
 * @return	정상적으로 메모리를 반환한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3buf_wunload(SN3BUF *pBuf, __ucs2 *pFilePath, __int32 pEncoding);

// Buffer Put (UCS2 Version)
/**
 * UCS2-LE 문자를 버퍼에 넣는다. 버퍼에는 항상 정상적인
 * 유니코드 문자가 LE 형태로 있어야한다. SN3NOCHAR나
 * SN3NULL 등도 들어갈 수 없다. 버퍼크기가 부족하면 버퍼를 늘린다.
 * @param	pBuf	버퍼의 포인터
 * @param	ch		UCS2 문자
 * @return	정상적으로 입력된 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3buf_putc_ucs2_raw(SN3BUF *pBuf, __ucs2 ch);
/**
 * UCS2-LE 문자를 버퍼에 넣는다. 버퍼에는 항상 정상적인
 * 유니코드 문자가 LE 형태로 있어야한다. SN3NOCHAR나
 * SN3NULL 등도 들어갈 수 없다. 버퍼크기가 부족하면 버퍼를 늘린다.
 * @param	pBuf	버퍼의 포인터
 * @param	ch		UCS2 문자
 * @return	정상적으로 입력된 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3buf_putc_ucs2(SN3BUF *pBuf, __ucs2 ch);
/**
 * UCS2-LE 문자열을 버퍼에 넣는다. UCS2-LE 문자열의 끝에
 * SN3NULL이 꼭 있어야하며, 버퍼에 SN3NULL은 들어가지 않는다.
 * 문자열중에 SN3NOCHAR 등이 있으면 무시하고 진행한다.
 * @param	pBuf	버퍼의 포인터
 * @param	str		UCS2 문자열
 * @return	정상적으로 입력된 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3buf_puts_ucs2(SN3BUF *pBuf, __ucs2 *str);
/**
 * UCS2-BE 문자열을 버퍼에 넣는다. UCS2-BE 문자열의 끝에
 * SN3NULL이 꼭 있어야하며, 버퍼에 SN3NULL은 들어가지 않는다.
 * 문자열중에 SN3NOCHAR 등이 있으면 무시하고 진행한다.
 * @param	pBuf	버퍼의 포인터
 * @param	str		UCS2 문자열
 * @return	정상적으로 입력된 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3buf_puts_ucs2_be(SN3BUF *pBuf, __ucs2 *str);
/**
 * UCS2-BE 문자열을 버퍼에 넣는다. UCS2-BE 문자열의 끝에
 * SN3NULL이 꼭 있어야하며, 버퍼에 SN3NULL은 들어가지 않는다.
 * 문자열중에 SN3NOCHAR 등이 있으면 무시하고 진행한다.
 * @param	pBuf	버퍼의 포인터
 * @param	str		UCS2 문자열
 * @return	정상적으로 입력된 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3buf_put_newline(SN3BUF *pBuf);
/**
 * 버퍼에 공백 문자를 입력.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @return	정상적으로 입력된경우 SN3OK 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3buf_put_space(SN3BUF *pBuf);

// Buffer Peek & Get (UCS2 Version)
/**
 * 버퍼에 제일 처음에 입력된 문자를 확인한다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @return	정상적으로 수행되었다면
 *          첫번째 문자(__ucs2)를 반환.
 *          버퍼가 비어있다면 SN3NOCHAR 반환.
 */
__ucs2 sn3buf_peekstart(SN3BUF *pBuf);
/**
 * 버퍼에 제일 마지막에 입력된 문자를 확인한다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @return	정상적으로 수행되었다면
 *          마지막문자(__ucs2)를 반환.
 *          버퍼가 비어있다면 SN3NOCHAR 반환.
 */
__ucs2 sn3buf_peekend(SN3BUF *pBuf);
/**
 * 버퍼의 가장 앞에 있는 UCS2-LE 문자를 읽어온다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @return	버퍼에서 읽어낸 유니코드를 반환
 *          버퍼에 비었으면 SN3NOCHAR를 반환
 */
__ucs2 sn3buf_getwch(SN3BUF *pBuf);
/**
 * 버퍼의 앞쪽에 UCS2-LE 문자를 넣는다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @param	ch		넣을 유니코드 문자
 * @return	별문제 없으면 SN3OK,
 *          버퍼의 앞쪽이 꽉찼으면 오류코드를 반환
 */
int sn3buf_ungetwch(SN3BUF *pBuf, __ucs2 ch);
/**
 * 버퍼에서 UCS2-LE 문자열을 읽어온다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @param	buf		받아올 버퍼의 포인터
 * @param	buf_size	받아올 버퍼의 크기
 * @return	읽어서 채운 유니코드 갯수(size_t)를 반환
 *          문제가 있다면 0을 반환.
 */
size_t sn3buf_get_ucs2(SN3BUF *pBuf, __ucs2 *buf, int buf_size);

// Buffer Put & Get (CP949 Version)
/**
 * MS-CP949 문자를 버퍼에 넣는다.
 * @param	pBuf	버퍼의 포인터
 * @param	ch		MS-CP949 문자
 * @return	정상적으로 입력된 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3buf_putc_cp949(SN3BUF *pBuf, __uint16 ch);
/**
 * MS-CP949 문자열을 버퍼에 넣는다. 문자열이 꼭 NULL로
 * 끝나야겠다.
 * @param	pBuf	버퍼의 포인터
 * @param	str		MS-CP949 문자열
 * @return	정상적으로 입력된 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3buf_puts_cp949(SN3BUF *pBuf, __uint8 *str);
/**
 * 버퍼에서 MS-CP949 문자열을 읽어온다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @param	buf		받아올 버퍼의 포인터
 * @param	buf_size	받아올 버퍼의 크기
 * @return	읽어서 채운 바이트수(size_t)를 반환
 *          문제가 있거나 더이상 가져올게 없으면 0을 반환.
 */
size_t sn3buf_get_cp949(SN3BUF *pBuf, __uint8 *buf, int buf_size);

// Buffer position
/**
 * 버퍼의 포지션을 셋팅 한다.
 * pos 가 0 보다 작은 경우 시작점으로 채워진 값보다 큰경우는 마지막으로 이동.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @param	pos		지정한 버퍼의 포지션
 * @return
 */
void sn3buf_setpos(SN3BUF *pBuf, size_t pos);
/**
 * 버퍼의 포지션을 시작점으로 옮겨준다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @return  버퍼가 비어있다면 0, 비어있지 않다면 버퍼의 시작점을 반환.
 */
size_t sn3buf_getpos(SN3BUF *pBuf);
/**
 * 버퍼의 포지션을 시작점으로 옮겨준다.
 * @param	pBuf	유니코드 버퍼의 포인터
 */
void sn3buf_rewind(SN3BUF *pBuf);

// Text getter
/**
 * 버퍼에서 지정한 인코딩으로 문자열을 읽어온다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @param	buf		받아올 버퍼의 포인터
 * @param	buf_size	받아올 버퍼의 크기
 * @param	encoding	저장할 인코딩
 * @return	읽어서 채운 바이트수(size_t)를 반환
 *          문제가 있거나 더이상 가져올게 없으면 0을 반환.
 */
size_t sn3buf_get_text(SN3BUF *pBuf, __uint8 *buf, int buf_size, int encoding);
/**
 * 버퍼에서 지정한 인코딩으로 문자열을 읽어온다.
 * @param	pBuf	유니코드 버퍼의 포인터
 * @param	buf		받아올 버퍼의 포인터
 * @param	buf_size	받아올 버퍼의 크기
 * @param	encoding	저장할 인코딩
 * @return	읽어서 채운 바이트수(size_t)를 반환
 *          문제가 있거나 더이상 가져올게 없으며 0을 반환.
 */
size_t sn3buf_get_text_le(SN3BUF *pBuf, __uint8 *buf, int buf_size, int encoding);


// SN3SUM //////////////////////////////////////////////////////
/**
 * SN3SUM 객체를 초기화한다.
 * @param	ppSum SN3SUM 포인터의 포인터
 * @return	제대로 메모리를 할당하면 SN3OK를 반환하고
 *					오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3sum_init(SN3SUM **ppSum);
/**
 * SN3SUM 객체의 메모리를 해제한다.
 * @param	pSum SN3SUM 포인터
 * @return	제대로 메모리를 해제하면 SN3OK를 반환하고
 *					오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3sum_free(SN3SUM *pSum);
/**
 * SN3SUM의 내용을 화면에 출력한다.
 * @param	pSum SN3SUM 포인터
 * @return	SN3OK를 반환한다.
 */
int sn3sum_show(SN3SUM *pSum);

// Summary Unloading ...
/**
 * SN3SUM의 내용을 SN3MFI에 인코딩 방식에 맞게 저장한다.
 * @param	pSum SN3SUM 포인터
 * @param	pMFI SN3MFI 포인터
 * @param	pEncoding 인코딩 방식
 * @return	SN3OK를 반환한다.
 */
int sn3sum_unload_m(SN3SUM *pSum, SN3MFI *pMFI, __int32 pEncoding);
/**
 * SN3SUM의 내용을 FILE에 인코딩 방식에 맞게 저장한다.
 * @param	pSum SN3SUM 포인터
 * @param	pFile FILE 포인터
 * @param	pEncoding 인코딩 방식
 * @return	파일에 제대로 저장했으면 SN3OK를 반환하고
 *			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3sum_unload_f(SN3SUM *pSum, FILE *pFile, __int32 pEncoding);
/**
 * SN3SUM의 내용을 파일에 인코딩 방식에 맞게 저장한다.
 * @param	pSum SN3SUM 포인터
 * @param	pFilePath 파일명
 * @param	pEncoding 인코딩 방식
 * @return	파일에 제대로 저장했으면 SN3OK를 반환하고
 *			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3sum_unload(SN3SUM *pSum, __uint8 *pFilePath, __int32 pEncoding);
/**
 * SN3SUM의 내용을 파일에 인코딩 방식에 맞게 저장한다.
 * @param	pSum SN3SUM 포인터
 * @param	pFilePath 파일명
 * @param	pEncoding 인코딩 방식
 * @return	파일에 제대로 저장했으면 SN3OK를 반환하고
 *			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3sum_wunload(SN3SUM *pSum, __ucs2 *pFilePath, __int32 pEncoding);

// Docinfo
/**
* 파일의 요약정보를 출력한다.
* @param  pFilePath 파일명
* @param  pSum	SN3SUM 포인터
* @return 요약정보가 정상적으로 출력되면 SN3OK가 반환되고
*			도중에 오류가 발생하면 해당 오류코드를 반환한다.
*/
int sn3flt_docinfo(__uint8 *pFilePath, SN3SUM *pSum);
/**
* 유니코드 경로의 파일의 요약정보를 출력한다.
* @param  pFilePath 파일명
* @param  pSum	SN3SUM 포인터
* @return 요약정보가 정상적으로 출력되면 SN3OK가 반환되고
*			도중에 오류가 발생하면 해당 오류코드를 반환한다.
*/
int sn3flt_wdocinfo(__ucs2 *pFilePath, SN3SUM *pSum);
/**
* 메모리에 있는 파일의 요약정보를 출력한다.
* @param  pMFI SN3MFI 포인터
* @param  pSum	SN3SUM 포인터
* @return 요약정보가 정상적으로 출력되면 SN3OK가 반환되고
*			도중에 오류가 발생하면 해당 오류코드를 반환한다.
*/
int sn3flt_docinfo_m(SN3MFI *pMFI, SN3SUM *pSum);
/**
 * 특정 파일의 DocumentSummaryInformation을 SN3BUF에 저장한다.
 * @param	pFilePath 파일명
 * @param	pBuf SN3BUF의 포인터
 * @return	SummaryInformation의 내용을 제대로 SN3BUF에 저장하면 SN3OK를 반환하고
 *			오류가 발생하면 해당 오류코드를 반환.
 */
int sn3flt_docinfoEx(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * 특정 파일의 DocumentSummaryInformation을 SN3BUF에 저장한다.
 * @param	pFilePath 파일명
 * @param	pBuf SN3BUF의 포인터
 * @return	SummaryInformation의 내용을 제대로 SN3BUF에 저장하면 SN3OK를 반환하고
 *			오류가 발생하면 해당 오류코드를 반환.
 */
int sn3flt_wdocinfoEx(__ucs2 *pFilePath, SN3BUF *pBuf);
/**
 * 메모리에 담긴 파일의 DocumentSummaryInformation을 SN3BUF에 저장한다.
 * @param	pMFI SN3MFI 포인터
 * @param	pBuf SN3BUF의 포인터
 * @return	SummaryInformation의 내용을 제대로 SN3BUF에 저장하면 SN3OK를 반환하고
 *			오류가 발생하면 해당 오류코드를 반환.
 */
int sn3flt_docinfoEx_m(SN3MFI *pMFI, SN3BUF *pBuf);

// Filter (FilePath) ///////////////////////////////////////////
/**
 * 파일 필터링 후 결과 텍스트를 버퍼에 기록한다.
 * @param	pFilePath	대상 파일 경로
 * @param   pBuf  추출한 텍스트가 저장될 SN3BUF 포인터
 * @param   WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	성공: SN3OK, 실패: 해당 에러코드
 */
int sn3flt_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
* 파일 필터링 후 결과 텍스트를 파일에 기록한다. (len을 wcslen()으로 구함)
* @param *pFilePath 입력파일 경로
* @param *pOutPath 출력파일 경로. NULL일 경우 stdout에 기록
* @param WithPage 페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
* @param encoding 출력 텍스트 인코딩
* @return 성공: SN3OK, 실패: 해당 에러코드
*/
int sn3flt_filter_ex(__uint8 *pFilePath, __uint8 *pOutPath, int WithPage, int encoding);
/**
 * 파일 필터링 후 결과 텍스트를 버퍼에 기록한다.
 * @param	pFilePath	대상 파일 경로
 * @param   pBuf  추출한 텍스트가 저장될 SN3BUF 포인터
 * @param   WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	성공: SN3OK, 실패: 해당 에러코드
 */
int sn3flt_wfilter(__ucs2 *pFilePath, SN3BUF *pBuf, int WithPage);

/**
 * alz 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	alz 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage	 페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3alz_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * bzip 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	bzip 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3bzip_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * chm 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	chm 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3chm_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * doc 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	doc 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3doc_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * docx 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	docx 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3docx_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * dwg 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	dwg 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3dwg_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * GZ(GNU Zip) 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	GZ 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3gz_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * h2k 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	h2k 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3h2k_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * htm / html 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	htm / html 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3htm_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwn 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	hwn 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3hwn_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwd 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	hwd 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3hwd_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwp3 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	hwp3 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3hwp3_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwx 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	hwx 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3hwx_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * jtd 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	jtd 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3jtd_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * mdb 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	mdb 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3mdb_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * mdi 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	mdi 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3mdi_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * mht 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	mht 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3mht_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * mp3 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	mp3 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3mp3_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * msg 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	msg 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3msg_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * pdf 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	pdf 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3pdf_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * ppt 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	ppt 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3ppt_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * pptx 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	pptx 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3pptx_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * rtf 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	rtf 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3rtf_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * 7zip 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	7zip 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3sevenzip_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * swf 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	swf 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3swf_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * sxx 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	sxx 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3sxx_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * tar 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	tar 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3tar_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * txt 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	txt 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3txt_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * wpd 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	wpd 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3wpd_filter( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xls 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	xls 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3xls_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xlsx 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	xlsx 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3xlsx_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwp 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	hwp 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3xml_hwp_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xml office 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	xml office 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3xml_office_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * zip 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	zip 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3zip_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * rar 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	rar 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3rar_filter( __uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * ndoc 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	ndoc 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3ndoc_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);

/**
 * nsf 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	nsf 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3nsf_filter(__uint8* pFilePaht, SN3BUF* pBuf);
/**
 * edb 파일을 버퍼에 필터링 한다.
 * @param	pFilePath	edb 파일 경로
 * @param	pBuf	추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3edb_filter(__uint8* pFilePaht, SN3BUF* pBuf);

// Filter (MFI) ////////////////////////////////////////////////
/**
 * 메모리에 담긴 파일 포맷 필터링 후 포맷에 맞게 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI 소스 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3flt_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);

/**
 * alz 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI alz 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3alz_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * bzip 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI bzip 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3bzip_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * chm 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI chm 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3chm_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * doc 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI doc 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3doc_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * docx 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI docx 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3docx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * dwg 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI dwg 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3dwg_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * GZ 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI GZ 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3gz_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * h2k 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI h2k 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3h2k_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * htm 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI htm 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3htm_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * hwn 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI hwn 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3hwn_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * hwd 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI hwd 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3hwd_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * hwp3 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI hwp3 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3hwp3_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * hwx 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI hwx 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3hwx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * jtd 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI jtd 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3jtd_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * mdb 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI mdb 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3mdb_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * mdi 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI mdi 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3mdi_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * mht 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI mht 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3mht_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * mp3 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI mp3 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3mp3_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * msg 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI msg 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3msg_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * pdf 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI pdf 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3pdf_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * ppt 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI ppt 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3ppt_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * pptx 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI pptx 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3pptx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * rtf 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI rtf 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3rtf_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * 7zip 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI 7zip 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3sevenzip_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * swf 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI swf 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3swf_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * sxx 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI sxx 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3sxx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * tar 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI tar 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage 페이지 구분자 출력 여부.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3tar_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * txt 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI txt 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3txt_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * wpd 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI wpd 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3wpd_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xls 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI xls 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3xls_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xlsx 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI xlsx 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3xlsx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf );
/**
 * xml_hwp 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI xml_hwp 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3xml_hwp_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xml office 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI xml office 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3xml_office_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * zip 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI zip 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3zip_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * rar 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI rar 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3rar_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * ndoc 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI ndoc 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3ndoc_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);

/**
 * nsf 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI nsf 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3nsf_filter_m(SN3MFI* pMFI, SN3BUF* pBuf);
/**
 * edb 파일 내용을 버퍼에 필터링한다.
 * @param	pMFI edb 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3edb_filter_m(SN3MFI* pMFI, SN3BUF* pBuf);

// Filter (MFI) with Format Code ///////////////////////////////
/**
 * 메모리에서 인자로 들어오는 번호에 해당하는 포맷 파일을 버퍼에 필터링한다.
 * @param	pMFI 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	WithPage  페이지 구분자 출력 여부. 1이면 출력, 0이면 출력안함.
 * @param	FileFormat 파일 포맷 해당 번호
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3flt_filter_c( SN3MFI *pMFI, SN3BUF *pBuf, int WithPage, int FileFormat);
/**
 * 메모리에서 인자로 들어오는 인코딩으로 txt 파일을 버퍼에 필터링한다.
 * @param	pMFI 파일이 담긴 메모리 포인터
 * @param	pBuf 추출한 텍스트가 저장될 SN3BUF 포인터
 * @param	FileFormat 인코딩 번호
 * @return	제대로 필터링해서 버퍼에 쓰면 SN3OK 를 반환하고
			오류가 발생하면 해당 오류코드를 반환한다.
 */
int sn3txt_filter_c( SN3MFI *pMFI, SN3BUF *pBuf, int FileFormat);


// File(sheet,table) list (FilePath) ///////////////////////////
/**
 * alz파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pFilePath	alz 파일 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3alz_filelist( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * GZ파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pFilePath	gz 파일 경로
 * @param	*pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3gz_filelist(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * mdb파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pFilePath	mdb 파일 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3mdb_filelist( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * 7zip파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pFilePath	7zip파일 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3sevenzip_filelist( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * tar파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pFilePath	tar 파일 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3tar_filelist(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xls파일의 시트 목록을 출력한다.
 *
 * @param	pFilePath	xls 파일 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3xls_sheetlist ( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xlsx파일의 시트 목록을 출력한다.
 *
 * @param	pFilePath	xlsx 파일 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3xlsx_sheetlist ( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * zip파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pFilePath	zip 파일 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3zip_filelist(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * rar파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pFilePath	rar 파일 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3rar_filelist(__uint8 *pFilePath, SN3BUF *pBuf);


// File(sheet,table) list (MFI) ////////////////////////////////
/**
 * alz파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	alz파일이 담긴 메모리 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3alz_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * GZ파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	gz파일이 담긴 메모리 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3gz_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * mdb파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	mdb파일이 담긴 메모리 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3mdb_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * 7zip파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	7zip파일이 담긴 메모리 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3sevenzip_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * tar파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	tar파일이 담긴 메모리 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3tar_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xls파일의 시트 목록을 출력한다.
 *
 * @param	pMFI	xls파일이 담긴 메모리 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3xls_sheetlist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xlsx파일의 시트 목록을 출력한다.
 *
 * @param	pMFI	xlsx파일이 담긴 메모리 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3xlsx_sheetlist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * zip파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	zip파일이 담긴 메모리 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3zip_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * rar파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	rar파일이 담긴 메모리 경로
 * @param	pBUF	SN3BUF 포인터
 * @return	정상적으로 메모리를 할당받고 초기화한 경우 SN3OK를 반환.
 *          문제가 있다면 해당 오류코드를 반환.
 */
int sn3rar_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);

// File(sheet,table) raw list (MFI) ////////////////////////////////
/**
* 압축 파일 정보를 담고 있는 SN3ARFILIST를 생성하고 초기화한다.
* SN3ARFILIST 사용하기 전 반드시 초기화해야하며 사용이 끝나면 snf_arfilist_free()로 해제해야 한다.
* @param	ppList  대상 SN3ARFILIST의 더블 포인터
* @return	성공하면 SN3OK를, 실패하면 에러코드를 반환한다.
*/
int sn3arfilist_init(SN3ARFILIST** ppList);
/**
* SN3ARFILIST를 메모리 해제한다.
* @param	pList  메모리 해제할 SN3ARFILIST 포인터
* @return	성공하면 SN3OK를, 실패하면 에러코드를 반환한다.
*/
void sn3arfilist_free(SN3ARFILIST* pList);
/**
* 아카이브 파일 리스트(SN3ARFILIST)에서 idx번째 raw파일의 이름을 반환한다.
* @param	pList 이름을 추출할 SN3ARFILIST 포인터
* @param	idx	추출할 파일의 파일 목록 내 위치 (0-based)
* @return	SN3ARFLIST의 idx번째 파일의 이름이 ucs2 문자열로 리턴된다.실패 시 에러코드 반환.
*/
__uint8* sn3arfilist_name(SN3ARFILIST* pList, int idx);
/**
* 아카이브 파일 리스트(SN3ARFILST)의 idx번째 출력용 파일 이름을 반환한다.
* pBuf에 출력용 파일 이름이 덧붙여지고, 필요하면 snf_buf_clear()로 버퍼를 비워줘야 한다.
* @param	pList 이름을 추출할 SN3ARFILIST 포인터
* @param	idx	추출할 파일의 파일 목록 내 위치 (0-based)
* @param	pBuf 파일 이름이 담긴 SN3BUF 포인터
* @return	성공 시 SN3OK를, 실패하면 에러코드를 반환한다.
*/
int sn3arfilist_printname(SN3ARFILIST* pList, int idx, SN3BUF* pBuf);
/**
* SN3ARFILIST가 갖고 있는 파일 목록 개수를 반환한다.
* @param	pList SN3ARFILIST 포인터
* @return	성공 시 SN3OK를, 실패하면 에러코드를 반환한다.
*/
int sn3arfilist_count(SN3ARFILIST* pList);

/**
 * alz파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	alz파일이 담긴 메모리 경로
 * @param	pList	SN3ARFILIST 포인터
 * @return  SN3OK 또는 오류코드
 */
int sn3alz_filelistEx_m(SN3MFI *pMFI, SN3ARFILIST* pList);
/**
 * 7zip 파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	7zip파일이 담긴 메모리 경로
 * @param	pList	SN3ARFILIST 포인터
 * @return  SN3OK 또는 오류코드
 */
int sn3sevenzip_filelistEx_m(SN3MFI *pMFI, SN3ARFILIST* pList);
/**
 * tar파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	tar파일이 담긴 메모리 경로
 * @param	pList	SN3ARFILIST 포인터
 * @return  SN3OK 또는 오류코드
 */
int sn3tar_filelistEx_m(SN3MFI *pMFI, SN3ARFILIST* pList);
/**
 * zip파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	zip파일이 담긴 메모리 경로
 * @param	pList	SN3ARFILIST 포인터
 * @return  SN3OK 또는 오류코드
 */
int sn3zip_filelistEx_m(SN3MFI *pMFI, SN3ARFILIST* pList);
/**
 * rar파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	rar파일이 담긴 메모리 경로
 * @param	pList	SN3ARFILIST 포인터
 * @return  SN3OK 또는 오류코드
 */
int sn3rar_filelistEx_m(SN3MFI *pMFI, SN3ARFILIST* pList);
/**
 * egg파일의 압축된 파일 목록을 출력한다.
 *
 * @param	pMFI	egg파일이 담긴 메모리 경로
 * @param	pList	SN3ARFILIST 포인터
 * @return  SN3OK 또는 오류코드
 */
int sn3egg_filelistEx_m(SN3MFI *pMFI, SN3ARFILIST* pList);

// Extract file from Archive ///////////////////////////////////
/**
* alz 압축 파일 내에 지정된 압축 파일을 풀어 SN3MFI에 쓴다.
* @param	pMFI 압축 파일이 열린 SN3MFI 포인터
* @param	pUzFile 압축 해제된 파일이 쓰여질 SN3MFI 포인터
* @param	pFileNm 압축 해제할 파일의 경로
* @return	성공 시 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int sn3alz_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* 7zip 압축 파일 내에 지정된 압축 파일을 풀어 SN3MFI에 쓴다.
* @param	pMFI 압축 파일이 열린 SN3MFI 포인터
* @param	pUzFile 압축 해제된 파일이 쓰여질 SN3MFI 포인터
* @param	pFileNm 압축 해제할 파일의 경로
* @return	성공 시 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int sn3sevenzip_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* tar 압축 파일 내에 지정된 압축 파일을 풀어 SN3MFI에 쓴다.
* @param	pMFI 압축 파일이 열린 SN3MFI 포인터
* @param	pUzFile 압축 해제된 파일이 쓰여질 SN3MFI 포인터
* @param	pFileNm 압축 해제할 파일의 경로
* @return	성공 시 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int sn3tar_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* zip 압축 파일 내에 지정된 압축 파일을 풀어 SN3MFI에 쓴다.
* @param	pMFI 압축 파일이 열린 SN3MFI 포인터
* @param	pUzFile 압축 해제된 파일이 쓰여질 SN3MFI 포인터
* @param	pFileNm 압축 해제할 파일의 경로
* @return	성공 시 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int sn3zip_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* rar 압축 파일 내에 지정된 압축 파일을 풀어 SN3MFI에 쓴다.
* @param	pMFI 압축 파일이 열린 SN3MFI 포인터
* @param	pUzFile 압축 해제된 파일이 쓰여질 SN3MFI 포인터
* @param	pFileNm 압축 해제할 파일의 경로
* @return	성공 시 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int sn3rar_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* bzip 압축 파일 내에 지정된 압축 파일을 풀어 SN3MFI에 쓴다.
* @param	pMFI 압축 파일이 열린 SN3MFI 포인터
* @param	pUzFile 압축 해제된 파일이 쓰여질 SN3MFI 포인터
* @return	성공 시 SN3OK를, 실패 시 오류코드를 반환한다.
*/
int sn3bzip_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile);

// User Callback Function Define ///////////////////////////////////
/**
 * 사용자 정의 함수를 세팅한다.
 *
 * @param pBuf			   버퍼의 포인터
 * @param snf_buf_user_func 사용자 정의 함수 포인터
 */
void sn3buf_set_user_func( SN3BUF *pBuf, void(* sn3buf_user_func)(SN3BUF* pBuf, void* pUserData) );
/**
 * 사용자 명령을 세팅한다.
 *
 * @param pBuf				버퍼의 포인터
 * @param snf_user_command	사용자 명령
 */
void sn3buf_set_user_command(SN3BUF *pBuf, int sn3_user_command);
/**
 * 사용자 데이터를 세팅한다.
 *
 * @param pBuf			버퍼의 포인터
 * @param pUserData		사용자 데이터 포인터
 */
void sn3buf_set_user_data(SN3BUF *pBuf, void* pUserData);

// User Marker Callback Function Define
#ifdef __cplusplus
/**
 * 사용자 콜백 마크 함수를 세팅한다.
 *
 * @param pBuf				버퍼의 포인터
 * @param snf_buf_marker_func 사용자 콜백 마커 함수 포인터
 */
void sn3buf_set_marker_func(SN3BUF *pBuf, int(* sn3buf_marker_func)(SN3BUF* pBuf, void* pMarkerData, SN3MARKER *pMarker)=NULL);
#else
/**
 * 사용자 콜백 마크 함수를 세팅한다.
 *
 * @param pBuf				버퍼의 포인터
 * @param snf_buf_marker_func 사용자 콜백 마커 함수 포인터
 */
void sn3buf_set_marker_func(SN3BUF *pBuf, int(* sn3buf_marker_func)(SN3BUF* pBuf, void* pMarkerData, SN3MARKER *pMarker));
#endif //__cplusplus

/**
 * 사용자 콜백 마크를 세팅한다.
 *
 * @param pBuf			버퍼의 포인터
 * @param pUserData		사용자 데이터 포인터
 */
void sn3buf_set_marker_data(SN3BUF *pBuf, void* pMarkerData);
/**
 * 사용자 콜백 마커S KIP 상태의 Setter 함수
 *
 * @param pBuf				버퍼의 포인터
 * @param snf_skip_command	스킵명령
 */
void sn3buf_set_skip_command(SN3BUF *pBuf, int sn3_skip_command);
/**
 * 사용자 콜백 마커 SKIP 상태의 Getter 함수
 *
 * @param pBuf			버퍼의 포인터
 * @return int			스킵명령
 */
int sn3buf_get_skip_command(SN3BUF *pBuf);

// User Image Callback Function Define ////////////////////////////
/**
* 이미지 추출 callback setter 함수
*
* @param pBuf						버퍼의 포인터
* @param wsnf_buf_set_img_flt_func	callback 함수
*/
int snf_buf_set_img_flt_func(SN3BUF *pBuf, bool(*sn3buf_img_flt_func)(void* pUserData, const __uint8* pStream, const size_t len, const __int32 imgIndex));
/**
* 이미지 추출 callback user data를 지정하는 함수
*
* @param pBuf						버퍼의 포인터
* @param pUserData					User Data의 포인터
*/
int snf_buf_set_img_user_data(SN3BUF *pBuf, void* pUserData);
/**
* 이미지 추출 callback setter 함수
*
* @param pBuf						버퍼의 포인터
* @param wsnf_buf_set_img_flt_func	callback 함수
*/
int snf_buf_set_txt_with_imgmarker_flt_func(SN3BUF *pBuf, bool(*sn3buf_txt_with_imgmarker_flt_func)(SN3BUF* pBuf, void* pUserData, const __int32 imgIndex));
/**
* 이미지 추출 callback setter 함수
*
* @param pBuf						버퍼의 포인터
* @param wsnf_buf_set_img_flt_with_info_func	callback 함수
*/
int snf_buf_set_img_flt_with_info_func(SN3BUF *pBuf, __int32(*sn3buf_img_flt_with_info_func)(void* pUserData, const __uint8* pStream, const size_t len, const SN3IMGINFO imginfo));

// Memory Limit
/**
 * memory limit을 설정합니다.
 * @param limit	설정할 memory limit
 * @return size_t 설정된 메모리 크기
 */
int sn3set_memory_limit(int limit);
/**
 * memory limit으로 설정된 값을 반환합니다.
 * @return size_t 설정된 메모리 크기
 */
size_t sn3mem_getMemoryLimit();
/**
 * 매개변수를 복사하고 복사된 문자열의 포인터를 반환한다.
 * @param _Src 복사할 문자
 * @return 복사된 문자의 포인터
 */
char* sn3strdup(const char* _Src);

/**
* 동적으로 할당된 매개변수의 메모리를 해제한다.
* @param PTR 메모리 해제할 동적 할당된 변수
*/
void sn3free(void *PTR);
#ifdef __cplusplus
}
#endif //__cplusplus

#endif /* SN3_H */
