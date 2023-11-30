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
 *	�� ���α׷��� (��)���̳�����Ʈ �ڻ��Դϴ�.
 *  (��)���̳�����Ʈ�� ���� ���Ǿ��� �����ϰų�
 *  �κ� ������ �� �����ϴ�.
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
#define SN3OPTION_COMPRESSION_IGNORE_EXTENSION_LIST			0x100000000L	// �������� �� ���� Ȯ���� ���� �ɼ�
#define SN3OPTION_NO_WITHPAGE								0x200000000L	// PDF ������ ���ڿ� ���� �ɼ�
#define SN3OPTION_ANNOTATION_SEPARATE						0x400000000L	// Annotation Marking
#define SN3OPTION_HTM_NO_SEPCIAL_CHAR						0x800000000L	// HTM���� &lt; &gt;�� �±�ó�� ó���ϴ� �ɼ�
#define SN3OPTION_EXCEL_USE_FILTERCACHE						0x1000000000L	// XLS���� cache data ���͸� on/off �ɼ�
#define SN3OPTION_EXCEL_USE_FILTERPHONETIC					0x2000000000L	// XLS���� ���� ���͸� on/off �ɼ�
#define SN3OPTION_ARCHIVE_RETURNCODE_CHECK					0x4000000000L	// ���� ������ �����ڵ尡 SN3OK �� �ƴϸ� 40101 ����
#define SN3OPTION_DB_EMPTY_SEPARATE							0x8000000000L
#define SN3OPTION_DONT_USE_EXCEPTION_HANDLING				0x10000000000L	// out of exception handling
#define SN3OPTION_EXTRACT_HYPERLINK							0x20000000000L  // �����۸�ũ ����(only PDF)
#define SN3OPTION_EXCEL_FILTER_FORMULA						0x40000000000L  // �������Ͽ��� ���� �Լ������� �����ϴ� �ɼ�
#define SN3OPTION_MAIL_MULTI_FILTER							0x80000000000L // EML, MHT ���� ��� ������ �� �����ϴ� �ɼ�
#define SN3OPTION_USE_NUMBER_FORMAT							0x100000000000L // ǥ������ ����� �̿��Ͽ� ������
#define SN3OPTION_BOOKMARKER								0x200000000000L // å���� ���͸� �ɼ� 
#define SN3OPTION_PDF_BOOKMARKER							0x200000000000L // PDF å���� ���͸� �ɼ�
#define SN3OPTION_PDF_COORD_BASED_OUTPUT					0x400000000000L // PDF ��ǥ ���� ���
#define SN3OPTION_XML_TAG_FILTER							0x800000000000L // XML ���� �±� ���͸� �ɼ�
#define SN3OPTION_WITHPAGE_SHEETNAME						0x1000000000000L // 'SHEET:��Ʈ�̸�' ���͸� �ɼ�
#define SN3OPTION_IGNORE_REPEATED_IMAGE						0x2000000000000L // �ݺ��Ǵ� �̹����� �����ϴ� �ɼ�
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
#define SN3OPTION_EXTRACT_HYPERLINK							0x20000000000LL  // �����۸�ũ ����(only PDF)
#define SN3OPTION_EXCEL_FILTER_FORMULA						0x40000000000LL  // �������Ͽ��� ���� �Լ������� �����ϴ� �ɼ�
#define SN3OPTION_MAIL_MULTI_FILTER							0x80000000000LL // EML, MHT ���� ��� ������ �� �����ϴ� �ɼ�
#define SN3OPTION_USE_NUMBER_FORMAT							0x100000000000LL // ǥ������ ����� �̿��Ͽ� ������
#define SN3OPTION_BOOKMARKER								0x200000000000LL // å���� ���͸� �ɼ� 
#define SN3OPTION_PDF_BOOKMARKER							0x200000000000LL // PDF å���� ���͸� �ɼ�
#define SN3OPTION_PDF_COORD_BASED_OUTPUT					0x400000000000LL // PDF ��ǥ ���� ���
#define SN3OPTION_XML_TAG_FILTER							0x800000000000LL // XML ���� �±� ���͸� �ɼ�
#define SN3OPTION_WITHPAGE_SHEETNAME						0x1000000000000LL // 'SHEET:��Ʈ�̸�' ���͸� �ɼ�
#define SN3OPTION_IGNORE_REPEATED_IMAGE						0x2000000000000LL // �ݺ��Ǵ� �̹����� �����ϴ� �ɼ�
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
* @brief	�ɼǵ��� ����� param�� �����ϴ� ����ü (����)
*/
typedef struct t_SN3OPTION_PARAM{ 
	__int64 MaxCompressionFileSize;		/**< ���͸��� ���������� �ִ�ũ��(<�� ���� ���͸�) -1 : ���� ���� */
	__int64 MaxFileSizeToExtract;		/**< ���͸��� ����� ������ �ִ� ũ��(<�� ���� ���͸�) -1 : ���Ѿ��� */
	__int32 MaxArchiveLevel;			/**< ���͸��� ���� ����(<�� ���� ���͸�) -1 : ���Ѿ��� */
	__int32 MinArchiveSizeLimitLevel;	/**< ������ ����� �ּ� ���� ����(>�� ���� ����) */
	__int32 TextEncoding;				/**< �⺻ �ؽ�Ʈ ���ڵ� (�ؽ�Ʈ ���� �ؼ���) */
	__int32 DefaultEncoding;			/**< �⺻ ���ڵ� */
	__int32 ArchiveFileNameEncoding;	/**< �������� �� ���� �̸� ���ڵ� */
	__int32 MaxCellLimitXLSX;			/**< xlsx �� ���� ���� */
	const char *ignoreExtList;			/**< ���� ��� Ȯ���� ��� */
}SN3OPTION_PARAM;

/**
 * @brief	���������� ���� ����ü
 */
typedef struct t_SN3SUM {
	__int32 	Format;			/**< SN3 �������� */
	__int32 	Format2;		/**< SN3 �������� */
	__ucs2* Title;				/**< ���� */
	__ucs2* Subject;			/**< ���� */
	__ucs2* Author;				/**< ���� */
	__ucs2* Date;				/**< ��¥ ���� */
	__ucs2* Keywords;			/**< Ű���� */
	__ucs2* Comments;			/**< ���� */
	__ucs2* Template;			/**< ���ø� */
	__ucs2* LastAuthor;			/**< ���� ������ */
	__ucs2* RevNumber;			/**< ���� ���� */
	__ucs2* AppName;			/**< �������α׷��� */
	__ucs2* CreateDTM;			/**< �������� */
	__ucs2* LastSaveDTM;		/**< ���� ���� �������� */
	__ucs2* AppVersion;			/**< �������α׷� ���� */
	__ucs2* contentStatus;		/**< ������ ���� */
	__ucs2* pages;				/**< ������ �� */
	__ucs2* language;			/**< ��� */
	__ucs2* words;				/**< �ܾ� �� */
	__ucs2* paragraphs;			/**< ���� �� */
	__ucs2* lines;				/**< ���� �� */
	__ucs2* characters;			/**< ���� �� */
} SN3SUM;

/**
 * @brief	��Ŀ �ݹ� - ���°�
 */
typedef enum {
	FILE_START_STATE = 1,	/**< FILE�� ���� ���� */
	FILE_END_STATE = 2,		/**< FILE�� �� ���� */
	OLE_START_STATE = 3,	/**< OLE�� ���� ���� */
	OLE_END_STATE = 4,		/**< OLE�� �� ���� */
	PAGE_START_STATE = 5,	/**< PAGE�� ���� ���� */
	PAGE_END_STATE = 6,		/**< PAGE�� �� ���� */
	UNZIP_FILE_STATE = 9,	/**< ���� ���� �� ���� ���� unzip ���� */
	ATTACHMENT_FILE_STATE = 10,	/**< ÷������ ��Ŀ �ݹ� ���� */
} SN3BUF_STATE_TYPE;

/**
 * @brief	��Ŀ �ݹ� - ��ŵ ��ɾ�
 */
typedef enum {
	NO_SKIP = 0,		/**< default */
	MARKER_SKIP = 1,	/**< ��Ŀ�� ��ŵ */
	CONTENT_SKIP = 2,	/**< ���͸� ��ŵ */
	ALL_SKIP = 3		/**< ��Ŀ���� ���͸� ��� ��ŵ */
} SN3BUF_SKIP_TYPE;

/**
 * @brief	��Ŀ������ ���� ����ü
 */
typedef struct t_SN3MARKER {
	int state;				/**< ���°�(����, ��) */
	__ucs2* marker;			/**< ��Ŀ��(�����̸�, ��������ȣ, ole��Ŀ��) */
	SN3MFI* unzipMFI;		/**< unzip file stream */
	int depth;				/**< ���� ���� �� ���� ������ depth */
	int ret;				/**< ���� (÷��) ������ ���͸� ��� �ڵ� */
}SN3MARKER;

/**
 * @brief	�̹��� ������ ���� ����ü
 */
typedef struct t_SN3IMGINFO {
	__int32 index;			/**< �̹��� index */
	__int32 formatCode;		/**< �̹��� �����ڵ� */
	__uint32 width;			/**< �̹��� �ʺ� */
	__uint32 height;		/**< �̹��� ���� */
} SN3IMGINFO;

/**
* @brief	������ Ÿ��
*/
typedef enum {
	SNF_GBL_SEPTYPE_NONE = 0,					/**< ���� */
	SNF_GBL_SEPTYPE_EXCEL_CELL = 1,				/**< ���� cell */
	SNF_GBL_SEPTYPE_EXCEL_ROW = 2,				/**< ���� row */
	SNF_GBL_SEPTYPE_EXCEL_FORMULA_START = 3,	/**< ���� ���� ���� */
	SNF_GBL_SEPTYPE_EXCEL_FORMULA_END = 4,		/**< ���� ���� �� */
	SNF_GBL_SEPTYPE_OLE_START = 5,				/**< ole ���� */
	SNF_GBL_SEPTYPE_OLE_END = 6,				/**< ole �� */
	SNF_GBL_SEPTYPE_ANNOTATION_START = 7,		/**< �ּ� ���� */
	SNF_GBL_SEPTYPE_ANNOTATION_END = 8,			/**< �ּ� �� */
	SNF_GBL_SEPTYPE_EXCEL_PIVOT_START = 9,		/**< ���� �ǹ����̺� ���� */
	SNF_GBL_SEPTYPE_EXCEL_PIVOT_END = 10,		/**< ���� �ǹ����̺� �� */
	SNF_GBL_SEPTYPE_EXCEL_CACHE_START = 11,		/**< ���� ĳ�� ���� */
	SNF_GBL_SEPTYPE_EXCEL_CACHE_END = 12,		/**< ���� ĳ�� �� */
	SNF_GBL_SEPTYPE_BOOKMARKER_START = 13,		/**< �ϸ�Ŀ ���� */
	SNF_GBL_SEPTYPE_BOOKMARKER_END = 14,		/**< �ϸ�Ŀ �� */
	SNF_GBL_SEPTYPE_HYPERLINK_START = 15,		/**< �����۸�ũ ���� */
	SNF_GBL_SEPTYPE_HYPERLINK_END = 16,			/**< �����۸�ũ �� */
} SNF_GBL_SEPTYPE;

/***************************************************************
 * Function Declarations
 ***************************************************************/
#ifdef __cplusplus
extern "C" {
#endif //__cplusplus

/**************************************************************
*                  SNF(V4 �̻�) API �Լ�                      *
***************************************************************/

// Config //////////////////////////////////////////////////////
/**
* ���� ���� ������ ����Ѵ�.
*/
void snf_gbl_showcfg();
/**
 * ���� ���� ȯ�� ������ �Ѵ�.
 * @param pKeyStr ���̼��� ��ȣ. ������ ������� �ʾ� NULL �Ǵ� ""�Է�.
 * @param Option  ���� ���� �ɼ�. Or�� �ߺ� ���� �����ϴ�.
 * @param FileType ���͸� ��� ���� ����. SN3FILETYPE_ALL�� �����ϰ� Or�� �ߺ� ���� �����ϴ�.
 * @param BaseBufSize �޸� ���� ũ��.
 */
void snf_gbl_setcfg(const char * pKeyStr, __uint64 FileType, __uint64 Option, size_t BaseBufSize);
/**
 * ���� ���� ȯ�� �� �������� ���� �ɼ��� �����Ѵ�.
 * @param pKeyStr ���̼��� ��ȣ. ������ ������� �ʾ� NULL �Ǵ� ""�Է�.
 * @param FileType ���͸� ��� ���� ����.
 * @param Option  ���� ���� �ɼ�
 * @param BaseBufSize ���͸��� ���Ǵ� ���� ũ��.
 * @param opt	  ���� ���� ���͸�, ���� ���� ���� SN3OPTION_PARAM ����ü
 */
void snf_gbl_setcfgEx(const char * pKeyStr, __uint64 FileType, __uint64 Option, size_t BaseBufSize, SN3OPTION_PARAM opt);
/**
* ���͸��� �۾� ���丮�� Ȱ���Ѵ�.
* @details �� API�� �۾� ���丮�� ����ϸ� ���� ���� ������ �޸𸮰� �ƴ϶� �ӽ� ������ Ȱ���ϰ� �ȴ�.
*		   ���ɿ��� �ణ�� �г�Ƽ�� ������ �޸� ��뷮�� �پ���.
* @param workDir �۾� ���丮 ��� (�̹� �����ϴ� ���丮���� ��)
* @param enc 1�̸� �۾� ���丮�� �ӽ� ���� ���� �� ���� ������ ��ȣȭ
* @param minSize �ش� ������ ū ���ϸ� �ӽ� ������ ����ϰ� �ȴ�. 100MB �̻� �� ����.
* @return ���͸� ���� �� SN3OK, ���н� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_gbl_set_work_dir(const __uint8* pWorkDir, int enc, __int64 minSize);
/**
* type�� �´� �����ڸ� �����Ѵ�.
* @param type ������ ������ ����
* @param separator ������
* @return ������ �����ڸ� ���������� ������ ��� SN3OK, ���н� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_gbl_set_separator(const SNF_GBL_SEPTYPE type, const __ucs2* separator);

// Utility /////////////////////////////////////////////////////
/**
* ���� �̸��� ���Ѵ�.
* @return	���� �̸��� �����Ѵ�.
*/
char* snf_ver_program();
/**
* ���� ������ ���Ѵ�.
* @return	���� ������ �����Ѵ�.
*/
char* snf_ver_version();

/**
 * MFI �����ͷκ��� ���� ������ �˾Ƴ���.
 * MFI�� ���� ��ġ�� ����ߴٰ� �ٽ� �ǵ�����.
 * @param	pMFI	MFI ������
 * @param   pFormat	�����ڵ尡 ����ȴ�.
 * @return	�������ΰ�� SN3OK ��ȯ.
 *			�������߻��Ѱ��� �ش� �����ڵ带 ��ȯ.
 */
int snf_fmt_detect_m(SN3MFI *pMFI, int *pFormat);
/**
 * ������ ���ð�ηκ��� ���� ������ �˾Ƴ���.
 * @param	pFilePath	FILE ���
 * @param   pFormat	�����ڵ尡 ����ȴ�.
 * @return	�������ΰ�� SN3OK ��ȯ.
 *			������ �߻��� ���� �ش� �����ڵ带 ��ȯ.
 */
int snf_fmt_detect(__uint8 *pFilePath, int *pFormat);
/**
* ������ ���ð�ηκ��� ���� ������ �˾Ƴ���.
* @param	pFilePath	FILE ���(�����ڵ� ���)
* @param   pFormat	�����ڵ尡 ����ȴ�.
* @return	�������ΰ�� SN3OK ��ȯ.
* ������ �߻��� ���� �ش� �����ڵ带 ��ȯ.
*/
int snf_fmt_wdetect(__ucs2 *pFilePath, int *pFormat);
/**
 * FormatCode �κ��� ������ �̸��� ã�´�.
 * @param	pFormatCode	�����ڵ�
 * @return	�����Ѱ�� ������ �̸��� ��ȯ�ϰ�
 *          �����Ѱ�� �����ڵ带 ��ȯ�Ѵ�.
 */
char* snf_fmt_format_name(int pFormatCode);

/**
 * FormatCode �κ��� ������ �̸��� ã�´�. ���� �����ϴ� ���˸� ã�´�.
 * @param	pFormatCode	�����ڵ�
 * @return	�����Ѱ�� ������ �̸��� ��ȯ�ϰ�
 *          �����Ѱ�� �����ڵ带 ��ȯ�Ѵ�.
 */
char* snf_fmt_formatcodeByName(int _formatCode);

/**
* ���� ��θ� �̿��� ���� ���͸��� ������ �������� true/false ����
* @param pFilePath  FILE ���
* @return ���͸��� �����ϸ� 1, �ƴϸ� 0�� ��ȯ�Ѵ�.
*/
int snf_fmt_isFilterFormat(__uint8 *pFilePath);
/**
* MFI�� ��� ���� ���� ���͸��� �������� true/false ����
* @param pMFI  MFI ������
* @return ���͸��� �����ϸ� 1, �ƴϸ� 0�� ��ȯ�Ѵ�.
*/
int snf_fmt_isFilterFormat_m(SN3MFI *pMFI);

/**
 * Next �����ڵ尡 (ERROR_SN3XXX_) �߸��� ����(���� ����)�� ������� Ȯ���Ѵ�.
 * @param	nErr	�����ڵ�
 * @return	�߸��� ����(���� ����) ��� ���� ������ ��ȯ.
 *          �ƴҰ�� 0�� ��ȯ
 */
int snf_err_isbadfile(int nErr);

/**
 * �����ڵ�(UCS2-LE) ���ڿ��� cp949 ���ڿ��� ����.
 * @param	wstr	��ȯ�� UCS2 ���ڿ�. �ݵ�� 0x0000���� ������ �Ѵ�.
 * @return	���������� ��ȯ�Ȱ�� cp949�� �����͸� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
char* snf_ucs_ucs2cp949(__ucs2 *wstr);
/**
* @brief MS-CP949 ���ڿ� �����͸� �Է� �޾� ucs2 ���ڿ� �����͸� ��ȯ
*
* MS-CP949 ���ڿ��� ucs2 ���ڿ��� ��ȯ�Ѵ�.
* ��ȯ ���� �����ʹ� �ݵ�� sn3utl_free() �� �̿��� �����ؾ� �Ѵ�.
*
* @param pUtf8 �Է� utf8 ���ڿ�.
* @see sn3utf8_to_ucs2(), sn3utf8_to_ucs2_loop(), sn3utl_free()
* @return ucs2 ���ڿ� ������
*/
__ucs2* snf_cp949_to_ucs2_str(__uint8 *pCp949);
/**
* ��ȯ��Ų �����ڵ� ���ڿ��� �޸� �����Ѵ�.
* @param	pMem  �޸� ������ �����ڵ� ���ڿ�
*/
void snf_utl_free(void *pMem);
/**
 * UCS2-LE ���ڿ��� ���̸� ��ȯ�Ѵ�.
 * @param	string	�����ڵ� ���ڿ��� ������
 * @return	�Էµ� �����ڵ� ���ڿ��� ���̸� ��ȯ.
 */
size_t snf_ucs_wcslen(__ucs2 *string );
/**
* �����ڵ� ���ڿ��� ���ڵ��Ѵ�.
* @param wstr �Է� UTF-8
* @param encoding ���ڵ� ����
* @return ���ڵ��� ����� ucs2 ���ڿ��� ��ȯ
*/
__uint8* snf_ucs_decode_str(__ucs2 *wstr, int encoding);
/**
* ucs2 ���ڿ��� ������ utf8 ���ڿ� �����ͷ� ��ȯ�Ѵ�.
* @param wstr �Է�
* @param wlen �Է� ����
* @param dest ����� utf ���ڿ�
* @param dlen ��� ����
* @param encoding ���ڵ� ����
* @return ����: SN3OK, ����: ERROR_UTF8_FROM_UCS2_LOOP_FULL_OUTPUT
*/
int snf_ucs_decode(__ucs2 *wstr, int wlen, __uint8* dest, int dlen, int encoding);

/**
* @brief utf8 ���ڿ� �����͸� �Է� �޾� ucs2 ���ڿ� �����͸� ��ȯ
*
* utf8 ���ڿ��� ucs2 ���ڿ��� ��ȯ�Ѵ�.
* ��ȯ ���� �����ʹ� �ݵ�� sn3utl_free() �� �̿��� �����ؾ� �Ѵ�.
*
* @param pUtf8 �Է� utf8 ���ڿ�.
* @see sn3utf8_to_ucs2(), sn3utf8_to_ucs2_loop(), sn3utl_free()
* @return ucs2 ���ڿ� ������
*/
__ucs2* snf_utf8_to_ucs2_str(__uint8 *pUtf8);

// SN3MFI ///////////////////////////////////////////////////////
// mfi open&close
/**
 * SN3MFI ��ü�� ����(�޸��Ҵ�)�ϰ� Default ������ �ʱ�ȭ �Ѵ�.
 * @param	ppMFI	SN3MFI �������� ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_mfi_fopen_rw(SN3MFI **ppMFI);
/**
 * SN3MFI ��ü�� ����(�޸��Ҵ�)�ϰ� �޸� ������ �������� �ʱ�ȭ �Ѵ�.
 * @param	pMemFile �޸� ���� ������
 * @param pMemSize �޸� ������ ũ��
 * @param ppMFI SN3MFI �������� ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_mfi_fopen_m(__uint8 *pMemFile, __int64 pMemSize, SN3MFI **ppMFI);
/**
 * SN3MFI �޸� ������ ������ �������� �����޾� MFI�� �ʱ�ȭ �Ѵ�.
 * @param	pMemFile malloc���� �Ҵ���� �޸� ���� ������
 * @param pMemSize �޸� ������ ũ��
 * @param ppMFI SN3MFI �������� ������
 * @return	���������� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_mfi_fopen_move_m(__uint8 *pMemFile, __int64 pMemSize, SN3MFI **ppMFI);
/**
 * SN3MFI ��ü�� ����(�޸��Ҵ�)�ϰ� ������ �������� �ʱ�ȭ �Ѵ�.
 * @param	pFilePath ���ϸ�
 * @param ppMFI SN3MFI �������� ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_mfi_fopen(__uint8 *pFilePath, SN3MFI **ppMFI);
/**
 * SN3MFI ��ü�� ����(�޸��Ҵ�)�ϰ� ������ �������� �ʱ�ȭ �Ѵ�.
 * @param	pFilePath ��Ƽ����Ʈ ���ϸ�
 * @param ppMFI SN3MFI �������� ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_mfi_wfopen(__ucs2 *pFilePath, SN3MFI **ppMFI);
/**
 * SN3MFI ��ü�� �ı�(�޸𸮹�ȯ)�Ѵ�.
 * @param pMFI SN3MFI ������
 * @return	���������� �޸𸮰� ��ȯ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_mfi_fclose(SN3MFI *pMFI);

// mfi misc
/**
 * SN3MFI ��ü�� ���� ���� �������� ó������ ������.
 * @param pMFI SN3MFI ������
 */
void snf_mfi_rewind(SN3MFI *pMFI);
/**
 * SN3MFI ��ü�� ���� �������� ���� �÷��׿� ���� Ư�� ��ġ�� �����Ѵ�.
 * ������ ���� �÷��״� SN3MFI_SEEK_SET, SN3MFI_SEEK_CUR, SN3MFI_SEEK_END
 * �� �ϳ����� �Ѵ�.
 * @param pMFI SN3MFI ������
 * @param pOffset �� ������
 * @param pOrigin ������ ���� �÷���
 * @return	pMFI�� ���� �������� ����� ������ �� �ִٸ� SN3OK��
 *					�ƴϸ� �ش� ������ ��ȯ.
 */
__int64 snf_mfi_fseek(SN3MFI *pMFI, __int64 pOffset, int pOrigin);
/**
 * SN3MFI ��ü�� ���� ũ�⸦ �����Ѵ�.
 * @param pMFI SN3MFI ������
 * @return	pMFI�� ���� ũ�� ��ȯ.
 */
size_t snf_mfi_fsize(SN3MFI *pMFI);
/**
 * SN3MFI ��ü�� ���� �������� �����Ѵ�.
 * @param pMFI SN3MFI ������
 * @return	pMFI�� ���� ������.
 */
__int64 snf_mfi_ftell(SN3MFI *pMFI);
/**
 * SN3MFI ��ü�� ���� �������� �������� �����ߴ��� �˻��Ѵ�.
 * @param pMFI SN3MFI ������
 * @return	pMFI�� ���� �������� �������� ���������� 1��
 *					�ƴϸ� 0�� ��ȯ.
 */
int snf_mfi_feof(SN3MFI *pMFI);
/**
 * SN3MFI ��ü�� ���� ���� �����Ǻ��� ������ Ư�� ���Ͽ� ����Ѵ�.
 * @param pMFI SN3MFI ������
 * @param pFilePath ��� ��� ���ϸ�
 * @return	���� ������ �ش� ������
 *					�ƴϸ� SN3OK�� ��ȯ.
 */
int snf_mfi_unload(SN3MFI *pMFI, __uint8 *pFilePath);

// mfi read
/**
* SN3MFI ��ü�� ���� ���� �������� ������ �а�
* ���� �������� 1 ������Ų��.
* @param pMFI SN3MFI ������
* @return	���� �������� ������ ���̶�� EOF��
* �ƴϸ� ���� ������ ��ȯ.
*/
int snf_mfi_fgetc(SN3MFI *pMFI);
/**
 * SN3MFI ��ü�� ���� ���� �������� �ٷ� ���� ������ �а�
 * ���� �������� 1 ���ҽ�Ų��.
 * @param pMFI SN3MFI ������
 * @param ch ���Ϲ��� ��
 * @return	���� �������� ó���̶�� EOF��
 *					�ƴϸ� ch�� ��ȯ.
 */
int snf_mfi_fungetc(SN3MFI *pMFI, int ch);
/**
 * SN3MFI ��ü�� ���� ���� �����Ǻ��� pSize*pCount ��ŭ�� ������
 * ���ۿ� ����� �� ���� ����Ʈ �� ��ŭ ���� �������� 1 ������Ų��.
 * ���� ����Ʈ���� ������ ���� �����ǿ��� ������������ ����Ʈ������ ũ��
 * ���� ����Ʈ���� �������Ѵ�.
 * @param pMFI SN3MFI ������
 * @param pBuffer __uint8�� ���� ���� ������
 * @param pSize pBuffer�� ����Ÿ�� ũ��
 * @param pCount ���� ����
 * @return	���� �о���� ������ ��ȯ.
 */
__int64 snf_mfi_fread(SN3MFI *pMFI, __uint8 *pBuffer, size_t pSize, size_t pCount);

// mfi write
/**
 * SN3MFI ��ü�� ���� ���� �����ǿ� ���� ����ϰ� �������� 1 ������Ų��.
 * SN3MFI ��ü�� pFile�� NULL�̸�
 * SN3MFI_REALLOC_SIZE ��ŭ�� �޸𸮸� ���� �Ҵ��ϰ�,
 * ��� ���� �������� Limit�� ������
 * SN3MFI_REALLOC_SIZE ��ŭ�� �޸𸮸� �߰��� �Ҵ��Ѵ�.
 * @param pMFI SN3MFI ������
 * @param ch ����� ������
 * @return	�޸� ������ ���� EOF��
 *					����� ��ϵǾ����� ch�� ��ȯ.
 */
int snf_mfi_fputc(SN3MFI *pMFI, int ch);
/**
 * SN3MFI ��ü�� ���� ���� �����Ǻ��� �Է¹��� ������ ������ ����Ѵ�.
 * SN3MFI ��ü�� pFile�� NULL�̸�
 * �ʿ��� ��ŭ�� �޸𸮸� ���� �Ҵ��ϰ�,
 * ��� ���� �������� Limit�� ������
 * �ʿ��� ��ŭ�� �޸𸮸� �߰��� �Ҵ��Ѵ�.
 * ����� ���� ����Ʈ�� ��ŭ ���� �������� ������Ų��.
 * @param pMFI SN3MFI ������
 * @param pBuffer ���Ͽ� ����� ����
 * @param pSize pBuffer�� ����Ÿ�� ũ��
 * @param pCount ����� ����
 * @return	�޸� ������ ���� 0��
 *					��ϵǾ����� ����� ������ ��ȯ.
 */
size_t snf_mfi_fwrite(SN3MFI *pMFI, __uint8 *pBuffer, size_t pSize, size_t pCount);


// SN3BUF //////////////////////////////////////////////////////
// Buffer init & free
/**
 * UCS2-LE ���۸� �ʱ�ȭ �Ѵ�.
 * @param	pBuf	���� �������� ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_buf_init(SN3BUF **pBuf);
/**
 * UCS2-LE ������ �޸𸮸� ��ȯ�Ѵ�.
 * @param	pBuf	������ ������
 * @return	���������� �޸𸮸� ��ȯ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_buf_free(SN3BUF *pBuf);

// Buffer misc
/**
 * ���۰� ����ִ��� Ȯ���Ѵ�.
 * @param	pBuf	������ ������
 * @return	����ִٸ� 1
 *          ������� �ʴٸ� 0 �� ��ȯ
 */
int snf_buf_isempty(SN3BUF *pBuf);
/**
 * UCS2-LE ������ ũ�⸦ ��ȯ�Ѵ�.
 * @param	pBuf	������ ������
 * @return	������ ũ�⸦ ��ȯ.
 */
size_t snf_buf_size(SN3BUF *pBuf);
/**
* ������ UTF8 ���̸� �����´�.
* @param  pBuf	������ ������
* @return ������ UTF8 ����(size_t)�� ��ȯ.
*/
size_t snf_buf_get_utf8_len( const SN3BUF *pBuf );
/**
* ���۸� ����.
* @param  pBuf  ������ ������
* @return ���۸� ��� �� SN3OK ��ȯ
*/
int snf_buf_clear(SN3BUF *pBuf);
/**
* ù��° �Ű����� ���� �ڿ� �ι�° �Ű����� ���۸� ���δ�.
* @param  pBuf  ������ ������
* @param  pBufAdd  ������ ������ ������
* @return ���������� ���۰� ���ٿ����ٸ� SN3OK��ȯ.
*		  ������ �ִ� ��쿡�� �ش� �����ڵ� ��ȯ.
*/
int snf_buf_append(SN3BUF *pBuf, SN3BUF *pBufAdd);

// Buffer Unloading
/**
 * UCS2-LE ������ ������ ������ encoding ���·� MFI�� ����Ѵ�.
 * @param	pBuf	������ ������
 * @param	pMFI	MFI�� ������
 * @param	pEncoding	Endocding Ÿ��
 * @return	���������� �޸𸮸� ��ȯ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_buf_unload_m(SN3BUF *pBuf, SN3MFI *pMFI, __int32 pEncoding);
/**
 * UCS2-LE ������ ������ ������ encoding ���·�
 * ��������� �������Ͽ� ����Ѵ�.
 * @param	pBuf	������ ������
 * @param	pFilePath   ��� ���ϰ��
 * @param	pEncoding	Encoding Ÿ��
 * @return	���������� �޸𸮸� ��ȯ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_buf_unload(SN3BUF *pBuf, __uint8 *pFilePath, __int32 pEncoding);
/**
 * UCS2-LE ������ ������ ������ encoding ���·�
 * ��������� �������Ͽ� ����Ѵ�.
 * @param	pBuf	������ ������
 * @param	pFilePath   ��� ���ϰ�� (�����ڵ� ���)
 * @param	pEncoding	Encoding Ÿ��
 * @return	���������� �޸𸮸� ��ȯ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_buf_wunload(SN3BUF *pBuf, __ucs2 *pFilePath, __int32 pEncoding);

// Buffer Put (UCS2 Version)
/**
 * UCS2-LE ���ڸ� ���ۿ� �ִ´�. ���ۿ��� �׻� ��������
 * �����ڵ� ���ڰ� LE ���·� �־���Ѵ�. SN3NOCHAR��
 * SN3NULL � �� �� ����. ����ũ�Ⱑ �����ϸ� ���۸� �ø���.
 * @param	pBuf	������ ������
 * @param	ch		UCS2 ����
 * @return	���������� �Էµ� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_buf_putc_ucs2_raw(SN3BUF *pBuf, __ucs2 ch);
/**
 * UCS2-LE ���ڸ� ���ۿ� �ִ´�. ���ۿ��� �׻� ��������
 * �����ڵ� ���ڰ� LE ���·� �־���Ѵ�. SN3NOCHAR��
 * SN3NULL � �� �� ����. ����ũ�Ⱑ �����ϸ� ���۸� �ø���.
 * @param	pBuf	������ ������
 * @param	ch		UCS2 ����
 * @return	���������� �Էµ� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_buf_putc_ucs2(SN3BUF *pBuf, __ucs2 ch);
/**
 * UCS2-LE ���ڿ��� ���ۿ� �ִ´�. UCS2-LE ���ڿ��� ����
 * SN3NULL�� �� �־���ϸ�, ���ۿ� SN3NULL�� ���� �ʴ´�.
 * ���ڿ� �߿� SN3NOCHAR ���� ������ �����ϰ� �����Ѵ�.
 * @param	pBuf	������ ������
 * @param	str		UCS2 ���ڿ�
 * @return	���������� �Էµ� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_buf_puts_ucs2(SN3BUF *pBuf, __ucs2 *str);
/**
 * UCS2-BE ���ڿ��� ���ۿ� �ִ´�. UCS2-BE ���ڿ��� ����
 * SN3NULL�� �� �־���ϸ�, ���ۿ� SN3NULL�� ���� �ʴ´�.
 * ���ڿ� �߿� SN3NOCHAR ���� ������ �����ϰ� �����Ѵ�.
 * @param	pBuf	������ ������
 * @param	str		UCS2 ���ڿ�
 * @return	���������� �Էµ� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_buf_puts_ucs2_be(SN3BUF *pBuf, __ucs2 *str);
/**
 * ���ۿ� newline ���ڸ� �Է�.
 * @param	pBuf	�����ڵ� ������ ������
 * @return	���������� �ԷµȰ�� SN3OK ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_buf_put_newline(SN3BUF *pBuf);
/**
 * ���ۿ� ���� ���ڸ� �Է�.
 * @param	pBuf	�����ڵ� ������ ������
 * @return	���������� �ԷµȰ�� SN3OK ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_buf_put_space(SN3BUF *pBuf);

// Buffer Peek & Get (UCS2 Version)
/**
 * ���ۿ� ���� ó���� �Էµ� ���ڸ� Ȯ���Ѵ�.
 * @param	pBuf	�����ڵ� ������ ������
 * @return	���������� ����Ǿ��ٸ�
 *          ù��° ����(__ucs2)�� ��ȯ.
 *          ���۰� ����ִٸ� SN3NOCHAR ��ȯ.
 */
__ucs2 snf_buf_peekstart(SN3BUF *pBuf);
/**
 * ���ۿ� ���� �������� �Էµ� ���ڸ� Ȯ���Ѵ�.
 * @param	pBuf	�����ڵ� ������ ������
 * @return	���������� ����Ǿ��ٸ�
 *          ����������(__ucs2)�� ��ȯ.
 *          ���۰� ����ִٸ� SN3NOCHAR ��ȯ.
 */
__ucs2 snf_buf_peekend(SN3BUF *pBuf);
/**
 * ������ ���� �տ� �ִ� UCS2-LE ���ڸ� �о�´�.
 * @param	pBuf	�����ڵ� ������ ������
 * @return	���ۿ��� �о �����ڵ带 ��ȯ
 *          ���ۿ� ������� SN3NOCHAR�� ��ȯ
 */
__ucs2 snf_buf_getwch(SN3BUF *pBuf);
/**
 * ������ ���ʿ� UCS2-LE ���ڸ� �ִ´�.
 * @param	pBuf	�����ڵ� ������ ������
 * @param	ch		���� �����ڵ� ����
 * @return	������ ������ SN3OK,
 *          ������ ������ ��á���� �����ڵ带 ��ȯ
 */
int snf_buf_ungetwch(SN3BUF *pBuf, __ucs2 ch);
/**
 * ���ۿ��� UCS2-LE ���ڿ��� �о�´�.
 * @param	pBuf	�����ڵ� ������ ������
 * @param	buf		�޾ƿ� ������ ������
 * @param	buf_size	�޾ƿ� ������ ũ��
 * @return	�о ä�� �����ڵ� ����(size_t)�� ��ȯ
 *          ������ �ִٸ� 0�� ��ȯ.
 */
size_t snf_buf_get_ucs2(SN3BUF *pBuf, __ucs2 *buf, int buf_size);

// Buffer Put & Get (CP949 Version)
/**
 * MS-CP949 ���ڸ� ���ۿ� �ִ´�.
 * @param	pBuf	������ ������
 * @param	ch		MS-CP949 ����
 * @return	���������� �Էµ� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_buf_putc_cp949(SN3BUF *pBuf, __uint16 ch);
/**
 * MS-CP949 ���ڿ��� ���ۿ� �ִ´�. ���ڿ��� �� NULL�� �������Ѵ�.
 * @param	pBuf	������ ������
 * @param	str		MS-CP949 ���ڿ�
 * @return	���������� �Էµ� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_buf_puts_cp949(SN3BUF *pBuf, __uint8 *str);
/**
 * ���ۿ��� MS-CP949 ���ڿ��� �о�´�.
 * @param	pBuf	�����ڵ� ������ ������
 * @param	buf		�޾ƿ� ������ ������
 * @param	buf_size	�޾ƿ� ������ ũ��
 * @return	�о ä�� ����Ʈ��(size_t)�� ��ȯ
 *          ������ �ְų� ���̻� �����ð� ������ 0�� ��ȯ.
 */
size_t snf_buf_get_cp949(SN3BUF *pBuf, __uint8 *buf, int buf_size);

// Buffer position
/**
 * ������ �������� ���� �Ѵ�.
 * pos �� 0 ���� ���� ��� ���������� ä���� ������ ū���� ���������� �̵�.
 * @param	pBuf	�����ڵ� ������ ������
 * @param	pos		������ ������ ������
 * @return
 */
void snf_buf_setpos(SN3BUF *pBuf, size_t pos);
/**
 * ������ �������� ���������� �Ű��ش�.
 * @param	pBuf	�����ڵ� ������ ������
 * @return  ���۰� ����ִٸ� 0, ������� �ʴٸ� ������ �������� ��ȯ.
 */
size_t snf_buf_getpos(SN3BUF *pBuf);
/**
 * ������ �������� ���������� �Ű��ش�.
 * @param	pBuf	�����ڵ� ������ ������
 */
void snf_buf_rewind(SN3BUF *pBuf);

// Text getter
/**
 * ���ۿ��� ������ ���ڵ����� ���ڿ��� �о�´�.
 * @param	pBuf	�����ڵ� ������ ������
 * @param	buf		�޾ƿ� ������ ������
 * @param	buf_size	�޾ƿ� ������ ũ��
 * @param	encoding	������ ���ڵ�
 * @return	�о ä�� ����Ʈ��(size_t)�� ��ȯ
 *          ������ �ְų� ���̻� �����ð� ������ 0�� ��ȯ.
 */
size_t snf_buf_get_text(SN3BUF *pBuf, __uint8 *buf, int buf_size, int encoding);
/**
 * ���ۿ��� ������ ���ڵ����� ���ڿ��� �о�´�.
 * @param	pBuf	�����ڵ� ������ ������
 * @param	buf		�޾ƿ� ������ ������
 * @param	buf_size	�޾ƿ� ������ ũ��
 * @param	encoding	������ ���ڵ�
 * @return	�о ä�� ����Ʈ��(size_t)�� ��ȯ
 *          ������ �ְų� ���̻� �����ð� ������ 0�� ��ȯ.
 */
size_t snf_buf_get_text_le(SN3BUF *pBuf, __uint8 *buf, int buf_size, int encoding);


// SN3SUM //////////////////////////////////////////////////////
/**
 * SN3SUM ��ü�� �ʱ�ȭ�Ѵ�.
 * @param	ppSum SN3SUM �������� ������
 * @return	����� �޸𸮸� �Ҵ��ϸ� SN3OK�� ��ȯ�ϰ�
 *					������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_sum_init(SN3SUM **ppSum);
/**
 * SN3SUM ��ü�� �޸𸮸� �����Ѵ�.
 * @param	pSum SN3SUM ������
 * @return	����� �޸𸮸� �����ϸ� SN3OK�� ��ȯ�ϰ�
 *					������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_sum_free(SN3SUM *pSum);
/**
 * SN3SUM�� ������ ȭ�鿡 ����Ѵ�.
 * @param	pSum SN3SUM ������
 * @return	SN3OK�� ��ȯ�Ѵ�.
 */
int snf_sum_show(SN3SUM *pSum);

// Summary Unloading ...
/**
 * SN3SUM�� ������ SN3MFI�� ���ڵ� ��Ŀ� �°� �����Ѵ�.
 * @param	pSum SN3SUM ������
 * @param	pMFI SN3MFI ������
 * @param	pEncoding ���ڵ� ���
 * @return	SN3SUM ������ ���������� ����Ǹ� SN3OK��,
 *				  ������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_sum_unload_m(SN3SUM *pSum, SN3MFI *pMFI, __int32 pEncoding);
/**
 * SN3SUM�� ������ FILE�� ���ڵ� ��Ŀ� �°� �����Ѵ�.
 * @param	pSum SN3SUM ������
 * @param	pFile FILE ������
 * @param	pEncoding ���ڵ� ���
 * @return	���Ͽ� ����� ���������� SN3OK�� ��ȯ�ϰ�
 *					������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_sum_unload_f(SN3SUM *pSum, FILE *pFile, __int32 pEncoding);
/**
 * SN3SUM�� ������ ���Ͽ� ���ڵ� ��Ŀ� �°� �����Ѵ�.
 * @param	pSum SN3SUM ������
 * @param	pFilePath ���ϸ�
 * @param	pEncoding ���ڵ� ���
 * @return	���Ͽ� ����� ���������� SN3OK�� ��ȯ�ϰ�
 *					������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_sum_unload(SN3SUM *pSum, __uint8 *pFilePath, __int32 pEncoding);
/**
 * SN3SUM�� ������ ���Ͽ� ���ڵ� ��Ŀ� �°� �����Ѵ�.
 * @param	pSum SN3SUM ������
 * @param	pFilePath ���ϸ�
 * @param	pEncoding ���ڵ� ���
 * @return	���Ͽ� ����� ���������� SN3OK�� ��ȯ�ϰ�
 *					������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_sum_wunload(SN3SUM *pSum, __ucs2 *pFilePath, __int32 pEncoding);

// Docinfo
/**
* ������ ��������� ����Ѵ�.
* @param  pFilePath ���ϸ�
* @param  pSum	SN3SUM ������
* @return ��������� ���������� ��µǸ� SN3OK�� ��ȯ�ǰ�
*			���߿� ������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_flt_docinfo(__uint8 *pFilePath, SN3SUM *pSum);
/**
* �����ڵ� ����� ������ ��������� ����Ѵ�.
* @param  pFilePath ���ϸ�
* @param  pSum	SN3SUM ������
* @return ��������� ���������� ��µǸ� SN3OK�� ��ȯ�ǰ�
*			���߿� ������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_flt_wdocinfo(__ucs2 *pFilePath, SN3SUM *pSum);
/**
* �޸𸮿� �ִ� ������ ��������� ����Ѵ�.
* @param  pMFI SN3MFI ������
* @param  pSum	SN3SUM ������
* @return ��������� ���������� ��µǸ� SN3OK�� ��ȯ�ǰ�
*			���߿� ������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_flt_docinfo_m(SN3MFI *pMFI, SN3SUM *pSum);
/**
 * Ư�� ������ DocumentSummaryInformation�� SN3BUF�� �����Ѵ�.
 * @param	pFilePath ���ϸ�
 * @param	pBuf SN3BUF�� ������
 * @return	SummaryInformation�� ������ ����� SN3BUF�� �����ϸ� SN3OK�� ��ȯ�ϰ�
 *			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_flt_docinfoEx(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * Ư�� ������ DocumentSummaryInformation�� SN3BUF�� �����Ѵ�.
 * @param	pFilePath ���ϸ�
 * @param	pBuf SN3BUF�� ������
 * @return	SummaryInformation�� ������ ����� SN3BUF�� �����ϸ� SN3OK�� ��ȯ�ϰ�
 *			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_flt_wdocinfoEx(__ucs2 *pFilePath, SN3BUF *pBuf);
/**
 * �޸𸮿� ��� ������ DocumentSummaryInformation�� SN3BUF�� �����Ѵ�.
 * @param	pMFI SN3MFI ������
 * @param	pBuf SN3BUF�� ������
 * @return	SummaryInformation�� ������ ����� SN3BUF�� �����ϸ� SN3OK�� ��ȯ�ϰ�
 *			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_flt_docinfoEx_m(SN3MFI *pMFI, SN3BUF *pBuf);

// Filter (FilePath) ///////////////////////////////////////////
/**
 * ���� ���͸� �� ��� �ؽ�Ʈ�� ���ۿ� ����Ѵ�.
 * @param	pFilePath	��� ���� ���
 * @param   pBuf  ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param   WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����: SN3OK, ����: �ش� �����ڵ�
 */
int snf_flt_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
* ���� ���͸� �� ��� �ؽ�Ʈ�� ���Ͽ� ����Ѵ�. (len�� wcslen()���� ����)
* @param pFilePath �Է����� ���
* @param pOutPath ������� ���. NULL�� ��� stdout�� ���
* @param WithPage ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
* @param encoding ��� �ؽ�Ʈ ���ڵ�
* @return ����: SN3OK, ����: �ش� �����ڵ�
*/
int snf_flt_filter_ex(__uint8 *pFilePath, __uint8 *pOutPath, int WithPage, int encoding);
/**
 * ���� ���͸� �� ��� �ؽ�Ʈ�� ���ۿ� ����Ѵ�.
 * @param	pFilePath	��� ���� ���
 * @param   pBuf  ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param   WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����: SN3OK, ����: �ش� �����ڵ�
 */
int snf_flt_wfilter(__ucs2 *pFilePath, SN3BUF *pBuf, int WithPage);

/**
 * alz ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	alz ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage	 ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_alz_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * bzip ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	bzip ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_bzip_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * chm ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	chm ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_chm_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * doc ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	doc ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_doc_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * docx ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	docx ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_docx_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * dwg ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	dwg ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_dwg_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * GZ(GNU Zip) ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	GZ ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_gz_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * h2k ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	h2k ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_h2k_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * htm / html ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	htm / html ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_htm_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwn ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	hwn ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_hwn_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwd ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	hwd ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_hwd_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwp3 ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	hwp3 ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_hwp3_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwx ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	hwx ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_hwx_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * jtd ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	jtd ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_jtd_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * mdb ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	mdb ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_mdb_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * mdi ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	mdi ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_mdi_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * mht ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	mht ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_mht_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * mp3 ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	mp3 ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_mp3_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * msg ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	msg ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_msg_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * pdf ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	pdf ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_pdf_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * ppt ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	ppt ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_ppt_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * pptx ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	pptx ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_pptx_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * ppam ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	ppam ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_ppam_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * thmx ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	thmx ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_thmx_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * rtf ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	rtf ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_rtf_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * 7zip ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	7zip ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_sevenzip_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * swf ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	swf ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_swf_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * sxx ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	sxx ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_sxx_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * tar ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	tar ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_tar_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * txt ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	txt ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_txt_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * vtt ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	vtt ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_vtt_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * wpd ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	wpd ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_wpd_filter( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xls ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	xls ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_xls_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xlsx ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	xlsx ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_xlsx_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwp ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	hwp ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_xml_hwp_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xml office ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	xml office ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_xml_office_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * zip ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	zip ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_zip_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * rar ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	rar ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_rar_filter( __uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * ndoc ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	ndoc ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_ndoc_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * KEYNOTE ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath Keynote ���� ���
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK�� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_keynote_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * PAGES ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath pages ���� ���
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK�� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_pages_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * NUMBERS ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath numbers ���� ���
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK�� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_numbers_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * pst ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	pst ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_pst_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwpx ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	hwpx ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_hwpx_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * �ؼ�(nxl) ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	nxl ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_nxl_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * ���� ���� ����(cell)�� ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	cell ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_cell_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * �Ѽ�(show) ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	show ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_show_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xps ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	xps ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_xps_filter(__uint8 *pFilePath, SN3BUF *pBuf);

/**
 * keynote'13 ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	keynote'13 ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_keynote13_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * pages13 ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	pages13 ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_pages13_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * numbers13 ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	numbers13 ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_numbers13_filter(__uint8 *pFilePath, SN3BUF *pBuf);

/**
 * keynote14 ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	keynote14 ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_keynote14_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * pages14 ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	pages14 ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_pages14_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * numbers14 ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	numbers14 ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_numbers14_filter(__uint8 *pFilePath, SN3BUF *pBuf);

/**
 * xlsb ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	xlsb ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_xlsb_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * DICOM ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	DICOM ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_dicom_filter(__uint8 *pFilePath, SN3BUF *pBuf);

/**
 * nsf ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	nsf ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_nsf_filter(__uint8* pFilePath, SN3BUF* pBuf);
/**
 * edb ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	edb ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_edb_filter(__uint8* pFilePath, SN3BUF* pBuf);

// Filter (MFI) ////////////////////////////////////////////////
/**
 * �޸𸮿� ��� ���� ���� ���͸� �� ���˿� �°� ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI �ҽ� ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_flt_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);

/**
 * alz ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI alz ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_alz_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * bzip ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI bzip ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_bzip_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * chm ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI chm ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_chm_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * doc ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI doc ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_doc_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * docx ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI docx ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_docx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * dwg ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI dwg ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_dwg_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * GZ ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI GZ ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_gz_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * h2k ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI h2k ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_h2k_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * htm ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI htm ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_htm_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * hwn ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI hwm ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_hwn_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * hwd ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI hwd ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_hwd_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * hwp3 ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI hwp3 ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_hwp3_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * hwx ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI hwx ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_hwx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * jtd ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI jtd ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_jtd_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * mdb ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI mdb ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_mdb_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * mdi ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI mdi ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_mdi_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * mht ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI mht ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_mht_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * mp3 ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI mp3 ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_mp3_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * msg ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI msg ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_msg_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * pdf ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI pdf ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_pdf_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * ppt ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI ppt ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_ppt_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * pptx ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI pptx ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_pptx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * rtf ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI rtf ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_rtf_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * 7zip ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI 7zip ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_sevenzip_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * swf ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI swf ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_swf_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * sxx ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI sxx ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_sxx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * tar ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI tar ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage ������ ������ ��� ����.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_tar_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * txt ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI txt ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_txt_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * vtt ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI vtt ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_vtt_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * wpd ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI wpd ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_wpd_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xls ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI xls ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_xls_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xlsx ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI xlsx ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_xlsx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf );
/**
 * hwp ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI hwp ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_xml_hwp_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xml office ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI xml office ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_xml_office_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * zip ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI zip ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_zip_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * rar ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI rar ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_rar_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * ndoc ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI ndoc ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_ndoc_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * egg ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI egg ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_egg_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * KEYNOTE ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI keynote ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_keynote_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * PAGES ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI pages ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_pages_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * NUMBERS ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI numbers ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_numbers_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * pst ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI pst ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_pst_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
* pst ���� ������ void�� ���� �����Ϳ� ����Ѵ�. wsnf_pst_email_close()�� ������ ����� �޸� ������ ���ƾ� �Ѵ�.
* @param	pMFI pst������ ��� �޸� ������
* @param	ctx ���� ������ ��� void�� ���� ������
* @return	����� ���͸��ϸ� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_pst_email_open(SN3MFI *pMFI, void **ctx);
/**
* void�� �����Ϳ� ��� �̸��� ��� ������ ��ȯ�Ѵ�.
* @param	ctx �̸��� ������ ��� ���� ������
* @return	�Ű������� ����Ű�� �������� �̸��� ��� ������ ��ȯ�Ѵ�.
*/
int snf_pst_email_count(void *ctx);
/**
* �޸𸮿� ��� �ƿ��� ���� ������ ���ۿ� ���͸��Ѵ�.
* @param	pMFI pst ������ ��� �޸� ������
* @param	pBuf ������ ���� ���� ������
* @param	ctx  �̸��� ������ ��� ���� ������
* @param	idx	���ۿ� ���� �̸��� �ε���
* @return	���ۿ� ���������� ���͸� �� SN3OK��, ������ �ִ� ��� �ش� �����ڵ� ��ȯ�Ѵ�.
*/
int snf_pst_filter_email_m(SN3MFI *pMFI, SN3BUF *pBuf, void *ctx, int idx);
/**
* wsnf_pst_email_close()���� �������� ������� SN3PST_API_CONTEXT ��ü�� �����Ѵ�.
* @param	ctx �̸��� ������ ��� ���� ������
*/
void snf_pst_email_close(void *ctx);

/**
 * hwpx ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI hwpx ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_hwpx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * nxl ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI nxl ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_nxl_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * �Ѽ�(cell) ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI cell ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_cell_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * �Ѽ�(show) ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI show ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_show_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xps ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI xps ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_xps_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);

/**
 * xlsb ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI xlsb ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_xlsb_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);

/**
 * keynote14 ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI keynote14 ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_keynote14_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * pages14 ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI pages14 ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_pages14_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * numbers14 ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI numbers14 ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_numbers14_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);

/**
 * DICOM ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI DICOM ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_dicom_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);

/**
 * nsf ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI nsf ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_nsf_filter_m(SN3MFI* pMFI, SN3BUF* pBuf);
/**
 * edb ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI edb ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_edb_filter_m(SN3MFI* pMFI, SN3BUF* pBuf);

// Filter (MFI) with Format Code ///////////////////////////////
/**
 * �޸𸮿��� ���ڷ� ������ ��ȣ�� �ش��ϴ� ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @param	FileFormat ���� ���� �ش� ��ȣ
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_flt_filter_c( SN3MFI *pMFI, SN3BUF *pBuf, int WithPage, int FileFormat);
/**
 * �޸𸮿��� ���ڷ� ������ ���ڵ����� txt ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	FileFormat ���ڵ� ��ȣ
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int snf_txt_filter_c( SN3MFI *pMFI, SN3BUF *pBuf, int FileFormat);


// File(sheet,table) list (FilePath) ///////////////////////////
/**
 * alz������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pFilePath	alz ���� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_alz_filelist( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * GZ������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pFilePath	gz ���� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_gz_filelist(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * mdb������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pFilePath	mdb ���� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_mdb_filelist( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * 7zip������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pFilePath	7zip ���� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_sevenzip_filelist( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * tar������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pFilePath	tar ���� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_tar_filelist(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xls������ ��Ʈ ����� ����Ѵ�.
 *
 * @param	pFilePath	xls ���� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_xls_sheetlist ( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xlsx������ ��Ʈ ����� ����Ѵ�.
 *
 * @param	pFilePath	xlsx ���� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_xlsx_sheetlist ( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * zip������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pFilePath	zip ���� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_zip_filelist(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * rar������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pFilePath	rar ���� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_rar_filelist(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xlsb������ ��Ʈ ����� ����Ѵ�.
 *
 * @param	pFilePath	xlsb ���� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_xlsb_sheetlist(__uint8 *pFilePath, SN3BUF *pBuf);

// File(sheet,table) list (MFI) ////////////////////////////////
/**
 * alz������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	alz ������ ��� �޸� ������
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_alz_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * GZ������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	gz ������ ��� �޸� ������
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_gz_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * mdb������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	mdb ������ ��� �޸� ������
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_mdb_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * 7zip������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	7zip ������ ��� �޸� ������
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_sevenzip_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * tar������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	tar ������ ��� �޸� ������
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_tar_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xls������ ��Ʈ ����� ����Ѵ�.
 *
 * @param	pMFI	xls ������ ��� �޸� ������
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_xls_sheetlist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xlsx������ ��Ʈ ����� ����Ѵ�.
 *
 * @param	pMFI	xlsx ������ ��� �޸� ������
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_xlsx_sheetlist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * zip������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	zip ������ ��� �޸� ������
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_zip_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * rar������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	rar ������ ��� �޸� ������
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_rar_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xlsb������ ��Ʈ ����� ����Ѵ�.
 *
 * @param	pMFI	xlsb ������ ��� �޸� ������
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_xlsb_sheetlist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * egg������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	egg ������ ��� �޸� ������
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int snf_egg_filelist_m( SN3MFI *pMFI, SN3BUF *pBuf);
// File(sheet,table) raw list (MFI) ////////////////////////////////
/**
* ��ī�̺� ���� ����Ʈ(SN3ARFILIST)�� �Ű������� ���� �Ҵ��Ѵ�.
* @param	ppList	SN3ARFILIST�� ���� �Ҵ���� ���� ������
* @return	�Ű������� ���������� �޸𸮸� �Ҵ���� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
*/
int snf_arfilist_init(SN3ARFILIST** ppList);
/**
* ��ī�̺� ���� ����Ʈ(SN3ARFILIST)�� �Ű��������� �޸� �����Ѵ�.
* @param	ppList	�Ÿ� ������ SN3ARFILIST ������
*/
void snf_arfilist_free(SN3ARFILIST* pList);
/**
* ��ī�̺� ���� ����Ʈ(SN3ARFILIST)���� idx��° raw������ �̸��� ��ȯ�Ѵ�.
* @param	pList �̸��� ������ SN3ARFILIST ������
* @param	idx	������ ������ ���� ��� �� ��ġ (0-based)
* @return	SN3ARFLIST�� idx��° ������ �̸��� ucs2 ���ڿ��� ���ϵȴ�.���� �� �����ڵ� ��ȯ.
*/
__uint8* snf_arfilist_name(SN3ARFILIST* pList, int idx);
/**
* ��ī�̺� ���� ����Ʈ(SN3ARFILST)�� idx��° ��¿� ���� �̸��� ��ȯ�Ѵ�.
* pBuf�� ��¿� ���� �̸��� ���ٿ�����, �ʿ��ϸ� snf_buf_clear()�� ���۸� ������ �Ѵ�.
* @param	pList �̸��� ������ SN3ARFILIST ������
* @param	idx	������ ������ ���� ��� �� ��ġ (0-based)
* @param	pBuf ���� �̸��� ��� SN3BUF ������
* @return	���� �� SN3OK��, �����ϸ� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_arfilist_printname(SN3ARFILIST* pList, int idx, SN3BUF* pBuf);
/**
* SN3ARFILIST�� ���� �ִ� ���� ��� ������ ��ȯ�Ѵ�.
* @param	pList SN3ARFILIST ������
* @return	���� �� SN3OK��, �����ϸ� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_arfilist_count(SN3ARFILIST* pList);

/**
* alz ���� ���� ���� ����� ������ ����� ��´�.
* ���� ���� �� ��� ����� ������ ��θ� ������ SN3ARFILST�� �����Ѵ�.
* @param	pMFI ��� ������ SN3MFI ������
* @param	pList ���� ����� ��� SN3ARFILIST ������
* @return	�����ϸ� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_alz_filelistEx_m(SN3MFI* pMFI, SN3ARFILIST* pList);
/**
* 7zip ���� ���� ���� ����� ������ ����� ��´�.
* ���� ���� �� ��� ����� ������ ��θ� ������ SN3ARFILST�� �����Ѵ�.
* @param	pMFI ��� ������ SN3MFI ������
* @param	pList ���� ����� ��� SN3ARFILIST ������
* @return	�����ϸ� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_sevenzip_filelistEx_m(SN3MFI* pMFI, SN3ARFILIST* pList);
/**
* tar ���� ���� ���� ����� ������ ����� ��´�.
* ���� ���� �� ��� ����� ������ ��θ� ������ SN3ARFILST�� �����Ѵ�.
* @param	pMFI ��� ������ SN3MFI ������
* @param	pList ���� ����� ��� SN3ARFILIST ������
* @return	�����ϸ� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_tar_filelistEx_m(SN3MFI* pMFI, SN3ARFILIST* pList);
/**
* zip ���� ���� ���� ����� ������ ����� ��´�.
* ���� ���� �� ��� ����� ������ ��θ� ������ SN3ARFILST�� �����Ѵ�.
* @param	pMFI ��� ������ SN3MFI ������
* @param	pList ���� ����� ��� SN3ARFILIST ������
* @return	�����ϸ� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_zip_filelistEx_m(SN3MFI* pMFI, SN3ARFILIST* pList);
/**
* rar ���� ���� ���� ����� ������ ����� ��´�.
* ���� ���� �� ��� ����� ������ ��θ� ������ SN3ARFILST�� �����Ѵ�.
* @param	pMFI ��� ������ SN3MFI ������
* @param	pList ���� ����� ��� SN3ARFILIST ������
* @return	�����ϸ� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_rar_filelistEx_m(SN3MFI* pMFI, SN3ARFILIST* pList);
/**
* egg ���� ���� ���� ����� ������ ����� ��´�.
* ���� ���� �� ��� ����� ������ ��θ� ������ SN3ARFILST�� �����Ѵ�.
* @param	pMFI ��� ������ SN3MFI ������
* @param	pList ���� ����� ��� SN3ARFILIST ������
* @return	�����ϸ� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_egg_filelistEx_m(SN3MFI* pMFI, SN3ARFILIST* pList);

// Extract file from Archive ///////////////////////////////////
/**
* alz ���� ���� ���� ������ ���� ������ Ǯ�� SN3MFI�� ����.
* @param	pMFI ���� ������ ���� SN3MFI ������
* @param	pUzFile ���� ������ ������ ������ SN3MFI ������
* @param	pFileNm ���� ������ ������ ���
* @return	���� �� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_alz_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* 7zip ���� ���� ���� ������ ���� ������ Ǯ�� SN3MFI�� ����.
* @param	pMFI ���� ������ ���� SN3MFI ������
* @param	pUzFile ���� ������ ������ ������ SN3MFI ������
* @param	pFileNm ���� ������ ������ ���
* @return	���� �� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_sevenzip_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* tar ���� ���� ���� ������ ���� ������ Ǯ�� SN3MFI�� ����.
* @param	pMFI ���� ������ ���� SN3MFI ������
* @param	pUzFile ���� ������ ������ ������ SN3MFI ������
* @param	pFileNm ���� ������ ������ ���
* @return	���� �� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_tar_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* zip ���� ���� ���� ������ ���� ������ Ǯ�� SN3MFI�� ����.
* @param	pMFI ���� ������ ���� SN3MFI ������
* @param	pUzFile ���� ������ ������ ������ SN3MFI ������
* @param	pFileNm ���� ������ ������ ���
* @return	���� �� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_zip_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* rar ���� ���� ���� ������ ���� ������ Ǯ�� SN3MFI�� ����.
* @param	pMFI ���� ������ ���� SN3MFI ������
* @param	pUzFile ���� ������ ������ ������ SN3MFI ������
* @param	pFileNm ���� ������ ������ ���
* @return	���� �� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_rar_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* bzip ���� ���� ���� ������ ���� ������ Ǯ�� SN3MFI�� ����.
* @param	pMFI ���� ������ ���� SN3MFI ������
* @param	pUzFile ���� ������ ������ ������ SN3MFI ������
* @return	���� �� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_bzip_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile);
/**
* egg ���� ���� ���� ������ ���� ������ Ǯ�� SN3MFI�� ����.
* @param	pMFI ���� ������ ���� SN3MFI ������
* @param	pUzFile ���� ������ ������ ������ SN3MFI ������
* @return	���� �� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int snf_egg_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileName);

// User Callback Function Define ///////////////////////////////////
/**
 * ����� ���� �Լ��� �����Ѵ�.
 * @param pBuf			   ������ ������
 * @param snf_buf_user_func ����� ���� �Լ� ������
 */
void snf_buf_set_user_func( SN3BUF *pBuf, void(* sn3buf_user_func)(SN3BUF* pBuf, void* pUserData) );
/**
 * ����� ����� �����Ѵ�.
 *
 * @param pBuf				������ ������
 * @param snf_user_command	����� ���
 *
 */
void snf_buf_set_user_command(SN3BUF *pBuf, int sn3_user_command);
/**
 * ����� �����͸� �����Ѵ�.
 *
 * @param pBuf			������ ������
 * @param pUserData		����� ������ ������
 */
void snf_buf_set_user_data(SN3BUF *pBuf, void* pUserData);
/**
* ����� �ݹ� 40101 �������Ͽ� ���� callback setter �Լ�
*
* @param pBuf						������ ������
* @param sn3buf_unknownfile_func	callback �Լ�
*/;
int  snf_buf_set_unknownfile_func(SN3BUF *pBuf, bool(*sn3buf_unknownfile_func)(SN3MFI* pMFI, SN3MFI* pNewMFI));

// User Marker Callback Function Define
#ifdef __cplusplus
/**
 * ����� �ݹ� ��ũ �Լ��� �����Ѵ�.
 *
 * @param pBuf				������ ������
 * @param snf_buf_marker_func ����� �ݹ� ��Ŀ �Լ� ������
 */
void snf_buf_set_marker_func(SN3BUF *pBuf, int(* sn3buf_marker_func)(SN3BUF* pBuf, void* pMarkerData, SN3MARKER *pMarker)=NULL);
#else
/**
 * ����� �ݹ� ��ũ �Լ��� �����Ѵ�.
 *
 * @param pBuf				������ ������
 * @param snf_buf_marker_func ����� �ݹ� ��Ŀ �Լ� ������
 */
void snf_buf_set_marker_func(SN3BUF *pBuf, int(* sn3buf_marker_func)(SN3BUF* pBuf, void* pMarkerData, SN3MARKER *pMarker));
#endif //__cplusplus
/**
 * ����� �ݹ� ��ũ�� �����Ѵ�.
 *
 * @param pBuf			������ ������
 * @param pUserData		����� ������ ������
 */
void snf_buf_set_marker_data(SN3BUF *pBuf, void* pMarkerData);
/**
 * ����� �ݹ� ��Ŀ SKIP ������ Setter �Լ�
 *
 * @param pBuf				������ ������
 * @param snf_skip_command	��ŵ���
 */
void snf_buf_set_skip_command(SN3BUF *pBuf, int sn3_skip_command);
/**
 * ����� �ݹ� ��Ŀ SKIP ������ Getter �Լ�
 *
 * @param pBuf			������ ������
 * @return int			��ŵ���
 */
int snf_buf_get_skip_command(SN3BUF *pBuf);

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

/**************************************************************
*                  SN3(V3 ����) API �Լ�                      *
***************************************************************/

// Config //////////////////////////////////////////////////////
/**
* ���� ���� ������ ����Ѵ�.
*/
void sn3gbl_showcfg();
/**
 * ���� ���� ȯ�� ������ �Ѵ�.
 * @param pKeyStr ���̼��� ��ȣ. ������ ������� �ʾ� NULL �Ǵ� ""�Է�.
 * @param FileType ���͸� ��� ���� ����. SN3FILETYPE_ALL�� �����ϰ� Or�� �ߺ� ���� �����ϴ�.
 * @param Option  ���� ���� �ɼ�. Or�� �ߺ� ���� �����ϴ�.
 * @param BaseBufSize �޸� ���� ũ��.
 */
void sn3gbl_setcfg(const char * pKeyStr, __uint64 FileType, __uint64 Option, size_t BaseBufSize);
/**
 * ���� ���� ȯ�� �� �������� ���� �ɼ��� �����Ѵ�.
 * @param pKeyStr ���̼��� ��ȣ. ������ ������� �ʾ� NULL �Ǵ� ""�Է�.
 * @param FileType ���͸� ��� ���� ����.
 * @param Option  ���� ���� �ɼ�
 * @param BaseBufSize ���͸��� ���Ǵ� ���� ũ��.
 * @param opt	  ���� ���� ���͸�, ���� ���� ���� SN3OPTION_PARAM ����ü
 */
void sn3gbl_setcfgEx(const char * pKeyStr, __uint64 FileType, __uint64 Option, size_t BaseBufSize, SN3OPTION_PARAM opt);

// Utility /////////////////////////////////////////////////////
/**
* ���� �̸��� ���Ѵ�.
* @return	���� �̸��� �����Ѵ�.
*/
char* sn3ver_program();
/**
* ���� ������ ���Ѵ�.
* @return	���� ������ �����Ѵ�.
*/
char* sn3ver_version();

/**
* ���� ���� �ڵ带 ���Ѵ�.
* @param	pMFI	���� ������ ���Ϸ��� ������ �޸� ����ü ������
* @param	pFormat ���� �����ڵ尡 ��ϵ� int�� ������. ���� ���� �˻簡 �����ϸ� ��ϵ��� �ʴ´�.
* @return	���� �� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int sn3fmt_detect_m(SN3MFI *pMFI, int *pFormat);
/**
* ������ ���� ��θ� �̿��ؼ� ���� �ڵ带 ���Ѵ�.
* @param	pFilePath �����ڵ带 ���Ϸ��� ���� ������ ���.
* @param	pFormat ���� �����ڵ尡 ����ȴ�. ���� ���� �˻簡 �����ϸ� ��ϵ��� �ʴ´�.
* @return	���� �� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int sn3fmt_detect(__uint8 *pFilePath, int *pFormat);
/**
 * ������ ���ð�η� ���� ���� ������ ���Ѵ�.
 * @param	pFilePath	FILE ��� (�����ڵ� ���)
 * @param   pFormat	�����ڵ尡 ����ȴ�. ���� ���� �˻� ���� �� ��ϵ��� �ʴ´�.
 * @return	���� �� SN3OK��, ���� �� �ش� �����ڵ带 ��ȯ.
 */
int sn3fmt_wdetect(__ucs2 *pFilePath, int *pFormat);
/**
 * FormatCode �� ���� ������ �̸��� ã�´�.
 * @param	pFormatCode	�����ڵ�
 * @return	�����Ѱ�� ������ �̸���,
 *          �����Ѱ�� �����ڵ带 ��ȯ�Ѵ�.
 */
char* sn3fmt_format_name(int pFormatCode);

/**
 * FormatCode �� ���� ������ �̸��� ã�´�. ���� �����ϴ� ���˸� ã�´�.
 * @param	pFormatCode	�����ڵ�
 * @return	�����Ѱ�� ������ �̸���,
 *          �����Ѱ�� �����ڵ带 ��ȯ�Ѵ�.
 */
char* sn3fmt_formatcodeByName(int _formatCode);

/**
* ���� ��θ� �̿��� ���� ���͸��� ������ �������� true/false ����
* @param pFilePath  FILE ���
* @return ���͸��� �����ϸ� 1, �ƴϸ� 0�� ��ȯ�Ѵ�.
*/
int sn3fmt_isFilterFormat(__uint8 *pFilePath);
/**
* MFI�� ��� ���� ���� ���͸��� �������� true/false ����
* @param pMFI  MFI ������
* @return ���͸��� �����ϸ� 1, �ƴϸ� 0�� ��ȯ�Ѵ�.
*/
int sn3fmt_isFilterFormat_m(SN3MFI *pMFI);

/**
 * Next �����ڵ尡 (ERROR_SN3XXX_) �߸��� ����(���� ����)�� ������� Ȯ���Ѵ�.
 * @param	nErr	�����ڵ�
 * @return	�߸��� ����(���� ����) ��� ���� ������ ��ȯ.
 *          �ƴҰ�� 0�� ��ȯ
 */
int sn3err_isbadfile(int nErr);

/**
 * �����ڵ�(UCS2-LE) ���ڿ��� cp949 ���ڿ��� ����.
 * @param	wstr	�����ڵ� ���ڿ�
 * @return	���������� ��ȯ�Ȱ�� cp949�� �����͸� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
char* sn3ucs_ucs2cp949(__ucs2 *wstr);
/**
 * MS-CP949���ڿ��� UCS2-LE���ڿ��� ��ȯ�Ѵ�.
 * ��ȯ�� �����ڵ� ���ڿ��� ���߿� �� free ������� �Ѵ�.
 * @param	pCp949	MS-CP949���ڿ��� ��� �ִ� ���� ������
 * @return	���������� ��ȯ�Ǿ��� ��� ��ȯ�� __ucs2 *�� ��ȯ
 *          ��ȯ�� ������ �ִٸ� NULL�� ��ȯ
 */
__ucs2* sn3cp949_to_ucs2_str(__uint8 *pCp949);
/**
* ��ȯ��Ų �����ڵ� ���ڿ��� �޸� �����Ѵ�.
* @param	pMem  �޸� ������ �����ڵ� ���ڿ�
*/
void sn3utl_free(void *pMem);
/**
 * UCS2-LE ���ڿ��� ���̸� ��ȯ�Ѵ�.
 * @param	string	�����ڵ� ���ڿ��� ������
 * @return	�Էµ� �����ڵ� ���ڿ��� ���̸� ��ȯ.
 */
size_t sn3ucs_wcslen(__ucs2 *string );
/**
* �����ڵ� ���ڿ��� ���ڵ��Ѵ�.
* @param wstr �Է� UTF-8
* @param encoding ���ڵ� ����
* @return ���ڵ��� ����� ucs2 ���ڿ��� ��ȯ
*/
__uint8* sn3ucs_decode_str(__ucs2 *wstr, int encoding);
/**
* ucs2 ���ڿ��� �Է� �޾� ������ utf8 ���ڿ� �����ͷ� ��ȯ�Ѵ�.
* @param wstr �Է�
* @param wlen �Է� ����
* @param dest ����� utf ���ڿ�
* @param dlen ��� ����
* @param encoding ���ڵ� ����
* @return ����: SN3OK, ����: ERROR_UTF8_FROM_UCS2_LOOP_FULL_OUTPUT
*/
int sn3ucs_decode(__ucs2 *wstr, int wlen, __uint8* dest, int dlen, int encoding);

/**
* @brief utf8 ���ڿ��� ucs2 ���ڿ��� ��ȯ
* @details utf8 ���ڿ��� �Է� ������ ucs2 ���ڿ��� ��ȯ�Ѵ�.
*		   ��ȯ ���� �����ʹ� �ݵ�� sn3utl_free() �� �̿��� �����ؾ��Ѵ�.
*
* @param pUtf8 �Է� utf8 ������
* @see sn3utf8_to_ucs2(), sn3utf8_to_ucs2_loop(), sn3utl_free()
* @return ucs2 ���ڿ� ������
*/
__ucs2* sn3utf8_to_ucs2_str(__uint8 *pUtf8);


// SN3MFI ///////////////////////////////////////////////////////
// mfi open&close
/**
 * SN3MFI ��ü�� ����(�޸��Ҵ�)�ϰ� Default ������ �ʱ�ȭ �Ѵ�.
 * @param	ppMFI	SN3MFI �������� ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3mfi_fopen_rw(SN3MFI **ppMFI);
/**
 * SN3MFI ��ü�� ����(�޸��Ҵ�)�ϰ� �޸� ������ �������� �ʱ�ȭ �Ѵ�.
 * @param	pMemFile �޸� ���� ������
 * @param pMemSize �޸� ������ ũ��
 * @param ppMFI SN3MFI �������� ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3mfi_fopen_m(__uint8 *pMemFile, __int64 pMemSize, SN3MFI **ppMFI);
/**
 * SN3MFI ��ü�� ����(�޸��Ҵ�)�ϰ� �޸� ������ �������� �ʱ�ȭ �Ѵ�.
 * @param	pMemFile �޸� ���� ������
 * @param pMemSize �޸� ������ ũ��
 * @param ppMFI SN3MFI �������� ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3mfi_fopen(__uint8 *pFilePath, SN3MFI **ppMFI);
/**
 * SN3MFI ��ü�� ����(�޸��Ҵ�)�ϰ� ������ �������� �ʱ�ȭ �Ѵ�.
 * @param	pFilePath ��Ƽ����Ʈ ���ϸ�
 * @param ppMFI SN3MFI �������� ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3mfi_wfopen(__ucs2 *pFilePath, SN3MFI **ppMFI);
/**
 * SN3MFI ��ü�� �ı�(�޸𸮹�ȯ)�Ѵ�.
 * @param pMFI SN3MFI ������
 * @return	���������� �޸𸮰� ��ȯ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3mfi_fclose(SN3MFI *pMFI);

// mfi misc
/**
 * SN3MFI ��ü�� ���� ���� �������� ó������ ������.
 * @param pMFI SN3MFI ������
 */
void sn3mfi_rewind(SN3MFI *pMFI);
/**
 * SN3MFI ��ü�� ���� �������� ���� �÷��׿� ���� Ư�� ��ġ�� �����Ѵ�.
 * ������ ���� �÷��״� SN3MFI_SEEK_SET, SN3MFI_SEEK_CUR, SN3MFI_SEEK_END
 * �� �ϳ����� �Ѵ�.
 * @param pMFI SN3MFI ������
 * @param pOffset �� ������
 * @param pOrigin ������ ���� �÷���
 * @return	pMFI�� ���� �������� ����� ������ �� �ִٸ� SN3OK��
 *					�ƴϸ� �ش� ������ ��ȯ.
 */
__int64 sn3mfi_fseek(SN3MFI *pMFI, __int64 pOffset, int pOrigin);
/**
 * SN3MFI ��ü�� ���� ũ�⸦ �����Ѵ�.
 * @param pMFI SN3MFI ������
 * @return	pMFI�� ���� ũ�� ��ȯ.
 */
size_t sn3mfi_fsize(SN3MFI *pMFI);
/**
 * SN3MFI ��ü�� ���� �������� �����Ѵ�.
 * @param pMFI SN3MFI ������
 * @return	pMFI�� ���� ������.
 */
__int64 sn3mfi_ftell(SN3MFI *pMFI);
/**
 * SN3MFI ��ü�� ���� �������� �������� �����ߴ��� �˻��Ѵ�.
 * @param pMFI SN3MFI ������
 * @return	pMFI�� ���� �������� �������� ���������� 1��
 *					�ƴϸ� 0�� ��ȯ.
 */
int sn3mfi_feof(SN3MFI *pMFI);
/**
 * SN3MFI ��ü�� ���� ���� �����Ǻ��� ������ Ư�� ���Ͽ� ����Ѵ�.
 * @param pMFI SN3MFI ������
 * @param pFilePath ��� ��� ���ϸ�
 * @return	���� ������ �ش� ������
 *					�ƴϸ� SN3OK�� ��ȯ.
 */
int sn3mfi_unload(SN3MFI *pMFI, __uint8 *pFilePath);

// mfi read
/**
*SN3MFI ��ü�� ���� ���� �������� ������ �а�
* ���� �������� 1 ������Ų��.
* @param pMFI SN3MFI ������
* @return	���� �������� ������ ���̶�� EOF��
* �ƴϸ� ���� ������ ��ȯ.
*/
int sn3mfi_fgetc(SN3MFI *pMFI);
/**
 * SN3MFI ��ü�� ���� ���� �������� �ٷ� ���� ������ �а�
 * ���� �������� 1 ���ҽ�Ų��.
 * @param pMFI SN3MFI ������
 * @param ch ���Ϲ��� ��
 * @return	���� �������� ó���̶�� EOF��
 *					�ƴϸ� ch�� ��ȯ.
 */
int sn3mfi_fungetc(SN3MFI *pMFI, int ch);
/**
 * SN3MFI ��ü�� ���� ���� �����Ǻ��� pSize*pCount ��ŭ�� ������
 * ���ۿ� ����� �� ���� ����Ʈ �� ��ŭ ���� �������� 1 ������Ų��.
 * ���� ����Ʈ���� ������ ���� �����ǿ��� ������������ ����Ʈ������ ũ��
 * ���� ����Ʈ���� �������Ѵ�.
 * @param pMFI SN3MFI ������
 * @param pBuffer __uint8�� ���� ���� ������
 * @param pSize pBuffer�� ����Ÿ�� ũ��
 * @param pCount ���� ����
 * @return	���� �о���� ������ ��ȯ.
 */
__int64 sn3mfi_fread(SN3MFI *pMFI, __uint8 *pBuffer, size_t pSize, size_t pCount);

// mfi write
/**
 * SN3MFI ��ü�� ���� ���� �����ǿ� ���� ����ϰ� �������� 1 ������Ų��.
 * SN3MFI ��ü�� pFile�� NULL�̸�
 * SN3MFI_REALLOC_SIZE ��ŭ�� �޸𸮸� ���� �Ҵ��ϰ�,
 * ��� ���� �������� Limit�� ������
 * SN3MFI_REALLOC_SIZE ��ŭ�� �޸𸮸� �߰��� �Ҵ��Ѵ�.
 * @param pMFI SN3MFI ������
 * @param ch ����� ������
 * @return	�޸� ������ ���� EOF��
 *					����� ��ϵǾ����� ch�� ��ȯ.
 */
int sn3mfi_fputc(SN3MFI *pMFI, int ch);
/**
 * SN3MFI ��ü�� ���� ���� �����Ǻ��� �Է¹��� ������ ������ ����Ѵ�.
 * SN3MFI ��ü�� pFile�� NULL�̸�
 * �ʿ��� ��ŭ�� �޸𸮸� ���� �Ҵ��ϰ�,
 * ��� ���� �������� Limit�� ������
 * �ʿ��� ��ŭ�� �޸𸮸� �߰��� �Ҵ��Ѵ�.
 * ����� ���� ����Ʈ�� ��ŭ ���� �������� ������Ų��.
 * @param pMFI SN3MFI ������
 * @param pBuffer ���Ͽ� ����� ����
 * @param pSize pBuffer�� ����Ÿ�� ũ��
 * @param pCount ����� ����
 * @return	�޸� ������ ���� 0��
 *					��ϵǾ����� ����� ������ ��ȯ.
 */
size_t sn3mfi_fwrite(SN3MFI *pMFI, __uint8 *pBuffer, size_t pSize, size_t pCount);


// SN3BUF //////////////////////////////////////////////////////
// Buffer init & free
/**
 * UCS2-LE ���۸� �ʱ�ȭ �Ѵ�.
 * @param	pBuf	���� �������� ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3buf_init(SN3BUF **pBuf);
/**
 * UCS2-LE ������ �޸𸮸� ��ȯ�Ѵ�.
 * @param	pBuf	������ ������
 * @return	���������� �޸𸮸� ��ȯ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3buf_free(SN3BUF *pBuf);

// Buffer misc
/**
 * ���۰� ����ִ��� Ȯ���Ѵ�.
 * @param	pBuf	�����ڵ� ������ ������
 * @return	����ִٸ� 1
 *          ������� �ʴٸ� 0 �� ��ȯ
 */
int sn3buf_isempty(SN3BUF *pBuf);
/**
 * UCS2-LE ������ ũ�⸦ ��ȯ�Ѵ�.
 * @param	pBuf	������ ������
 * @return	������ ũ�⸦ ��ȯ.
 */
size_t sn3buf_size(SN3BUF *pBuf);
/**
* ���۸� ����.
* @param  pBuf  ������ ������
* @return ���۸� ��� �� SN3OK ��ȯ
*/
int sn3buf_clear(SN3BUF *pBuf);
/**
* ù��° �Ű����� ���� �ڿ� �ι�° �Ű����� ���۸� ���δ�.
* @param  pBuf  ������ ������
* @param  pBufAdd  ������ ������ ������
* @return ���������� ���۰� ���ٿ����ٸ� SN3OK��ȯ.
*		  ������ �ִ� ��쿡�� �ش� �����ڵ� ��ȯ.
*/
int sn3buf_append(SN3BUF *pBuf, SN3BUF *pBufAdd);

// Buffer Unloading
/**
 * UCS2-LE ������ ������ ������ encoding ���·� MFI�� ����Ѵ�.
 * @param	pBuf	������ ������
 * @param	pMFI	MFI�� ������
 * @param	pEncoding	Endocding Ÿ��
 * @return	���������� �޸𸮸� ��ȯ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3buf_unload_m(SN3BUF *pBuf, SN3MFI *pMFI, __int32 pEncoding);
/**
 * UCS2-LE ������ ������ ������ encoding ���·�
 * ��������� �������Ͽ� ����Ѵ�.
 * @param	pBuf	������ ������
 * @param	pFilePath   ��� ���ϰ��
 * @param	pEncoding	Endocding Ÿ��
 * @return	���������� �޸𸮸� ��ȯ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3buf_unload(SN3BUF *pBuf, __uint8 *pFilePath, __int32 pEncoding);
/**
 * UCS2-LE ������ ������ ������ encoding ���·�
 * ��������� �������Ͽ� ����Ѵ�.
 * @param	pBuf	������ ������
 * @param	pFilePath   ��� ���ϰ�� (�����ڵ� ���)
 * @param	pEncoding	Endocding Ÿ��
 * @return	���������� �޸𸮸� ��ȯ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3buf_wunload(SN3BUF *pBuf, __ucs2 *pFilePath, __int32 pEncoding);

// Buffer Put (UCS2 Version)
/**
 * UCS2-LE ���ڸ� ���ۿ� �ִ´�. ���ۿ��� �׻� ��������
 * �����ڵ� ���ڰ� LE ���·� �־���Ѵ�. SN3NOCHAR��
 * SN3NULL � �� �� ����. ����ũ�Ⱑ �����ϸ� ���۸� �ø���.
 * @param	pBuf	������ ������
 * @param	ch		UCS2 ����
 * @return	���������� �Էµ� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3buf_putc_ucs2_raw(SN3BUF *pBuf, __ucs2 ch);
/**
 * UCS2-LE ���ڸ� ���ۿ� �ִ´�. ���ۿ��� �׻� ��������
 * �����ڵ� ���ڰ� LE ���·� �־���Ѵ�. SN3NOCHAR��
 * SN3NULL � �� �� ����. ����ũ�Ⱑ �����ϸ� ���۸� �ø���.
 * @param	pBuf	������ ������
 * @param	ch		UCS2 ����
 * @return	���������� �Էµ� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3buf_putc_ucs2(SN3BUF *pBuf, __ucs2 ch);
/**
 * UCS2-LE ���ڿ��� ���ۿ� �ִ´�. UCS2-LE ���ڿ��� ����
 * SN3NULL�� �� �־���ϸ�, ���ۿ� SN3NULL�� ���� �ʴ´�.
 * ���ڿ��߿� SN3NOCHAR ���� ������ �����ϰ� �����Ѵ�.
 * @param	pBuf	������ ������
 * @param	str		UCS2 ���ڿ�
 * @return	���������� �Էµ� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3buf_puts_ucs2(SN3BUF *pBuf, __ucs2 *str);
/**
 * UCS2-BE ���ڿ��� ���ۿ� �ִ´�. UCS2-BE ���ڿ��� ����
 * SN3NULL�� �� �־���ϸ�, ���ۿ� SN3NULL�� ���� �ʴ´�.
 * ���ڿ��߿� SN3NOCHAR ���� ������ �����ϰ� �����Ѵ�.
 * @param	pBuf	������ ������
 * @param	str		UCS2 ���ڿ�
 * @return	���������� �Էµ� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3buf_puts_ucs2_be(SN3BUF *pBuf, __ucs2 *str);
/**
 * UCS2-BE ���ڿ��� ���ۿ� �ִ´�. UCS2-BE ���ڿ��� ����
 * SN3NULL�� �� �־���ϸ�, ���ۿ� SN3NULL�� ���� �ʴ´�.
 * ���ڿ��߿� SN3NOCHAR ���� ������ �����ϰ� �����Ѵ�.
 * @param	pBuf	������ ������
 * @param	str		UCS2 ���ڿ�
 * @return	���������� �Էµ� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3buf_put_newline(SN3BUF *pBuf);
/**
 * ���ۿ� ���� ���ڸ� �Է�.
 * @param	pBuf	�����ڵ� ������ ������
 * @return	���������� �ԷµȰ�� SN3OK ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3buf_put_space(SN3BUF *pBuf);

// Buffer Peek & Get (UCS2 Version)
/**
 * ���ۿ� ���� ó���� �Էµ� ���ڸ� Ȯ���Ѵ�.
 * @param	pBuf	�����ڵ� ������ ������
 * @return	���������� ����Ǿ��ٸ�
 *          ù��° ����(__ucs2)�� ��ȯ.
 *          ���۰� ����ִٸ� SN3NOCHAR ��ȯ.
 */
__ucs2 sn3buf_peekstart(SN3BUF *pBuf);
/**
 * ���ۿ� ���� �������� �Էµ� ���ڸ� Ȯ���Ѵ�.
 * @param	pBuf	�����ڵ� ������ ������
 * @return	���������� ����Ǿ��ٸ�
 *          ����������(__ucs2)�� ��ȯ.
 *          ���۰� ����ִٸ� SN3NOCHAR ��ȯ.
 */
__ucs2 sn3buf_peekend(SN3BUF *pBuf);
/**
 * ������ ���� �տ� �ִ� UCS2-LE ���ڸ� �о�´�.
 * @param	pBuf	�����ڵ� ������ ������
 * @return	���ۿ��� �о �����ڵ带 ��ȯ
 *          ���ۿ� ������� SN3NOCHAR�� ��ȯ
 */
__ucs2 sn3buf_getwch(SN3BUF *pBuf);
/**
 * ������ ���ʿ� UCS2-LE ���ڸ� �ִ´�.
 * @param	pBuf	�����ڵ� ������ ������
 * @param	ch		���� �����ڵ� ����
 * @return	������ ������ SN3OK,
 *          ������ ������ ��á���� �����ڵ带 ��ȯ
 */
int sn3buf_ungetwch(SN3BUF *pBuf, __ucs2 ch);
/**
 * ���ۿ��� UCS2-LE ���ڿ��� �о�´�.
 * @param	pBuf	�����ڵ� ������ ������
 * @param	buf		�޾ƿ� ������ ������
 * @param	buf_size	�޾ƿ� ������ ũ��
 * @return	�о ä�� �����ڵ� ����(size_t)�� ��ȯ
 *          ������ �ִٸ� 0�� ��ȯ.
 */
size_t sn3buf_get_ucs2(SN3BUF *pBuf, __ucs2 *buf, int buf_size);

// Buffer Put & Get (CP949 Version)
/**
 * MS-CP949 ���ڸ� ���ۿ� �ִ´�.
 * @param	pBuf	������ ������
 * @param	ch		MS-CP949 ����
 * @return	���������� �Էµ� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3buf_putc_cp949(SN3BUF *pBuf, __uint16 ch);
/**
 * MS-CP949 ���ڿ��� ���ۿ� �ִ´�. ���ڿ��� �� NULL��
 * �����߰ڴ�.
 * @param	pBuf	������ ������
 * @param	str		MS-CP949 ���ڿ�
 * @return	���������� �Էµ� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3buf_puts_cp949(SN3BUF *pBuf, __uint8 *str);
/**
 * ���ۿ��� MS-CP949 ���ڿ��� �о�´�.
 * @param	pBuf	�����ڵ� ������ ������
 * @param	buf		�޾ƿ� ������ ������
 * @param	buf_size	�޾ƿ� ������ ũ��
 * @return	�о ä�� ����Ʈ��(size_t)�� ��ȯ
 *          ������ �ְų� ���̻� �����ð� ������ 0�� ��ȯ.
 */
size_t sn3buf_get_cp949(SN3BUF *pBuf, __uint8 *buf, int buf_size);

// Buffer position
/**
 * ������ �������� ���� �Ѵ�.
 * pos �� 0 ���� ���� ��� ���������� ä���� ������ ū���� ���������� �̵�.
 * @param	pBuf	�����ڵ� ������ ������
 * @param	pos		������ ������ ������
 * @return
 */
void sn3buf_setpos(SN3BUF *pBuf, size_t pos);
/**
 * ������ �������� ���������� �Ű��ش�.
 * @param	pBuf	�����ڵ� ������ ������
 * @return  ���۰� ����ִٸ� 0, ������� �ʴٸ� ������ �������� ��ȯ.
 */
size_t sn3buf_getpos(SN3BUF *pBuf);
/**
 * ������ �������� ���������� �Ű��ش�.
 * @param	pBuf	�����ڵ� ������ ������
 */
void sn3buf_rewind(SN3BUF *pBuf);

// Text getter
/**
 * ���ۿ��� ������ ���ڵ����� ���ڿ��� �о�´�.
 * @param	pBuf	�����ڵ� ������ ������
 * @param	buf		�޾ƿ� ������ ������
 * @param	buf_size	�޾ƿ� ������ ũ��
 * @param	encoding	������ ���ڵ�
 * @return	�о ä�� ����Ʈ��(size_t)�� ��ȯ
 *          ������ �ְų� ���̻� �����ð� ������ 0�� ��ȯ.
 */
size_t sn3buf_get_text(SN3BUF *pBuf, __uint8 *buf, int buf_size, int encoding);
/**
 * ���ۿ��� ������ ���ڵ����� ���ڿ��� �о�´�.
 * @param	pBuf	�����ڵ� ������ ������
 * @param	buf		�޾ƿ� ������ ������
 * @param	buf_size	�޾ƿ� ������ ũ��
 * @param	encoding	������ ���ڵ�
 * @return	�о ä�� ����Ʈ��(size_t)�� ��ȯ
 *          ������ �ְų� ���̻� �����ð� ������ 0�� ��ȯ.
 */
size_t sn3buf_get_text_le(SN3BUF *pBuf, __uint8 *buf, int buf_size, int encoding);


// SN3SUM //////////////////////////////////////////////////////
/**
 * SN3SUM ��ü�� �ʱ�ȭ�Ѵ�.
 * @param	ppSum SN3SUM �������� ������
 * @return	����� �޸𸮸� �Ҵ��ϸ� SN3OK�� ��ȯ�ϰ�
 *					������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3sum_init(SN3SUM **ppSum);
/**
 * SN3SUM ��ü�� �޸𸮸� �����Ѵ�.
 * @param	pSum SN3SUM ������
 * @return	����� �޸𸮸� �����ϸ� SN3OK�� ��ȯ�ϰ�
 *					������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3sum_free(SN3SUM *pSum);
/**
 * SN3SUM�� ������ ȭ�鿡 ����Ѵ�.
 * @param	pSum SN3SUM ������
 * @return	SN3OK�� ��ȯ�Ѵ�.
 */
int sn3sum_show(SN3SUM *pSum);

// Summary Unloading ...
/**
 * SN3SUM�� ������ SN3MFI�� ���ڵ� ��Ŀ� �°� �����Ѵ�.
 * @param	pSum SN3SUM ������
 * @param	pMFI SN3MFI ������
 * @param	pEncoding ���ڵ� ���
 * @return	SN3OK�� ��ȯ�Ѵ�.
 */
int sn3sum_unload_m(SN3SUM *pSum, SN3MFI *pMFI, __int32 pEncoding);
/**
 * SN3SUM�� ������ FILE�� ���ڵ� ��Ŀ� �°� �����Ѵ�.
 * @param	pSum SN3SUM ������
 * @param	pFile FILE ������
 * @param	pEncoding ���ڵ� ���
 * @return	���Ͽ� ����� ���������� SN3OK�� ��ȯ�ϰ�
 *			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3sum_unload_f(SN3SUM *pSum, FILE *pFile, __int32 pEncoding);
/**
 * SN3SUM�� ������ ���Ͽ� ���ڵ� ��Ŀ� �°� �����Ѵ�.
 * @param	pSum SN3SUM ������
 * @param	pFilePath ���ϸ�
 * @param	pEncoding ���ڵ� ���
 * @return	���Ͽ� ����� ���������� SN3OK�� ��ȯ�ϰ�
 *			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3sum_unload(SN3SUM *pSum, __uint8 *pFilePath, __int32 pEncoding);
/**
 * SN3SUM�� ������ ���Ͽ� ���ڵ� ��Ŀ� �°� �����Ѵ�.
 * @param	pSum SN3SUM ������
 * @param	pFilePath ���ϸ�
 * @param	pEncoding ���ڵ� ���
 * @return	���Ͽ� ����� ���������� SN3OK�� ��ȯ�ϰ�
 *			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3sum_wunload(SN3SUM *pSum, __ucs2 *pFilePath, __int32 pEncoding);

// Docinfo
/**
* ������ ��������� ����Ѵ�.
* @param  pFilePath ���ϸ�
* @param  pSum	SN3SUM ������
* @return ��������� ���������� ��µǸ� SN3OK�� ��ȯ�ǰ�
*			���߿� ������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
*/
int sn3flt_docinfo(__uint8 *pFilePath, SN3SUM *pSum);
/**
* �����ڵ� ����� ������ ��������� ����Ѵ�.
* @param  pFilePath ���ϸ�
* @param  pSum	SN3SUM ������
* @return ��������� ���������� ��µǸ� SN3OK�� ��ȯ�ǰ�
*			���߿� ������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
*/
int sn3flt_wdocinfo(__ucs2 *pFilePath, SN3SUM *pSum);
/**
* �޸𸮿� �ִ� ������ ��������� ����Ѵ�.
* @param  pMFI SN3MFI ������
* @param  pSum	SN3SUM ������
* @return ��������� ���������� ��µǸ� SN3OK�� ��ȯ�ǰ�
*			���߿� ������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
*/
int sn3flt_docinfo_m(SN3MFI *pMFI, SN3SUM *pSum);
/**
 * Ư�� ������ DocumentSummaryInformation�� SN3BUF�� �����Ѵ�.
 * @param	pFilePath ���ϸ�
 * @param	pBuf SN3BUF�� ������
 * @return	SummaryInformation�� ������ ����� SN3BUF�� �����ϸ� SN3OK�� ��ȯ�ϰ�
 *			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3flt_docinfoEx(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * Ư�� ������ DocumentSummaryInformation�� SN3BUF�� �����Ѵ�.
 * @param	pFilePath ���ϸ�
 * @param	pBuf SN3BUF�� ������
 * @return	SummaryInformation�� ������ ����� SN3BUF�� �����ϸ� SN3OK�� ��ȯ�ϰ�
 *			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3flt_wdocinfoEx(__ucs2 *pFilePath, SN3BUF *pBuf);
/**
 * �޸𸮿� ��� ������ DocumentSummaryInformation�� SN3BUF�� �����Ѵ�.
 * @param	pMFI SN3MFI ������
 * @param	pBuf SN3BUF�� ������
 * @return	SummaryInformation�� ������ ����� SN3BUF�� �����ϸ� SN3OK�� ��ȯ�ϰ�
 *			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3flt_docinfoEx_m(SN3MFI *pMFI, SN3BUF *pBuf);

// Filter (FilePath) ///////////////////////////////////////////
/**
 * ���� ���͸� �� ��� �ؽ�Ʈ�� ���ۿ� ����Ѵ�.
 * @param	pFilePath	��� ���� ���
 * @param   pBuf  ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param   WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����: SN3OK, ����: �ش� �����ڵ�
 */
int sn3flt_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
* ���� ���͸� �� ��� �ؽ�Ʈ�� ���Ͽ� ����Ѵ�. (len�� wcslen()���� ����)
* @param *pFilePath �Է����� ���
* @param *pOutPath ������� ���. NULL�� ��� stdout�� ���
* @param WithPage ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
* @param encoding ��� �ؽ�Ʈ ���ڵ�
* @return ����: SN3OK, ����: �ش� �����ڵ�
*/
int sn3flt_filter_ex(__uint8 *pFilePath, __uint8 *pOutPath, int WithPage, int encoding);
/**
 * ���� ���͸� �� ��� �ؽ�Ʈ�� ���ۿ� ����Ѵ�.
 * @param	pFilePath	��� ���� ���
 * @param   pBuf  ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param   WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����: SN3OK, ����: �ش� �����ڵ�
 */
int sn3flt_wfilter(__ucs2 *pFilePath, SN3BUF *pBuf, int WithPage);

/**
 * alz ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	alz ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage	 ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3alz_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * bzip ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	bzip ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3bzip_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * chm ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	chm ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3chm_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * doc ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	doc ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3doc_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * docx ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	docx ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3docx_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * dwg ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	dwg ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3dwg_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * GZ(GNU Zip) ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	GZ ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3gz_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * h2k ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	h2k ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3h2k_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * htm / html ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	htm / html ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3htm_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwn ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	hwn ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3hwn_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwd ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	hwd ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3hwd_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwp3 ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	hwp3 ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3hwp3_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwx ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	hwx ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3hwx_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * jtd ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	jtd ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3jtd_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * mdb ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	mdb ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3mdb_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * mdi ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	mdi ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3mdi_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * mht ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	mht ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3mht_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * mp3 ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	mp3 ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3mp3_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * msg ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	msg ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3msg_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * pdf ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	pdf ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3pdf_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * ppt ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	ppt ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3ppt_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * pptx ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	pptx ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3pptx_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * rtf ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	rtf ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3rtf_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * 7zip ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	7zip ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3sevenzip_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * swf ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	swf ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3swf_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * sxx ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	sxx ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3sxx_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * tar ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	tar ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3tar_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * txt ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	txt ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3txt_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * wpd ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	wpd ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3wpd_filter( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xls ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	xls ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3xls_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xlsx ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	xlsx ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3xlsx_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * hwp ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	hwp ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3xml_hwp_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xml office ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	xml office ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3xml_office_filter(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * zip ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	zip ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3zip_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * rar ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	rar ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3rar_filter( __uint8 *pFilePath, SN3BUF *pBuf, int WithPage);
/**
 * ndoc ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	ndoc ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3ndoc_filter(__uint8 *pFilePath, SN3BUF *pBuf, int WithPage);

/**
 * nsf ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	nsf ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3nsf_filter(__uint8* pFilePaht, SN3BUF* pBuf);
/**
 * edb ������ ���ۿ� ���͸� �Ѵ�.
 * @param	pFilePath	edb ���� ���
 * @param	pBuf	������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3edb_filter(__uint8* pFilePaht, SN3BUF* pBuf);

// Filter (MFI) ////////////////////////////////////////////////
/**
 * �޸𸮿� ��� ���� ���� ���͸� �� ���˿� �°� ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI �ҽ� ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3flt_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);

/**
 * alz ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI alz ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3alz_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * bzip ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI bzip ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3bzip_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * chm ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI chm ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3chm_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * doc ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI doc ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3doc_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * docx ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI docx ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3docx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * dwg ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI dwg ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3dwg_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * GZ ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI GZ ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3gz_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * h2k ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI h2k ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3h2k_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * htm ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI htm ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3htm_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * hwn ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI hwn ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3hwn_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * hwd ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI hwd ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3hwd_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * hwp3 ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI hwp3 ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3hwp3_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * hwx ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI hwx ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3hwx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * jtd ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI jtd ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3jtd_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * mdb ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI mdb ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3mdb_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * mdi ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI mdi ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3mdi_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * mht ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI mht ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3mht_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * mp3 ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI mp3 ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3mp3_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * msg ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI msg ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3msg_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * pdf ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI pdf ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3pdf_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * ppt ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI ppt ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3ppt_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * pptx ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI pptx ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3pptx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * rtf ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI rtf ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3rtf_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * 7zip ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI 7zip ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3sevenzip_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * swf ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI swf ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3swf_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * sxx ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI sxx ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3sxx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * tar ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI tar ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage ������ ������ ��� ����.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3tar_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * txt ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI txt ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3txt_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * wpd ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI wpd ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3wpd_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xls ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI xls ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3xls_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xlsx ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI xlsx ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3xlsx_filter_m(SN3MFI *pMFI, SN3BUF *pBuf );
/**
 * xml_hwp ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI xml_hwp ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3xml_hwp_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xml office ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI xml office ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3xml_office_filter_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * zip ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI zip ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3zip_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * rar ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI rar ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3rar_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);
/**
 * ndoc ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI ndoc ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3ndoc_filter_m(SN3MFI *pMFI, SN3BUF *pBuf, int WithPage);

/**
 * nsf ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI nsf ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3nsf_filter_m(SN3MFI* pMFI, SN3BUF* pBuf);
/**
 * edb ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI edb ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3edb_filter_m(SN3MFI* pMFI, SN3BUF* pBuf);

// Filter (MFI) with Format Code ///////////////////////////////
/**
 * �޸𸮿��� ���ڷ� ������ ��ȣ�� �ش��ϴ� ���� ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	WithPage  ������ ������ ��� ����. 1�̸� ���, 0�̸� ��¾���.
 * @param	FileFormat ���� ���� �ش� ��ȣ
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3flt_filter_c( SN3MFI *pMFI, SN3BUF *pBuf, int WithPage, int FileFormat);
/**
 * �޸𸮿��� ���ڷ� ������ ���ڵ����� txt ������ ���ۿ� ���͸��Ѵ�.
 * @param	pMFI ������ ��� �޸� ������
 * @param	pBuf ������ �ؽ�Ʈ�� ����� SN3BUF ������
 * @param	FileFormat ���ڵ� ��ȣ
 * @return	����� ���͸��ؼ� ���ۿ� ���� SN3OK �� ��ȯ�ϰ�
			������ �߻��ϸ� �ش� �����ڵ带 ��ȯ�Ѵ�.
 */
int sn3txt_filter_c( SN3MFI *pMFI, SN3BUF *pBuf, int FileFormat);


// File(sheet,table) list (FilePath) ///////////////////////////
/**
 * alz������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pFilePath	alz ���� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3alz_filelist( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * GZ������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pFilePath	gz ���� ���
 * @param	*pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3gz_filelist(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * mdb������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pFilePath	mdb ���� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3mdb_filelist( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * 7zip������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pFilePath	7zip���� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3sevenzip_filelist( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * tar������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pFilePath	tar ���� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3tar_filelist(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xls������ ��Ʈ ����� ����Ѵ�.
 *
 * @param	pFilePath	xls ���� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3xls_sheetlist ( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * xlsx������ ��Ʈ ����� ����Ѵ�.
 *
 * @param	pFilePath	xlsx ���� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3xlsx_sheetlist ( __uint8 *pFilePath, SN3BUF *pBuf);
/**
 * zip������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pFilePath	zip ���� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3zip_filelist(__uint8 *pFilePath, SN3BUF *pBuf);
/**
 * rar������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pFilePath	rar ���� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3rar_filelist(__uint8 *pFilePath, SN3BUF *pBuf);


// File(sheet,table) list (MFI) ////////////////////////////////
/**
 * alz������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	alz������ ��� �޸� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3alz_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * GZ������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	gz������ ��� �޸� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3gz_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * mdb������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	mdb������ ��� �޸� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3mdb_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * 7zip������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	7zip������ ��� �޸� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3sevenzip_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * tar������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	tar������ ��� �޸� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3tar_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xls������ ��Ʈ ����� ����Ѵ�.
 *
 * @param	pMFI	xls������ ��� �޸� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3xls_sheetlist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * xlsx������ ��Ʈ ����� ����Ѵ�.
 *
 * @param	pMFI	xlsx������ ��� �޸� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3xlsx_sheetlist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * zip������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	zip������ ��� �޸� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3zip_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);
/**
 * rar������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	rar������ ��� �޸� ���
 * @param	pBUF	SN3BUF ������
 * @return	���������� �޸𸮸� �Ҵ�ް� �ʱ�ȭ�� ��� SN3OK�� ��ȯ.
 *          ������ �ִٸ� �ش� �����ڵ带 ��ȯ.
 */
int sn3rar_filelist_m(SN3MFI *pMFI, SN3BUF *pBuf);

// File(sheet,table) raw list (MFI) ////////////////////////////////
/**
* ���� ���� ������ ��� �ִ� SN3ARFILIST�� �����ϰ� �ʱ�ȭ�Ѵ�.
* SN3ARFILIST ����ϱ� �� �ݵ�� �ʱ�ȭ�ؾ��ϸ� ����� ������ snf_arfilist_free()�� �����ؾ� �Ѵ�.
* @param	ppList  ��� SN3ARFILIST�� ���� ������
* @return	�����ϸ� SN3OK��, �����ϸ� �����ڵ带 ��ȯ�Ѵ�.
*/
int sn3arfilist_init(SN3ARFILIST** ppList);
/**
* SN3ARFILIST�� �޸� �����Ѵ�.
* @param	pList  �޸� ������ SN3ARFILIST ������
* @return	�����ϸ� SN3OK��, �����ϸ� �����ڵ带 ��ȯ�Ѵ�.
*/
void sn3arfilist_free(SN3ARFILIST* pList);
/**
* ��ī�̺� ���� ����Ʈ(SN3ARFILIST)���� idx��° raw������ �̸��� ��ȯ�Ѵ�.
* @param	pList �̸��� ������ SN3ARFILIST ������
* @param	idx	������ ������ ���� ��� �� ��ġ (0-based)
* @return	SN3ARFLIST�� idx��° ������ �̸��� ucs2 ���ڿ��� ���ϵȴ�.���� �� �����ڵ� ��ȯ.
*/
__uint8* sn3arfilist_name(SN3ARFILIST* pList, int idx);
/**
* ��ī�̺� ���� ����Ʈ(SN3ARFILST)�� idx��° ��¿� ���� �̸��� ��ȯ�Ѵ�.
* pBuf�� ��¿� ���� �̸��� ���ٿ�����, �ʿ��ϸ� snf_buf_clear()�� ���۸� ������ �Ѵ�.
* @param	pList �̸��� ������ SN3ARFILIST ������
* @param	idx	������ ������ ���� ��� �� ��ġ (0-based)
* @param	pBuf ���� �̸��� ��� SN3BUF ������
* @return	���� �� SN3OK��, �����ϸ� �����ڵ带 ��ȯ�Ѵ�.
*/
int sn3arfilist_printname(SN3ARFILIST* pList, int idx, SN3BUF* pBuf);
/**
* SN3ARFILIST�� ���� �ִ� ���� ��� ������ ��ȯ�Ѵ�.
* @param	pList SN3ARFILIST ������
* @return	���� �� SN3OK��, �����ϸ� �����ڵ带 ��ȯ�Ѵ�.
*/
int sn3arfilist_count(SN3ARFILIST* pList);

/**
 * alz������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	alz������ ��� �޸� ���
 * @param	pList	SN3ARFILIST ������
 * @return  SN3OK �Ǵ� �����ڵ�
 */
int sn3alz_filelistEx_m(SN3MFI *pMFI, SN3ARFILIST* pList);
/**
 * 7zip ������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	7zip������ ��� �޸� ���
 * @param	pList	SN3ARFILIST ������
 * @return  SN3OK �Ǵ� �����ڵ�
 */
int sn3sevenzip_filelistEx_m(SN3MFI *pMFI, SN3ARFILIST* pList);
/**
 * tar������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	tar������ ��� �޸� ���
 * @param	pList	SN3ARFILIST ������
 * @return  SN3OK �Ǵ� �����ڵ�
 */
int sn3tar_filelistEx_m(SN3MFI *pMFI, SN3ARFILIST* pList);
/**
 * zip������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	zip������ ��� �޸� ���
 * @param	pList	SN3ARFILIST ������
 * @return  SN3OK �Ǵ� �����ڵ�
 */
int sn3zip_filelistEx_m(SN3MFI *pMFI, SN3ARFILIST* pList);
/**
 * rar������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	rar������ ��� �޸� ���
 * @param	pList	SN3ARFILIST ������
 * @return  SN3OK �Ǵ� �����ڵ�
 */
int sn3rar_filelistEx_m(SN3MFI *pMFI, SN3ARFILIST* pList);
/**
 * egg������ ����� ���� ����� ����Ѵ�.
 *
 * @param	pMFI	egg������ ��� �޸� ���
 * @param	pList	SN3ARFILIST ������
 * @return  SN3OK �Ǵ� �����ڵ�
 */
int sn3egg_filelistEx_m(SN3MFI *pMFI, SN3ARFILIST* pList);

// Extract file from Archive ///////////////////////////////////
/**
* alz ���� ���� ���� ������ ���� ������ Ǯ�� SN3MFI�� ����.
* @param	pMFI ���� ������ ���� SN3MFI ������
* @param	pUzFile ���� ������ ������ ������ SN3MFI ������
* @param	pFileNm ���� ������ ������ ���
* @return	���� �� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int sn3alz_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* 7zip ���� ���� ���� ������ ���� ������ Ǯ�� SN3MFI�� ����.
* @param	pMFI ���� ������ ���� SN3MFI ������
* @param	pUzFile ���� ������ ������ ������ SN3MFI ������
* @param	pFileNm ���� ������ ������ ���
* @return	���� �� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int sn3sevenzip_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* tar ���� ���� ���� ������ ���� ������ Ǯ�� SN3MFI�� ����.
* @param	pMFI ���� ������ ���� SN3MFI ������
* @param	pUzFile ���� ������ ������ ������ SN3MFI ������
* @param	pFileNm ���� ������ ������ ���
* @return	���� �� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int sn3tar_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* zip ���� ���� ���� ������ ���� ������ Ǯ�� SN3MFI�� ����.
* @param	pMFI ���� ������ ���� SN3MFI ������
* @param	pUzFile ���� ������ ������ ������ SN3MFI ������
* @param	pFileNm ���� ������ ������ ���
* @return	���� �� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int sn3zip_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* rar ���� ���� ���� ������ ���� ������ Ǯ�� SN3MFI�� ����.
* @param	pMFI ���� ������ ���� SN3MFI ������
* @param	pUzFile ���� ������ ������ ������ SN3MFI ������
* @param	pFileNm ���� ������ ������ ���
* @return	���� �� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int sn3rar_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile, __uint8* pFileNm);
/**
* bzip ���� ���� ���� ������ ���� ������ Ǯ�� SN3MFI�� ����.
* @param	pMFI ���� ������ ���� SN3MFI ������
* @param	pUzFile ���� ������ ������ ������ SN3MFI ������
* @return	���� �� SN3OK��, ���� �� �����ڵ带 ��ȯ�Ѵ�.
*/
int sn3bzip_getfile_m(SN3MFI *pMFI, SN3MFI *pUzFile);

// User Callback Function Define ///////////////////////////////////
/**
 * ����� ���� �Լ��� �����Ѵ�.
 *
 * @param pBuf			   ������ ������
 * @param snf_buf_user_func ����� ���� �Լ� ������
 */
void sn3buf_set_user_func( SN3BUF *pBuf, void(* sn3buf_user_func)(SN3BUF* pBuf, void* pUserData) );
/**
 * ����� ����� �����Ѵ�.
 *
 * @param pBuf				������ ������
 * @param snf_user_command	����� ���
 */
void sn3buf_set_user_command(SN3BUF *pBuf, int sn3_user_command);
/**
 * ����� �����͸� �����Ѵ�.
 *
 * @param pBuf			������ ������
 * @param pUserData		����� ������ ������
 */
void sn3buf_set_user_data(SN3BUF *pBuf, void* pUserData);

// User Marker Callback Function Define
#ifdef __cplusplus
/**
 * ����� �ݹ� ��ũ �Լ��� �����Ѵ�.
 *
 * @param pBuf				������ ������
 * @param snf_buf_marker_func ����� �ݹ� ��Ŀ �Լ� ������
 */
void sn3buf_set_marker_func(SN3BUF *pBuf, int(* sn3buf_marker_func)(SN3BUF* pBuf, void* pMarkerData, SN3MARKER *pMarker)=NULL);
#else
/**
 * ����� �ݹ� ��ũ �Լ��� �����Ѵ�.
 *
 * @param pBuf				������ ������
 * @param snf_buf_marker_func ����� �ݹ� ��Ŀ �Լ� ������
 */
void sn3buf_set_marker_func(SN3BUF *pBuf, int(* sn3buf_marker_func)(SN3BUF* pBuf, void* pMarkerData, SN3MARKER *pMarker));
#endif //__cplusplus

/**
 * ����� �ݹ� ��ũ�� �����Ѵ�.
 *
 * @param pBuf			������ ������
 * @param pUserData		����� ������ ������
 */
void sn3buf_set_marker_data(SN3BUF *pBuf, void* pMarkerData);
/**
 * ����� �ݹ� ��ĿS KIP ������ Setter �Լ�
 *
 * @param pBuf				������ ������
 * @param snf_skip_command	��ŵ���
 */
void sn3buf_set_skip_command(SN3BUF *pBuf, int sn3_skip_command);
/**
 * ����� �ݹ� ��Ŀ SKIP ������ Getter �Լ�
 *
 * @param pBuf			������ ������
 * @return int			��ŵ���
 */
int sn3buf_get_skip_command(SN3BUF *pBuf);

// User Image Callback Function Define ////////////////////////////
/**
* �̹��� ���� callback setter �Լ�
*
* @param pBuf						������ ������
* @param wsnf_buf_set_img_flt_func	callback �Լ�
*/
int snf_buf_set_img_flt_func(SN3BUF *pBuf, bool(*sn3buf_img_flt_func)(void* pUserData, const __uint8* pStream, const size_t len, const __int32 imgIndex));
/**
* �̹��� ���� callback user data�� �����ϴ� �Լ�
*
* @param pBuf						������ ������
* @param pUserData					User Data�� ������
*/
int snf_buf_set_img_user_data(SN3BUF *pBuf, void* pUserData);
/**
* �̹��� ���� callback setter �Լ�
*
* @param pBuf						������ ������
* @param wsnf_buf_set_img_flt_func	callback �Լ�
*/
int snf_buf_set_txt_with_imgmarker_flt_func(SN3BUF *pBuf, bool(*sn3buf_txt_with_imgmarker_flt_func)(SN3BUF* pBuf, void* pUserData, const __int32 imgIndex));
/**
* �̹��� ���� callback setter �Լ�
*
* @param pBuf						������ ������
* @param wsnf_buf_set_img_flt_with_info_func	callback �Լ�
*/
int snf_buf_set_img_flt_with_info_func(SN3BUF *pBuf, __int32(*sn3buf_img_flt_with_info_func)(void* pUserData, const __uint8* pStream, const size_t len, const SN3IMGINFO imginfo));

// Memory Limit
/**
 * memory limit�� �����մϴ�.
 * @param limit	������ memory limit
 * @return size_t ������ �޸� ũ��
 */
int sn3set_memory_limit(int limit);
/**
 * memory limit���� ������ ���� ��ȯ�մϴ�.
 * @return size_t ������ �޸� ũ��
 */
size_t sn3mem_getMemoryLimit();
/**
 * �Ű������� �����ϰ� ����� ���ڿ��� �����͸� ��ȯ�Ѵ�.
 * @param _Src ������ ����
 * @return ����� ������ ������
 */
char* sn3strdup(const char* _Src);

/**
* �������� �Ҵ�� �Ű������� �޸𸮸� �����Ѵ�.
* @param PTR �޸� ������ ���� �Ҵ�� ����
*/
void sn3free(void *PTR);
#ifdef __cplusplus
}
#endif //__cplusplus

#endif /* SN3_H */
