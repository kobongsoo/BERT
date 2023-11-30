/**************************************************************
 *
 *  �� ���α׷��� (��)���̳�����Ʈ�� �ڻ��Դϴ�.
 *  (��)���̳�����Ʈ�� ���� ���Ǿ��� �����ϰų�
 *  �κ� ������ �� �����ϴ�.
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

/** @brief SN3MFI ����ü�� ���� �޸� �Ҵ� ���� 
*/
#define ERROR_SN3MFI_FOPEN_RW_MFI_MALLOC_FAILURE	10501 
/** @brief ���� �޸𸮰� NULL�̰ų� �޸� ũ�Ⱑ 0 ������ 
*/
#define	ERROR_SN3MFI_FOPEN_M_NULL_MEMFILE			10502 
/** @brief SN3MFI ����ü�� ���� �޸� �Ҵ� ���� 
*/
#define	ERROR_SN3MFI_FOPEN_M_MFI_MALLOC_FAILURE		10503 
/** @brief FILE �����Ͱ� NULL�̰ų� ������ ũ�Ⱑ 0 ������ 
*/
#define	ERROR_SN3MFI_FOPEN_F_NULL_FILE				10504 
/** @brief FILE�� ������ �б� ���� FILE ũ�� ��ŭ�� �޸� �Ҵ� ���� 
*/
#define	ERROR_SN3MFI_FOPEN_F_FILE_MALLOC_FAILURE	10505 
/** @brief FILE�� ������ �б� ���� FILE ũ�� ��ŭ�� �޸� �Ҵ� ���� 
*/
#define	ERROR_SN3MFI_FOPEN_F_MFI_MALLOC_FAILURE		10506 
/** @brief FILE ���� �б� ���� */
#define	ERROR_SN3MFI_FOPEN_F_FREAD_FAILURE			10507 

/** @brief FILE�� ��� ���ڿ��� NULL 
*/
#define	ERROR_SN3MFI_FOPEN_NULL_FILEPATH			10508 
/** @brief FILE�� ũ�Ⱑ 0 
*/
#define	ERROR_SN3MFI_FOPEN_FILE_SIZE_ZERO			10509 
/** @brief FILE �б� ������ ���� 
*/
#define	ERROR_SN3MFI_FOPEN_NO_READ_ACCESS			10510 
/** @brief FILE ���� �б� ����(STAT ����) 
*/
#define	ERROR_SN3MFI_FOPEN_READING_FILE_STAT		10511 
/** @brief FILE�� ������ �б� ���� FILE ũ�� ��ŭ�� �޸� �Ҵ� ���� 
*/
#define	ERROR_SN3MFI_FOPEN_FILE_MALLOC_FAILURE		10512 
/** @brief FILE ���� ���� 
*/
#define	ERROR_SN3MFI_FOPEN_FILE_OPEN_FAILURE		10513 
/** @brief FILE ���� �б� ���� 
*/
#define	ERROR_SN3MFI_FOPEN_FILE_READ_FAILURE		10514 
/** @brief SN3MFI ����ü�� ���� �޸� �Ҵ� ���� 
*/
#define	ERROR_SN3MFI_FOPEN_MFI_MALLOC_FAILURE		10515 

/** @brief SN3MFI �� NULL 
*/
#define	ERROR_SN3MFI_FCLOSE_NULL_MFI				10516 

/** @brief SN3MFI ���� ��ġ �̵� �� SN3MFI �� NULL 
*/
#define	ERROR_SN3MFI_FSEEK_NULL_FILE				10517 

/** @brief SN3MFI ���� ��ġ �̵� �� �߸��� ���� �ɼ� ���� 
*/
#define	ERROR_SN3MFI_FSEEK_BAD_ORIGIN				10519 

/** @brief SN3MFI�� ������ FILE�� ���� ���� 
*/
#define	ERROR_SN3MFI_UNLOAD_F_FWRITE_FAILURE		10520 
/** @brief SN3MFI�� ������ ���� ���� FILE ���� ���� 
*/
#define	ERROR_SN3MFI_UNLOAD_FILE_OPEN_FAILURE		10521 
/** @brief SN3MFI ������ NULL ����.
*/
#define	ERROR_SN3MFI_FCOPY_NULL_ERROR		10522 
/** @brief SN3MFI ���� ����.
*/
#define	ERROR_SN3MFI_FCOPY_WRITE_ERROR		10523 
/** @brief SN3MFI �ʱ�ȭ ���� ���� MFI ���.
*/
#define	ERROR_SN3MFI_UNINITIALIZED_ERROR		10524 

// SN3BUF ERROR //////////////////////////////////////////////////////////////////////////

/** @brief SN3BUF �޸� �Ҵ� �ʱ�ȭ ����
*/
#define	ERROR_SN3BUF_INIT_BUFFER_MEMORY_ALLOCATION_FAILURE	10601

/** @brief SN3BUF�� NULL�� �� �޸𸮸� �����ϴ� ���
*/
#define	ERROR_SN3BUF_FREE_BUFFER_IS_NULL			10602

/** @brief SN3BUF�� �ִ� ������ ���Ϸ� �������� ���� ���� ����
*/
#define	ERROR_SN3BUF_UNLOAD_FILE_OPEN_FAILURE			10603

/** @brief NULL�� SN3BUF�� UCS2 ���ڸ� ���ۿ� �������� �Ҷ� ����
*/
#define	ERROR_SN3BUF_PUTC_UCS2_BUFFER_IS_NULL			10604
/** @brief SN3BUF �޸� ���Ҵ� ����
*/
#define	ERROR_SN3BUF_PUTC_UCS2_BUFFER_REALLOCATION_FAILURE	10605

/** @brief NULL�� SN3BUF�� UCS2 ���ڿ��� ���ۿ� �������� �Ҷ� ����
*/
#define	ERROR_SN3BUF_PUTS_UCS2_BUFFER_IS_NULL			10607
/** @brief NULL�� ���ڿ��� SN3BUF�� �������� �Ҷ� ����
*/
#define	ERROR_SN3BUF_PUTS_UCS2_INPUT_IS_NULL			10608

/** @brief SN3BUF �����Ͱ� NULL�� ���
*/
#define	ERROR_SN3BUF_BUFFER_IS_NULL			10609

/** @brief �ӽ÷� ����� UCS2 ���ڿ��� �Ҵ� ����
*/
#define	ERROR_SN3BUF_PUTS_CP949_TMPOUTPUT_ALLOCATION_FAILURE	10611
/** @brief CP949 ���ڿ��� SN3BUF�� ��� �� �����Ͱ� ���ڿ��� �Ѿ
*/
#define	ERROR_SN3BUF_PUTS_CP949_OOPS_OUTPUT_OVERRUN		10612

/** @brief SN3BUF ���ʿ� UCS2-LE ���ڸ� ���� �� SN3BUF�� ��������Ʈ�� 0���� ���� ���
*/
#define	ERROR_SN3BUF_UNGETWCH_FAILURE				10613

/** @brief UTF8 �ؽ�Ʈ�� SN3BUF�� ��� �� �ӽ÷� ����� UCS2 �޸� �Ҵ� ���� 
*/
#define	ERROR_SN3BUF_PUTS_UTF8_TMPOUTPUT_ALLOCATION_FAILURE	10614 
/** @brief UTF8 �ؽ�Ʈ�� SN3BUF�� ��� �� �ӽ÷� ���Ǵ� UCS2 �޸� ���� 
*/
#define	ERROR_SN3BUF_PUTS_UTF8_OOPS_OUTPUT_OVERRUN		10615 


// OPENFILE ERROR  //////////////////////////////////////////////////////////////////////////

/** @brief OLE ���� ����� 512 byte �� ����� �ƴ� ���
*/
#define ERROR_SN3OLE_ISOLE_BAD_FILE_SIZE			10726

/** @brief OLE ���� ����� ���������� ���� ���
*/
#define ERROR_SN3OLE_ISOLE_FREAD_HEADER_FAILURE		10728
/** @brief OLE ���� ����� �������̳� OLE ID �� �������� ���
*/
#define ERROR_SN3OLE_ISOLE_BAD_OLE_ID				10729

/** @brief OLE ���� ����(BBD ROOT CHAIN �� �������� �������� ���)
*/
#define ERROR_SN3OLE_MOUNT2_BAD_ROOT_CHAIN_START		10734

/** @brief OLE ���� ����(SBD �� �������� �������� ���)
*/
#define ERROR_SN3OLE_MOUNT2_BAD_SBD_STARTBLOCK			10735

/** @brief BBD LIST ������ �޸� ���� �߻�
*/
#define ERROR_SN3OLE_MOUNT2_MALLOC_BBD_LIST_FAILURE		10736

/** @brief ROOT CHAIN ������ �޸� ���� �߻�
*/
#define ERROR_SN3OLE_MOUNT2_MALLOC_ROOT_CHAIN_FAILURE	10737

/** @brief SBD CHAIN ������ �޸� ���� �߻�
*/
#define ERROR_SN3OLE_MOUNT2_MALLOC_SBD_CHAIN_FAILURE	10738

/** @brief OLE ���� ����(BBD LIST �� �������� ���)
*/
#define ERROR_SN3OLE_MOUNT2_BAD_BBD_LIST				10739

/** @brief OLE ���� ����(BBD CHAIN �� �������� ���)
*/
#define ERROR_SN3OLE_MOUNT2_BAD_ROOT_CHAIN				10740

/** @brief SBD CHAIN �� �������� ���
*/
#define	ERROR_SN3OLE_MOUNT2_BAD_SBD_CHAIN				10741

/** @brief OLE ���� ����(MOUNT�� ROOT �� ã�� �� �ϴ� ���)
*/
#define	ERROR_SN3OLE_MOUNT2_OPEN_ROOT_FAILURE			10743

/** @brief BBD �� ���� ���� �������� ���
*/
#define	ERROR_SN3OLE_MOUNT2_BAD_BBD_NEXTBLOCK			10744

/** @brief UMOUNT �� �����Ͱ� �߸� �� ���
*/
#define ERROR_SN3OLE_UMOUNT_NULL_FILE_SYSTEM			10745

/** @brief Block �ּ��� NULL Pointer ����
*/
#define	ERROR_SN3OLE_BLOCKADDR_NULL_FILE_SYSTEM			10747

/** @brief Block �ּҿ� BLOCK ������ ��ġ ���� �ʴ� ���
*/
#define ERROR_SN3OLE_BLOCKADDR_BAD_BLOCK_NUMBER			10748

/** @brief ROOT Stroage Open �ÿ� NULL Pointer ����
*/
#define ERROR_SN3OLE_OPENROOT_NULL_FILE_SYSTEM			10749

/** @brief ROOT Stroage Open �ÿ� NULL Pointer ����
*/
#define ERROR_SN3OLE_OPENROOT_NULL_ROOT_DIR				10750

/** @brief ROOT PPS �� �������� ���
*/
#define	ERROR_SN3OLE_OPENROOT_BAD_ROOT_PPS				10751

/** @brief ROOT DIR Open �� �޸� ����
*/
#define	ERROR_SN3OLE_OPENROOT_MALLOC_ROOT_DIR_FAILURE	10752

/** @brief PPS �� ���� �� NULL Pointer ����
*/
#define	ERROR_SN3OLE_READPPS_NULL_PPS_BASE				10753

/** @brief PPS �� ���� �� NULL Pointer ����
*/
#define	ERROR_SN3OLE_READPPS_NULL_PPS					10754

/** @brief PPS Block�� �������� ���
*/
#define	ERROR_SN3OLE_READPPS_BROKEN_PPS_BLOCK			10755

/** @brief DIRPPS �� Prev PPS �� �������� ���
*/
#define	ERROR_SN3OLE_DIRPPS_BAD_PPS_PREV				10757

/** @brief DIRPPS �� Next PPS �� �������� ���
*/
#define	ERROR_SN3OLE_DIRPPS_BAD_PPS_NEXT				10758

/** @brief DIRPPS ���� File System ���ٽ� NULL Pointer ����
*/
#define	ERROR_SN3OLE_DIRPPS_NULL_FILE_SYSTEM			10759

/** @brief DIRPPS ���� Directory ���ٽ� NULL Pointer ����
*/
#define	ERROR_SN3OLE_DIRPPS_NULL_DIRECTORY				10760

/** @brief DIRPPS ���� PPS Index �� PPS Level �� �������� ���
*/
#define	ERROR_SN3OLE_DIRPPS_BAD_PPS_INDEX_OR_LEVEL		10761


/** @brief Openfile ���� File System ���ٽ�  NULL Pointer ����
*/
#define	ERROR_SN3OLE_FOPEN_NULL_FILE_SYSTEM				10768

/** @brief Openfile ���� ���� Directory ���ٽ� NULL Pointer ����
*/
#define	ERROR_SN3OLE_FOPEN_NULL_CURRENT_DIR				10769

/** @brief Openfile ���� �Է¹��� file ���� NULL �� ���
*/
#define	ERROR_SN3OLE_FOPEN_NULL_FILE_NAME				10770

/** @brief Openfile ���� Open �� ������ NULL �� ���
*/
#define	ERROR_SN3OLE_FOPEN_NULL_FILE					10771

/** @brief Openfile ���� File �� ã�� �� �ϴ� ���
*/
#define	ERROR_SN3OLE_FOPEN_NO_SUCH_FILE_NAME			10772

/** @brief Openfile ���� �޸� ���� �߻�
*/
#define	ERROR_SN3OLE_FOPEN_MALLOC_BLOCK_CHAIN_FAILURE		10773

/** @brief Openfile ���� Block chain �� �������� ���
*/
#define	ERROR_SN3OLE_FOPEN_BAD_BLOCK_CHAIN					10774

/** @brief Openfile ���� �޸� ���� �߻�
*/
#define	ERROR_SN3OLE_FOPEN_MALLOC_FILE_FAILURE				10775

/** @brief User DocInfo ���� Stream Buffer ������ �޸� ����
*/
#define	ERROR_SN3OLE_USER_DOCINFO_FS_MALLOC_STREAM_BUFFER_FAILURE	10821

// TXT ERROR /////////////////////////////////////////////////////////////////////////////
/** @brief TXT ���� ���͸� �� �޸� �Ҵ� ����
*/
#define	ERROR_SN3TXT_MEMORY_ALLOC_FAILURE	20000

// PDF ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief �Ϲ����� PDF ���� ����
*/
#define ERROR_SN3PDF								31100
/** @brief PDF ������ Stream Object ���� ����
*/
#define	ERROR_SN3PDF_OPEN_INPUT_STREAM				31101
/** @brief PDF ������ Stream Object ���� ���� �� ���� ��� �߻�
*/
#define	ERROR_SN3PDF_NO_INPUT_STREAM				31102
/** @brief PDF ������ Header ������ ���� �� �� ��� �߻�
*/
#define	ERROR_SN3PDF_ERROR_READING_PDF_HEADER		31103
/** @brief PDF ������ Xref �� �������� ã�� �� ��
*/
#define	ERROR_SN3PDF_READING_XREF_START				31104
/** @brief PDF ������ Xref �� �д� ���� ���� �߻�
*/
#define	ERROR_SN3PDF_READING_XREF					31105
/** @brief PDF ������ Page Catalog ������ ���� �� ��
*/
#define	ERROR_SN3PDF_PAGE_READING_CATALOG			31106
/** @brief PDF ������ Page Reference ������ ���� �� ��
*/
#define	ERROR_SN3PDF_READING_PAGE_REF				31107
/** @brief ���ȼ����� �Ǿ� �ִ� PDF ������ ��� �߻�
*/
#define	ERROR_SN3PDF_ENCRYPTED_PDF					31108
/** @brief PDF ������ Page Number �� ���������� ��� �߻�
*/
#define	ERROR_SN3PDF_INVALID_PAGE_NUM				31109
/** @brief �޸𸮾��� PDF ������ Input Stream Object ���� ����
*/
#define	ERROR_SN3PDF_FILTER_M_INVALID_INPUT_STREAM	31110
/** @brief PDf �������� �ؽ�Ʈ ���� ����
*/
#define	ERROR_SN3PDF_FILTER_M_FILTERING_FAILURE		31111
/** @brief PDF ������ Stream Object ���� ����
*/
#define ERROR_SN3PDF_MEMORY_ALLOC_FAILURE			31112



// MSG ERROR /////////////////////////////////////////////////////////////////////////////
/** @brief MSG ������ IPM.Note �� �������� ���
*/ 
#define	ERROR_SN3MSG_FILTER_FS_BAD_IPM_TYPE				39101 
/** @brief MSG �� ���� �б� ����
*/ 
#define	ERROR_SN3MSG_FILTER_M_FREAD_TITLE_FAILURE		39102

// MP3 ERROR /////////////////////////////////////////////////////////////////////////////
/** @brief MP3 ��� �б� ����
*/ 
#define	ERROR_SN3MP3_FILTER_M_FREAD_HEADER_FAILURE		30901
/** @brief MP3 ��� ������ �������� ���
*/ 
#define	ERROR_SN3MP3_FILTER_M_INVALID_MP3_HEADER		30902
/** @brief MP3 �� TAG �� �б� ����
*/ 
#define	ERROR_SN3MP3_FILTER_M_FREAD_TAG_FAILURE			30903
/** @brief MP3 �� TAG �� ã�� �� �ϴ� ���
*/ 
#define	ERROR_SN3MP3_FILTER_M_NO_TAG_FOUND				30904
/** @brief MP3 �� TAG �� ���� �б� ����
*/ 
#define	ERROR_SN3MP3_FILTER_M_FREAD_TITLE_FAILURE		30905
/** @brief MP3 �� TAG �� ���ǰ� �б� ����
*/ 
#define	ERROR_SN3MP3_FILTER_M_FREAD_ARTIST_FAILURE		30906
/** @brief MP3 �� TAG �� �ٹ����� �б� ����
*/ 
#define	ERROR_SN3MP3_FILTER_M_FREAD_ALBUM_FAILURE		30907
/** @brief MP3 �� TAG �� ���۳⵵ �б� ����
*/ 
#define	ERROR_SN3MP3_FILTER_M_FREAD_YEAR_FAILURE		30908
/** @brief MP3 �� TAG �� �ּ����� �б� ����
*/ 
#define	ERROR_SN3MP3_FILTER_M_FREAD_COMMENTS_FAILURE	30909

/** @brief MP3 ��� �б� ����
*/ 
#define	ERROR_SN3MP3_DOCINFO_M_FREAD_HEADER_FAILURE		30911
/** @brief MP3 ��� ������ �������� ���
*/ 
#define	ERROR_SN3MP3_DOCINFO_M_INVALID_MP3_HEADER		30912
/** @brief MP3 �� TAG �� �б� ����
*/ 
#define	ERROR_SN3MP3_DOCINFO_M_FREAD_TAG_FAILURE		30913
/** @brief MP3 �� TAG �� ã�� �� �ϴ� ���
*/ 
#define	ERROR_SN3MP3_DOCINFO_M_NO_TAG_FOUND				30914
/** @brief MP3 �� TAG �� ���� �б� ����
*/ 
#define	ERROR_SN3MP3_DOCINFO_M_FREAD_TITLE_FAILURE		30915
/** @brief MP3 �� TAG �� ���ǰ� �б� ����
*/ 
#define	ERROR_SN3MP3_DOCINFO_M_FREAD_ARTIST_FAILURE		30916
/** @brief MP3 �� TAG �� �ٹ����� �б� ����
*/ 
#define	ERROR_SN3MP3_DOCINFO_M_FREAD_ALBUM_FAILURE		30917
/** @brief MP3 �� TAG �� ���۳⵵ �б� ����
*/ 
#define	ERROR_SN3MP3_DOCINFO_M_FREAD_YEAR_FAILURE		30918
/** @brief MP3 �� TAG �� �ּ����� �б� ����
*/ 
#define	ERROR_SN3MP3_DOCINFO_M_FREAD_COMMENTS_FAILURE	30919

// MHT ERROR /////////////////////////////////////////////////////////////////////////////
/** @brief MHT ������ ����� �������� ���
*/ 
#define ERROR_SN3MHT_FILTER_M_INVALID_HEADER		33801
/** @brief MHT ������ �������� �ʴ� ���ڵ����� �Ǿ� �ִ� ���
*/ 
#define ERROR_SN3MHT_FILTER_M_UNSUPPORTED_ENCODING	33802
/** @brief MHT ������ �������� �ʴ� charset �� ���� ���
*/ 
#define ERROR_SN3MHT_FILTER_M_UNSUPPORTED_CHARSET	33803
/** @brief ������ �� ���� �� �ϰ� MULTIPART BOUNDARY �� ���� ���
*/ 
#define	ERROR_SN3MHT_FILTER_M_END_OF_MULTIPART		33804


// MDI ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief �ùٸ� MDI ������ �ƴ� ���
*/
#define ERROR_SN3MDI_FILTER_M_NOT_MDI_ERROR	32301
/** @brief MDI ���� �б� ����
*/
#define	ERROR_SN3MDI_FILTER_M_FREAD_ERROR		32302

// LZX ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief ������ ���� ���� 
*/
#define ERROR_SN3LZX_DATAFORMAT   65001
/** @brief �߸��� ������ 
*/
#define ERROR_SN3LZX_ILLEGALDATA  65002
/** @brief �޸� ���� 
*/
#define ERROR_SN3LZX_NOMEMORY     65003

// JTD ERROR /////////////////////////////////////////////////////////////////////////////


/** @brief ����� ID ������ �ùٸ��� �ʴ� ��� �߻�
*/
#define ERROR_DOCUMENT_TEXT_INVALID_HEADER_ID			56001

/** @brief ��� �������� �ؽ�Ʈ�� ID ������ �ùٸ��� �ʴ� ��� �߻�
*/
#define ERROR_DOCUMENT_TEXT_INVALID_RECORD_HEADER_ID	56002

/** @brief �޸� ����
*/
#define ERROR_JTD_OUT_OF_MEMORY							56003 

/** @brief �ʿ��� Ư�� ���ڰ� ���� ��� �߻� 
*/
#define ERROR_SN3JTD_ERROR_SPECIAL_DATA					56004 

// HWP3 ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief ��й�ȣ�� �ִ� HWP3 ���� ���͸� �� �߻� 
*/
#define	ERROR_SN3HWP3_FILTER_M_PASSWORD_EXISTS				30501 
/** @brief HWP3 ���� �ʱ�ȭ ���� 
*/
#define	ERROR_SN3HWP3_FILTER_M_INIT_HWP3_FAILURE			30502 
/** @brief HWP3 ���� ���� ���� 
*/
#define	ERROR_SN3HWP3_FILTER_M_HWP3_OPEN_FAILURE			30503 

/** @brief HWP3 ���� ������� �б� ���� 
*/
#define	ERROR_SN3HWP3_DOCINFO_M_FREAD_HWP_ID_FAILURE		30504 
/** @brief HWP3 ���� ��������� �߸��� ���� ��� 
*/
#define	ERROR_SN3HWP3_DOCINFO_M_INVALID_FILE_HEADER			30505 
/** @brief HWP3 ���� �߸��� ������� ������ 
*/
#define	ERROR_SN3HWP3_DOCINFO_M_INVALID_DOCINFO_SIZE		30506 
/** @brief HWP3 ���� ������� �б� ���� 
*/
#define	ERROR_SN3HWP3_DOCINFO_M_FREAD_HWP_SUMMARY_FAILURE	30507 
/** @brief HWP3 Style ������ �д� ���� ���� �߻�
*/
#define	ERROR_SN3HWP3_FILTER_STYLEINFO_READ_FAILURE			30508 
/** @brief HWP3 �׸���ü ������ �з��׷����� �д� ���� ���� �߻�
*/
#define	ERROR_SN3HWP3_FILTER_TEXTBOX_READ_FAILURE			30509 
/** @brief HWP3 v1.20 ������ �������� �ʴ´�. (v2.0 ���� ����)
*/
#define ERROR_SN3HWP3_FILTER_V120_NO_FILTER_ASSOCIATED		30510
/** @brief GZIP ó�� �� ����
*/
#define ERROR_SN3HWP3_FILTER_GZIP_INIT						30511
/** @brief HWP3 ��Ʈ ������ �д� ���� ���� �߻�
*/
#define ERROR_SN3HWP3_FILTER_FONTINFO_READ_FAILURE			30512
/** @brief HWP3 ���� ������ �д� ���� ���� �߻�
*/
#define ERROR_SN3HWP3_FILTER_PARALIST_READ_FAILURE			30513
/** @brief HWP3 �޸� �Ҵ� ����
*/
#define ERROR_SN3HWP3_FILTER_MALLOC_FAILURE					30514

// H2K ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief HWP 2000 ��������� �޸� �Ҵ� ���� 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_MALLOC_STREAM_BUFFER_FAILURE	33501 
/** @brief HWP 2000 ��������� �Ӽ��� �޸� �Ҵ� ���� 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_MALLOC_PROPSET_FAILURE			33502 
/** @brief HWP 2000 ��������� �߸��� ����Ʈ ���� 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_WRONG_BYTE_ORDER				33503 
/** @brief HWP 2000 ��������� �߸��� ���� ���� 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_WRONG_FORMAT_VERSION			33504 
/** @brief HWP 2000 ��������� �߸��� OLE �ü������(0:16bit Win, 1:Macintosh, 2:32bit Win)
*/
#define	ERROR_SN3H2K_DOCINFO_FS_WRONG_OS_KIND					33505 
/** @brief HWP 2000 ��������� �߸��� Reserved ���� 1���� Ŀ���� 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_WRONG_RESERVED					33506 
/** @brief HWP 2000 ��������� �߸��� Section Offset
*/
#define	ERROR_SN3H2K_DOCINFO_FS_WRONG_SECTION_OFFSET			33507 
/** @brief HWP 2000 ��������� �߸��� Section Size 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_WRONG_SECTION_SIZE				33508 
/** @brief HWP 2000 ��������� �߸��� Section ���� Property ���� 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_WRONG_NUM_OF_PROPS				33509 
/** @brief HWP 2000 ��������� �߸��� Property ID�� �迭
*/
#define	ERROR_SN3H2K_DOCINFO_FS_MALLOC_PROPSET_ID_FAILURE		33510  
/** @brief HWP 2000 ��������� �߸��� Property Offset�� �迭
*/
#define	ERROR_SN3H2K_DOCINFO_FS_MALLOC_PROPSET_OFFSET_FAILURE	33511 
/** @brief HWP 2000 ��������� �߸��� Property Ÿ�� 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_MALLOC_PROPSET_TYPE_FAILURE		33512 
/** @brief HWP 2000 ��������� �߸��� Property ID �Ǵ� Offset 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_WRONG_PROP_ID_OR_OFFSET			33513 
/** @brief HWP 2000 ��������� �����ڵ� ���ڿ� �޸� �Ҵ� ���� 
*/
#define	ERROR_SN3H2K_DOCINFO_FS_MALLOC_TMPWSTR_FAILURE			33514 
/** @brief HWP 2000 ��ȣȭ�� ���
*/
#define	ERROR_SN3H2K_FILTER_FS_FILE_ENCRYPTED					33515 

/** @brief HWP 2000 ������ ������ ���
*/
#define	ERROR_SN3H2K_FILTER_FS_FILE_DISTRIBUTION				33516

/** @brief HWP 2000 ���ڵ� ���� �б� ����
*/
#define	ERROR_SN3H2K_FILTER_READ_RECORD							33521

/** @brief HWP 2000 ���� �ؽ�Ʈ ���� �б� ����
*/
#define	ERROR_SN3H2K_FILTER_READ_PARA_TEXT						33522

/** @brief HWP 2000 ���� �������� �б� ����
*/
#define	ERROR_SN3H2K_FILTER_READ_PARA_CHARSHAPE					33523

/** @brief HWP 2000 ���� ���� �б� ����
*/
#define	ERROR_SN3H2K_FILTER_READ_SECTION						33524

/** @brief HWP 2000 GZIP �ʱ�ȭ ����
*/
#define	ERROR_SN3H2K_FILTER_GZIP_INIT							33525

/** @brief HWP 2000 ������� �޸� �Ҵ� ����
*/
#define	ERROR_SN3H2K_FILTER_PARAREADER_INIT_MEMORY_ALLOCATION	33526

/** @brief HWP 2000 �������� �޸� �Ҵ� ����
*/
#define	ERROR_SN3H2K_FILTER_CHAROBJECT_INIT_MEMORY_ALLOCATION	33527

/** @brief HWP 2000 �������� �޸� �Ҵ� ����
*/
#define	ERROR_SN3H2K_FILTER_SHAPEOBJECT_INIT_MEMORY_ALLOCATION	33528

/** @brief HWP 2000 ������ ���� ��� ���� ����.
*/
#define ERROR_SN3H2K_FILTER_READONLY_GZIP_BAD_HEADER			33529

/** @brief HWP 2000 ������ ���� DecryptGZIP �ʱ�ȭ ����
 */
#define ERROR_SN3H2K_FILTER_READONLY_GZIP_INIT					33530

/** @brief HWP 2000 ���� ����Ʈ ��� ����
 */
#define ERROR_SN3H2K_FILTER_READ_LIST_HEADER					33531

// by Ummi 2012.05.23
/** @brief HWP 2000 ����� ���� ������ �޸� �Ҵ� ���� 
*/
#define	ERROR_SN3H2K_USER_DOCINFO_FS_MALLOC_STREAM_BUFFER_FAILURE	33551 
/** @brief HWP 2000 ����� ���� ������ �Ӽ��� �޸� �Ҵ� ���� 
*/
#define	ERROR_SN3H2K_USER_DOCINFO_FS_MALLOC_PROPSET_FAILURE			33552 
/** @brief HWP 2000 ����� ���� ������ �߸��� ����Ʈ ���� 
*/
#define	ERROR_SN3H2K_USER_DOCINFO_FS_WRONG_BYTE_ORDER				33553 
/** @brief HWP 2000 ����� ���� ������ �߸��� Property Sets 
*/
#define ERROR_SN3H2K_USER_DOCINFO_FS_WRONG_NUM_PROPERTY_SETS		33554
/** @brief HWP 2000 ����� ���� ������ �߸��� Property ID�� �迭
*/
#define	ERROR_SN3H2K_USER_DOCINFO_FS_MALLOC_PROPSET_ID_FAILURE		33555 
/** @brief HWP 2000 ����� ���� ������ �߸��� Property Offset�� �迭
*/
#define	ERROR_SN3H2K_USER_DOCINFO_FS_MALLOC_PROPSET_OFFSET_FAILURE	33556 
/** @brief HWP 2000 ��� ���� �б� ����
*/
#define ERROR_SN3H2K_FILTER_WRONG_BLOCK_SIZE 33557
/** @brief HWP 2000 ��ȿ���� ���� ���ڵ� ���
 */
#define ERROR_SN3H2K_FILTER_INVALID_RECORD_HEADER					33558

// GZ ERROR //////////////////////////////////////////////////////////////////////////////

/** @brief GZ ������ �߸��� ��� ���� 
*/
#define	ERROR_SN3GZ_FILTER_M_FREAD_LOC_HEADER_FAILURE		33701 
/** @brief GZ ������ �߸��� ���� �ñ״�ó
*/
#define	ERROR_SN3GZ_FILTER_M_INVALID_FILE_SIGNATURE			33702 
/** @brief GZ ������ �߸��� ���� ������
*/
#define	ERROR_SN3GZ_FILTER_M_INVALID_FILE_LENGTH			33703 
/** @brief Deprecated
*/
#define	ERROR_SN3GZ_FILTER_M_FREAD_GZ_NAME_FAILURE			33704 
/** @brief Deprecated
*/
#define	ERROR_SN3GZ_FILTER_M_INVALID_COMPRESSED_LENGTH		33705 

/** @brief GZ ������ �߸��� ��� ������ ������ �� �߻�
*/
#define	ERROR_SN3GZ_FOPEN_M_INVALID_GZ_HEADER				33710 
/** @brief GZ ������ ������ �� MFI�� NULL�� �߻��ϴ� ���
*/
#define	ERROR_SN3GZ_FOPEN_M_NULL_MFI						33711 
/** @brief GZ ������ ������ �� ���� �б⿡ �����ϴ� ���
*/
#define	ERROR_SN3GZ_FOPEN_M_FREAD_FAILURE					33712 
/** @brief GZ ������ ������ �� �޸� �Ҵ� ����
*/
#define	ERROR_SN3GZ_FOPEN_M_MALLOC_ZFILE_FAILURE			33713 
/** @brief GZ ������ ������ �� �ñ״�ó�� ã�� ���� ���
*/
#define	ERROR_SN3GZ_FOPEN_M_INVALID_SIGNATURE				33714 
/** @brief GZ ���� ó�� �� ������ ���� ������ 
*/
#define	ERROR_SN3GZ_FOPEN_M_END_OF_FILELIST					33717 
/** @brief GZ ���� ó���� �޸� �Ҵ� ����
*/
#define	ERROR_SN3GZ_MEMORY_ALLOC_FAILURE					33718

/** @brief GZ ���� �ݱ� �� SN3GZ_FILE�� NULL 
*/
#define	ERROR_SN3GZ_FCLOSE_NULL_ZFILE						33721 

/** @brief GZ �������� �ʴ� ��������(ZIP ���� ����� STORED Ȥ�� DEFLATED �� �ƴ�)
*/
#define	ERROR_SN3GZ_UNZIP_M_NOT_SUPPORTED_COMPRESSION		33731 
/** @brief GZ ���������� ���� �޸� �Ҵ� ����
*/
#define	ERROR_SN3GZ_UNZIP_M_UNCOMPRESSED_MALLOC_FAILURE		33732 
/** @brief STORED ������ GZ ������ SN3MFI�κ��� �б� ����
*/
#define	ERROR_SN3GZ_UNZIP_M_STORED_DATA_FREAD_FAILURE		33733 
/** @brief STORED ������ GZ ������ SN3MFI�� ���� ����
*/
#define	ERROR_SN3GZ_UNZIP_M_STORED_DATA_FWRITE_FAILURE		33734 
/** @brief DEFLATED ������ GZ ������ SN3MFI�� ���� ����
*/
#define	ERROR_SN3GZ_UNZIP_M_DEFLATED_DATA_ZWRITE_FAILURE	33737 
/** @brief GZ ���� �ݱ� ����
*/
#define	ERROR_SN3GZ_UNZIP_M_GGZ_ZCLOSE_FAILURE				33738 
/** @brief 
*/
#define	ERROR_SN3GZ_UNZIP_M_IMPOSSIBLE_PATH_FLOW			33739 

/** @brief crc32 ����
*/
#define	ERROR_SN3GZ_UNZIP_M_CRC32							33740 

// GUL ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief �ƹ����� ������ ���� �������� ���� 
*/
#define	ERROR_SN3GUL_FILTER_FS_NOT_IMPLEMENTED_YET	33401 

// FLT ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief ���͸��� �������� �ʴ� ������ ���
*/
#define	ERROR_SN3FLT_FILTER_M_NO_FILTER_ASSOCIATED	40101

/** @brief ���͸��� �������� �ʴ� ������ ��������� ������ ���
*/
#define	ERROR_SN3FLT_DOCINFO_M_NO_FILTER_ASSOCIATED	40102

/** @brief RAR ���� ���� ������ �������� �ʴ´�.
*/
#define	ERROR_SN3RAR_SPLIT_COMPRESSED_FILE 40103

/** @brief ���͸��� �޸� �Ҵ� ����
*/
#define	ERROR_SN3FLT_MEMORY_ALLOC_FAILUER 40105

// DWG ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief ���� ����� �ּ� ������� ���� (0x19)
*/
#define ERROR_SN3DWG_FILTER_M_BAD_FILESIZE		31001
/** @brief �޸� �Ҵ� ����
*/
#define ERROR_SN3DWG_FILTER_M_MALLOC_FAILURE	31002

/** @brief DWG ������� �б� ����
*/
#define ERROR_SN3DWG_HEADER					31010

/** @brief DWG ������ �������� �ʴ� ���� ����
*/
#define ERROR_SN3DWG_HEADER_VERSION_UNKNOWN		31011
/** @brief ��� ������ ����� ���� ������� ū ���
*/
#define ERROR_SN3DWG_HEADER_BAD_ENTBLOCK		31033
/** @brief �߸��� ���� ���ù�ȣ
*/
#define ERROR_SN3DWG_HEADER_BAD_SECLOC			31013
/** @brief �߸��� ������ ������ ��ġ����
*/
#define ERROR_SN3DWG_HEADER_BAD_SENTINEL		31014
/** @brief �߸��� ���� ������
*/
#define ERROR_SN3DWG_HEADER_BAD_FILESIZE		31015
/** @brief �߸��� R18 ����
*/
#define ERROR_SN3DWG_HEADER_BAD_R18FILEID		31016
/** @brief �������� ���������� ���� �޸� �Ҵ� ����
*/
#define ERROR_SN3DWG_HEADER_MALLOC_FAILURE		31017

/** @brief �߸��� R18 ���� �� ���
*/
#define ERROR_SN3DWG_R18_BAD_SECTMAP			31021
/** @brief �߸��� R18 ���� ���� ���
*/
#define ERROR_SN3DWG_R18_BAD_SECTINFO			31022
/** @brief �߸��� R18 NumSectDesc ����
*/
#define ERROR_SN3DWG_R18_BAD_SECTDESC			31023
/** @brief ���� �޸� �Ҵ� ����
*/
#define ERROR_SN3DWG_SECT_MALLOC_FAILURE		31024
/** @brief Deprecated
*/
#define ERROR_SN3DWG_R18_BAD_NORMSECT			31025
/** @brief R18 ���� �̸��� ã�� ����
*/
#define ERROR_SN3DWG_R18_NO_SECTNAME			31026
/** @brief R18 ���� ���۸� ã�� ����
*/
#define ERROR_SN3DWG_R18_NO_SECTBUF				31027
/** @brief R18�� �߸��� ���� ������
*/
#define ERROR_SN3DWG_R18_DECOMP_FAILURE			31028
/** @brief �߸��� R18 Summary Info
*/
#define ERROR_SN3DWG_R18_BAD_SUMMARY			31029

/** @brief �߸��� CRC
*/
#define ERROR_SN3DWG_BAD_CRC					31030

/** @brief �߸��� DWG R1315 Object
*/
#define ERROR_SN3DWG_BAD_OBJECTS				31031

/** @brief �߸��� DWG R1315 Object
*/
#define ERROR_SN3DWG_BAD_OBJECT_SIZE			31032


/** @brief �߸��� DWG R2004 ���ǵ�����
*/
#define ERROR_SN3DWG_BAD_SECTION			31034

// DOCX ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief ���� ������ ������ ���� SN3MFI ���� ����
*/
#define ERROR_SN3DOCX_CANNOT_OPEN_UNZIPFILE	46001
/** @brief DOCX ���Ϸκ��� ���� ������ ���� ���� ����
*/
#define ERROR_SN3DOCX_CANNOT_ARCHIVE_ZIP	46002
/** @brief DOCX ���Ϸκ��� ���� ������ XML���� �Ľ̽� ���� �߻�
*/
#define ERROR_SN3DOCX_CANNOT_PARSE_XML		46003
/** @brief DOCX ���� ������ ��ũ�� ���͸� ����
*/
#define ERROR_SN3DOCX_CANNOT_OVBA_MACRO_PARSE  46004

// DOC ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief FIB ������ �д� ���� ���� �߻�
*/
#define	ERROR_SN3DOC_FILTER_FS_FIB_READ_FAILURE		30101
/** @brief �������� �ʴ� Word ����
*/
#define	ERROR_SN3DOC_FILTER_FS_BAD_WORD_VERSION		30102
/** @brief ��ȣȭ�� DOC ����
*/
#define ERROR_SN3DOC_FILTER_FS_FILE_ENCRYPTED		30103
/** @brief DOC ���� ���͸� �� �޸� �Ҵ� ����
*/
#define ERROR_SN3DOC_FILTER_MALLOC_FAILURE		30104


// CHM ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief CHM ������ ���� SN3MFI ���� ����
*/
#define ERROR_SN3CHM_CANNOT_OPEN_CHMFILE			31304

/** @brief malloc fail
*/
#define ERROR_SN3CHM_FILTER_MALLOC_FAILURE					31323

// ZIP ERROR /////////////////////////////////////////////////////////////////////////////
/** @brief 
*/
#define	ERROR_SN3ZIP_FILTER_M_INVALID_COMPRESSED_LENGTH	35005 
/** @brief ZIP ���� ���� �� SN3MFI�� NULL 
*/
#define	ERROR_SN3ZIP_FOPEN_M_NULL_MFI			35011 
/** @brief SN3MFI�� ���� ������ ���� �б� ���� 
*/
#define	ERROR_SN3ZIP_FOPEN_M_FREAD_FAILURE		35012
/** @brief SN3ZIP_FILE ����ü�� ���� �޸� �Ҵ� ���� 
*/
#define	ERROR_SN3ZIP_FOPEN_M_MALLOC_ZFILE_FAILURE	35013
/** @brief ZIP ���Ͽ� ZIP ���� �ñ״���(0x02014b50)�� ���� 
*/
#define	ERROR_SN3ZIP_FOPEN_M_INVALID_SIGNATURE		35014 
/** @brief ZIP ���Ͽ� ZIP ���� �ñ״���(0x02014b50)�� ���� 
*/
#define	ERROR_SN3ZIP_FOPEN_M_MALLOC_FILENAME_FAILURE	35015 
/** @brief ZIP �����̸��� ���� �޸� �Ҵ� ���� 
*/
#define	ERROR_SN3ZIP_FOPEN_M_MALLOC_EXTRAFIELD_FAILURE	35016 
/** @brief ZIP ���� ó�� �� ������ ���� ������ 
*/
#define	ERROR_SN3ZIP_FOPEN_M_END_OF_FILELIST		35017 

/** @brief ZIP ���� �ݱ� �� SN3ZIP_FILE�� NULL 
*/
#define	ERROR_SN3ZIP_FCLOSE_NULL_ZFILE			35021 

/** @brief �������� �ʴ� ��������(ZIP ���� ����� STORED Ȥ�� DEFLATED �� �ƴ�)
*/
#define	ERROR_SN3ZIP_UNZIP_M_NOT_SUPPORTED_COMPRESSION		35031 
/** @brief ZIP ���������� ���� �޸� �Ҵ� ����
*/
#define	ERROR_SN3ZIP_UNZIP_M_UNCOMPRESSED_MALLOC_FAILURE	35032 
/** @brief STORED ������ ZIP ������ SN3MFI�κ��� �б� ����
*/
#define	ERROR_SN3ZIP_UNZIP_M_STORED_DATA_FREAD_FAILURE		35033 
/** @brief STORED ������ ZIP ������ SN3MFI�� ���� ����
*/
#define	ERROR_SN3ZIP_UNZIP_M_STORED_DATA_FWRITE_FAILURE		35034 
/** @brief DEFLATED ������ ZIP ������ SN3MFI�� ���� ����
*/
#define	ERROR_SN3ZIP_UNZIP_M_DEFLATED_DATA_ZWRITE_FAILURE	35037 
/** @brief DEFLATED ������ ZIP ������ SN3MFI�� ���� ����
*/
#define	ERROR_SN3ZIP_UNZIP_M_GZIP_ZCLOSE_FAILURE		35038 
/** @brief
*/
#define	ERROR_SN3ZIP_UNZIP_M_IMPOSSIBLE_PATH_FLOW		35039 
/** @brief ���� ZIP ���� 
*/
#define	ERROR_SN3ZIP_FOPEN_M_BROKEN_ZIP_FILE			35040 

/** @brief zip ��ȣȭ�� ���
*/
#define ERROR_SN3ZIP_FILTER_FS_FILE_ENCRYPTED		35042  // by lightbell 2009.01.07

/** @brief ZIP ���� ���� �ش� ������ ����
*/
#define ERROR_SN3ZIP_FILE_NOT_FOUND				35051 

/** @brief ZIP ������ central directory signature�� ã�� ����
*/
#define ERROR_SN3ZIP_NOT_FOUND_END_SIG			35061 

/** @brief ZIP ������ uncompress size �� 0 �� ���
*/
#define ERROR_SN3ZIP_UNCOMPRESS_SIZE_ZERO		35071
/** @brief ZIP ���� ������ ���� ����
*/
#define ERROR_SN3ZIP_UNZIP_STRM_ERROR			35072
/** @brief ZIP ���� ������ �޸� �Ҵ� ����
*/
#define ERROR_SN3ZIP_MEMORY_ALLOC_FAILURE			35073

/** @bried archive fileinfo ���� ����
*/
#define ERROR_SN3ARFILIST_INIT_FAILED			36001
/** @bried archive fileinfo �߸��� ����
 */
#define ERROR_SN3ARFILIST_NULL_LIST				36002
/** @bried archive fileinfo �߸��� ����
 */
#define ERROR_SN3ARFILIST_WRONG_IDX				36003

// SN3FMT ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief ��ȣȭ�� office 2007 ����  
*/
#define ERROR_SN3FMT_ENCRYPT_OFFICE	44001 
/** @brief �޸� �Ҵ� ����
*/
#define ERROR_SN3FMT_MEMORY_ALLOC_FAILURE	44100 

// XLSX ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief ���� ������ ������ ���� SN3MFI ���� ����
*/
#define ERROR_SN3XLSX_CANNOT_OPEN_UNZIPFILE	45001 
/** @brief XLSX ���Ϸκ��� ���� ������ ���� ���� ����
*/
#define ERROR_SN3XLSX_CANNOT_ARCHIVE_ZIP	45002 
/** @brief XLSX ���Ϸκ��� ���� ������ XML���� �Ľ̽� ���� �߻�
*/
#define ERROR_SN3XLSX_CANNOT_PARSE_XML		45003 

/** @brief XLSX �ؽ�Ʈ ��� ���۰� NULL
*/
#define ERROR_SN3XLSX_OUTPUT_BUFFER_NULL	45004 

/** @brief XLSX �޸� ����
*/
#define ERROR_SN3XLSX_MEMORY_ALLOC_FAILURE	45005


// XLS ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief ��ȣȭ�� XLS ����  
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

/** @brief TAR ���� ���� Ư�� ���� ũ�Ⱑ 512 �̸���
*/
#define	ERROR_SN3TAR_FILTER_M_INVALID_BLOCK_SIZE	33601 
/** @brief TAR ���� �� �޸� �Ҵ� ����
*/
#define	ERROR_SN3TAR_MEMORY_ALLOC_FAILURE			33602


// SXX ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief OpenOffice ���� ���͸� �� XML �Ľ� ����
*/
#define ERROR_SN3SXX_CANNOT_PARSE_XML		34001 

/** @brief OpenOffice ���� ������ SN3MFI�� ���� ����
*/
#define ERROR_SN3SXX_CANNOT_OPEN_UNZIPFILE	34011 
/** @brief OpenOffice ���� ���� �� Ư�� xml ������ ã�� ���� 
*/
#define ERROR_SN3SXX_CANNOT_ARCHIVE_ZIP		34012 

/** @brief ���� ������ OpenOffice ������ �ƴ� 
*/
#define ERROR_SN3SXX_IS_NOT_SXX_FILE		34021

/** @brief ��ȣȭ�� OpenOffice ���� �Դϴ�.
*/
#define ERROR_SN3SXX_IS_ENCRYPTED_FILE		34023


// SWF ERROR /////////////////////////////////////////////////////////////////////////////


/** @brief �߸��� SWF ����(���� �� Ư�� ������ ����) 
*/
#define ERROR_SN3SWF_LOAD_FILENOT_SWF			31701 
/** @brief �� �� ���� SWF ���� ����
*/
#define ERROR_SN3SWF_LOAD_VERSION_UNKNOWN		31702 
/** @brief ���͸��� ���� �޸� �Ҵ� ����
*/
#define ERROR_SN3SWF_LOAD_MALLOC_FAILURE		31703 
/** @brief �߸��� SWF ����(������ ���̰� ���� ����� Ʋ��)
*/
#define ERROR_SN3SWF_LOAD_BAD_FILESIZE			31704 

// SN3SUM ERROR //////////////////////////////////////////////////////////////////////////

/** @brief SN3SUM ����ü�� ���� �޸� �Ҵ� ����
*/
#define	ERROR_SN3SUM_INIT_MEMORY_ALLOCATION_FAILURE		40201 
/** @brief SN3SUM ����ü �޸� ���� �� SN3SUM�� NULL
*/
#define	ERROR_SN3SUM_FREE_SUMMARY_IS_NULL				40202 
/** @brief SN3SUM ������ ���� ���� FILE ���� ����
*/
#define	ERROR_SN3SUM_UNLOAD_FILE_OPEN_FAILURE			40203 

/** @brief MS Office 2007 ������ ���� ���� �б� �� ���� ������ SN3MFI�� ���� ����
*/
#define ERROR_SN3SUM_CANNOT_OPEN_UNZIPFILE	40301 
/** @brief MS Office 2007 ���� ���� �� �������� XML ������ ����
*/
#define ERROR_SN3SUM_CANNOT_ARCHIVE_ZIP	40302 
/** @brief MS Office 2007 �������� XML �Ľ� ����
*/
#define ERROR_SN3SUM_CANNOT_PARSE_XML		40303 

/** @brief SN3SUM �����Ͱ� NULL�� ��� (snf_sum_init�ʿ�)
*/
#define ERROR_SN3SUM_IS_NULL	40304 


// Format NDOC ERROR /////////////////////////////////////////////////////////////////////////// 
/** @brief	Encrypt�� NDOC ������ ��������� Decrypt�� �� ���°��
*/
#define ERROR_NDOC_CANNOT_DECRYPT_HEADER	61001

// RTF ERROR /////////////////////////////////////////////////////////////////////////////

/** @brief RTF Mark-up ���� '}'�� �߸� ��
*/      
#define ERROR_SN3RTF_FILTER_M_STACK_UNDERFLOW    30701 
/** @brief RTF Mark-up ���� '{'�� '}' ���� ����
*/      
#define ERROR_SN3RTF_FILTER_M_STACK_OVERFLOW     30702 
/** @brief RTF ���� ���͸� �� RTF Mark-up ���� '}'���� ������ �������� ������
*/      
#define ERROR_SN3RTF_FILTER_M_UNMATCHED_BRACE    30703 
/** @brief RTF ���� �� �߸��� 16���� ���ڿ��� ����
*/      
#define ERROR_SN3RTF_FILTER_M_INVALID_HEX        30704 
/** @brief RTF ���� �� �߸��� ������ ����*/      
#define ERROR_SN3RTF_FILTER_M_BAD_TABLE          30705 
/** @brief RTF ���� �Ľ� ����
*/      
#define ERROR_SN3RTF_FILTER_M_ASSERTION_FAILURE  30706 
/** @brief RTF ���� �Ľ� �� ������ ���� ������
*/      
#define ERROR_SN3RTF_FILTER_M_END_OF_FILE        30707 


// PPTX ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief ���� ������ ������ ���� SN3MFI ���� ����
*/
#define ERROR_SN3PPTX_CANNOT_OPEN_UNZIPFILE	47001 
/** @brief DOCX ���Ϸκ��� ���� ������ ���� ���� ����
*/
#define ERROR_SN3PPTX_CANNOT_ARCHIVE_ZIP	47002 
/** @brief PPTX ���Ϸκ��� ���� ������ XML���� �Ľ̽� ���� �߻�
*/
#define ERROR_SN3PPTX_CANNOT_PARSE_XML		47003
/** @brief PPTX ó�� �� xml parser �ʱ�ȭ ����
*/
#define ERROR_SN3PPTX_FAILED_TO_INIT_XML_PARSER		47004
/** @brief PPTX ó�� �� �޸� �Ҵ� ����
*/
#define ERROR_SN3PPTX_MEMORY_ALLOC_FAILURE		47005
//////////////////////////////////////////////////////////////////////////////////////////


// XPS ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief ���� ������ ������ ���� SN3MFI ���� ����
*/
#define ERROR_SN3XPS_CANNOT_OPEN_UNZIPFILE	48001 
/** @brief XPS ���Ϸκ��� ���� ������ ���� ���� ����
*/
#define ERROR_SN3XPS_CANNOT_ARCHIVE_ZIP		48002 
/** @brief XPS ���Ϸκ��� ���� ������ XML���� �Ľ̽� ���� �߻�
*/
#define ERROR_SN3XPS_CANNOT_PARSE_XML		48003 
/** @brief XPS �� Document �б� ����
 */
#define ERROR_SN3XPS_CANNOT_OPEN_DOCUMENT	48004

//////////////////////////////////////////////////////////////////////////////////////////


// PPT ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief	PPT�� ��ȣȭ�� ��� 
*/
#define ERROR_SN3PPT_FILTER_FS_FILE_ENCRYPTED	50000 

/** @brief  �߸��� Atom�� �����ϴ� ��� ���� �߻�
*/
#define ERROR_SN3PPT_FOUND_BAD_ATOM				50001 

/** @brief  �߸��� Offset ���� �����ϴ� ���
*/
#define ERROR_SN3PPT_INVALID_OFFSET				50002 
/** @brief �߸��� slidelist ����
*/
#define ERROR_SN3PPT_FOUND_BAD_SLIDE_LIST	50003 
/** @brief �߸��� ���丮 ��Ʈ��
*/
#define ERROR_SN3PPT_FOUND_BAD_DIR_ENTRY	50004
/** @brief �߸��� Offset
*/
#define ERROR_SN3PPT_FOUND_BAD_OFFSET		50005
/** @brief �޸� �Ҵ� ����
*/
#define ERROR_SN3PPT_MEMORY_ALLOC_FAILURE	50006
/** @brief �߸��� ��� Ÿ��
*/
#define ERROR_SN3PPT_INVALID_HEADER_TYPE	50007
/** @brief �߸��� ��� ����
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
/** @brief �߸��� ���ڵ� ���
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
/** @brief ���Ͽ��� ����
*/
#define ERROR_SN3ALZ_CANT_OPEN_FILE				58003	
/** @brief 
*/
#define ERROR_SN3ALZ_CANT_OPEN_DEST_FILE			58004	
/** @brief ���� ���� ����
*/
#define ERROR_SN3ALZ_CORRUPTED_FILE				58005	
/** @brief ALZIP �� �ƴ�.
*/
#define ERROR_SN3ALZ_NOT_ALZ_FILE					58006	
/** @brief alz signature �б� ����
*/
#define ERROR_SN3ALZ_CANT_READ_SIG				58007	
/** @brief alz ����� ���� �� ����
*/
#define ERROR_SN3ALZ_CANT_READ_FILE				58008
/** @brief alz ����� ���� �� ���� ���
*/
#define ERROR_SN3ALZ_AT_READ_HEADER				58009
/** @brief alz �߸��� ���� �̸� ����
*/
#define ERROR_SN3ALZ_INVALID_FILENAME_LENGTH		58010
/** @brief alz ������� ���丮�� ���� �� ����
*/
#define ERROR_SN3ALZ_CANT_READ_CENTRAL_DIRECTORY_STRUCTURE_HEAD	58012

/** @brief alz �޸� �Ҵ� ����
*/
#define ERROR_SN3ALZ_MEM_ALLOC_FAILED				58017
/** @brief alz BZIP2 �Ľ� ����
*/
#define ERROR_SN3ALZ_BZIP2_FAILED					58020
/** @brief alz Ǯ�� ���� ������
*/
#define ERROR_SN3ALZ_UNKNOWN_COMPRESSION_METHOD	58022

/** @brief alz ���������� ����� ���� �� ����
*/
#define ERROR_SN3ALZ_CANT_READ_LOCAL_FILE_HEAD	58031

/** @brief alz ��ȣȭ�� ���
*/
#define ERROR_SN3ALZ_FILTER_FS_FILE_ENCRYPTED		58032  

//////////////////////////////////////////////////////////////////////////////////////////

// OLE10NATIVE ERROR  ///////////////////////////////////////////////////////////////////////////
/** @brief signature OLE������ �ƴ�
*/
#define ERROR_SN3OLE10NATIVE_NOT_OLE 59001
/** @brief signature native stream�� �б� ����
*/
#define ERROR_SN3OLE10NATIVE_STREAM_READ_FAIL 59002
/** @brief signature �޸𸮰� ������� ���Ͽ� native stream �б� ����
*/
#define ERROR_SN3OLE10NATIVE_NOT_ENOUGH_MEM 59003

/** @brief OLENATIVE10 ���� Native Data Block Read ����	
*/
#define ERROR_SN3OLE10NATIVE_UNKNOWN	59004

/** @brief OLENATIVE10 ���� Native Data Filtering Fail
*/
#define ERROR_SN3OLE10NATIVE_FILTER_FAIL	59005



//////////////////////////////////////////////////////////////////////////////////////////


//////////////////////////////////////////////////////////////////////////////////////////

// WPD ERROR  ///////////////////////////////////////////////////////////////////////////

/** @brief WPD ���� ��� �б� ����
*/
#define ERROR_SN3WPD_FAIL_READ_HEADER 62000
/** @brief
*/
#define ERROR_SN3WPD_BAD_PAIR_FUNC_DOC 62001
/** @brief WPD ���� ���� üũ�� ����
*/
#define ERROR_SN3WPD_INVALID_HEADER_VERSION 62003
/** @brief WPD ������ �ƴ� ���
*/
#define ERROR_SN3WPD_NOT_DOCUMENT_TYPE 62004

//////////////////////////////////////////////////////////////////////////////////////////


//////////////////////////////////////////////////////////////////////////////////////////

// 7ZIP ERROR  ///////////////////////////////////////////////////////////////////////////

/** @brief GENERAL ERROR
*/
#define ERROR_SN3SEVENZIP_GENERAL						61002	
/** @brief ���Ͽ��� ����
*/
#define ERROR_SN3SEVENZIP_CANT_OPEN_FILE				61003	
/** @brief Deprecated
*/
#define ERROR_SN3SEVENZIP_CANT_OPEN_DEST_FILE			61004	
/** @brief ���� ���� ����
*/
#define ERROR_SN3SEVENZIP_CORRUPTED_FILE				61005	
/** @brief signature �б� ����
*/
#define ERROR_SN3SEVENZIP_CANT_READ_SIG					61006
/** @brief
*/
#define ERROR_SN3SEVENZIP_UNKNOWN_COMPRESSION_METHOD	61008

/** @brief sevenzip ��ȣȭ�� ���
*/
#define ERROR_SN3SEVENZIP_FILTER_FS_FILE_ENCRYPTED		61009  

/** @brief ���� ������ CRC ������ �߻��� ���
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
/** @brief LZMA2 �������� ������ �Ǿ��ִ� ���
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
/** @brief ���Ͽ��� ����
*/
#define ERROR_SN3RAR_CANT_OPEN_FILE				71003	
/** @brief Deprecated
*/
#define ERROR_SN3RAR_CANT_OPEN_DEST_FILE			71004	
/** @brief ���� ���� ����
*/
#define ERROR_SN3RAR_CORRUPTED_FILE				71005	
/** @brief signature �б� ����
*/
#define ERROR_SN3RAR_CANT_READ_SIG					71006
/** @brief Deprecated
*/
#define ERROR_SN3RAR_CANT_READ_FILE				71007
/** @brief Deprecated
*/
#define ERROR_SN3RAR_UNKNOWN_COMPRESSION_METHOD	71008

/** @brief rar ��ȣȭ�� ���
*/
#define ERROR_SN3RAR_FILTER_FS_FILE_ENCRYPTED		71009

/** @brief ���� ������ CRC ������ �߻��� ���
*/
#define ERROR_SN3RAR_FILTER_BAD_CRC				71010
/** @brief ���� �Ӽ� �б� ����
*/
#define ERROR_SN3RAR_FAIL							71021
/** @brief �޸� �Ҵ� ����
*/
#define ERROR_SN3RAR_MEM_ALLOC_FAILED			71028


//////////////////////////////////////////////////////////////////////////////////////////

// MDB ERROR  ///////////////////////////////////////////////////////////////////////////

/** @brief ���͸� �� ��ȣ�� ������ �����ΰ��
*/
#define ERROR_SN3MDB_FILTER_M_PASSWORD_EXISTS		63001

/** @brief ���͸� �� MDB������ ���̺��� �������
*/
#define ERROR_SN3MDB_FILTER_M_BROKEN_TABLE			63002

/** @brief ���͸� �� MDB������ ���̺� ������ ���� �� ���°��
*/
#define ERROR_SN3MDB_FILTER_M_READ_TABLE			63003

/** @brief �������� �ʴ� JET DB�ΰ��
*/
#define ERROR_SN3MDB_FOPEN_M_UNKNOWN_JET_VERSION	63004

/** @brief MDB�� ���ڵ尡 ���������� ���� ���
*/
#define	ERROR_SN3MDB_FILTER_M_INVALID_RECORD		63005

/** @brief MDB������ signature�� �ν��� �� ���� ���
*/
#define	ERROR_SN3MDB_FOPEN_M_INVALID_SIGNATURE		63006

/** @brief MDB������ ���� ������ �б� ����
*/
#define ERROR_SN3MDB_READ_NEXT_PAGE					63007
/** @brief MDB���� ���͸��� ���� �޸� �Ҵ� ����
*/
#define ERROR_SN3MDB_MEMORY_ALLOC_FAILURE					63007
//////////////////////////////////////////////////////////////////////////////////////////

// OLE_CONTENTS ERROR  ///////////////////////////////////////////////////////////////////////////
/** @brief signature OLE������ �ƴ�
*/
#define ERROR_SN3OLE_CONTENTS_NOT_OLE 72001

/** @brief signature MFI �� OLE���Ͽ� MOUNT �� �� ����
*/
#define ERROR_SN3OLE_CONTENTS_MOUNT 72002

/** @brief signature OLE���� stream open ����
*/
#define ERROR_SN3OLE_CONTENTS_STREAM_OPEN 72003

/** @brief signature OLE���� stream size check ����
*/
#define ERROR_SN3OLE_CONTENTS_STREAM_SIZE 72004
/////////////////////////////////////////////////////////////////////////////////////////
/** @brief ������ ���� �ƴ����� �� �� ���� ������ ������ �б� ����
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
/** @brief cumpressBuffer �� ù��° ����Ʈ�� 0x01 �� �ƴ� ���
*/
#define ERROR_COMPRESS_CURRENT_INVALID_HEADER 84001
//////////////////////////////////////////////////////////////////////////////////////////

/** @brief XML �Ľ� ����
*/
#define ERROR_SN3XML_STATUS								64001
/** @brief XML �ش� ������Ʈ ����
*/
#define ERROR_SN3XML_NO_ELEMENTS                        64002

// PST ERROR  ///////////////////////////////////////////////////////////////////////////

/** @brief PST ���� ����� dwMagic �� Ʋ�� ���
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
/** @reief ����� 2G �̻��� ��� ����
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
/** @brief PST �޸� Malloc/Realloc ����
 */
#define ERROR_SN3PST_MEMORY_ALLOC_FAILURE 		89202


// SN3XML ERROR  ///////////////////////////////////////////////////////////////////////////

// IWORK ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief xml ������ ���� ���� �Ҵ� ����
*/
#define ERROR_SN3IWORK_NO_MEMMORY			90001 
/** @brief buffer�� xml���� �б� ����
*/
#define ERROR_SN3IWORK_CANNOT_READ_FILE	90002 
/** @brief xml DomTree ���� ����
*/
#define ERROR_SN3IWORK_CANNOT_PARSE_TREE	90003 
/** @brief iwork2013/4 �߸��� header
*/
#define ERROR_SN3IWORK2K_INVAILD_HEADER	90010
/** @brief iwork2013/4  Decode error
*/
#define ERROR_SN3IWORK2K_DECODE_ERROR		90011
/** @brief iwork2013/4 �߸��� MessageInfo stream
*/
#define ERROR_SN3IWORK2K_INVALID_MESSAGE_INFO		90012
/** @brief �߸��� iwork2013 ����
*/
#define ERROR_SN3IWORK2013_INVALID_FILE		90013
//////////////////////////////////////////////////////////////////////////////////////////

// KEYNOTE ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief ���� ������ ������ ���� SN3MFI ���� ����
*/
#define ERROR_SN3KEYNOTE_CANNOT_OPEN_UNZIPFILE	91001 
/** @brief KEYNOTE ���Ϸκ��� ���� ������ ���� ���� ����
*/
#define ERROR_SN3KEYNOTE_CANNOT_ARCHIVE_ZIP		91002 
/** @brief KEYNOTE ���Ϸκ��� ���� ������ XML���� �Ľ̽� ���� �߻�
*/
#define ERROR_SN3KEYNOTE_CANNOT_PARSE_XML		91003 
/** @brief xml ������ ���� ���� �Ҵ� ����
*/
#define ERROR_SN3KEYNOTE_NO_MEMMORY				91004

//////////////////////////////////////////////////////////////////////////////////////////

// PAGES ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief ���� ������ ������ ���� SN3MFI ���� ����
*/
#define ERROR_SN3PAGES_CANNOT_OPEN_UNZIPFILE	92001 
/** @brief PAGES ���Ϸκ��� ���� ������ ���� ���� ����
*/
#define ERROR_SN3PAGES_CANNOT_ARCHIVE_ZIP		92002 
/** @brief PAGES ���Ϸκ��� ���� ������ XML���� �Ľ̽� ���� �߻�
*/
#define ERROR_SN3PAGES_CANNOT_PARSE_XML			92003 
/** @brief xml ������ ���� ���� �Ҵ� ����
*/
#define ERROR_SN3PAGES_NO_MEMMORY				92004

//////////////////////////////////////////////////////////////////////////////////////////

// NUMBERS ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief ���� ������ ������ ���� SN3MFI ���� ����
*/
#define ERROR_SN3NUMBERS_CANNOT_OPEN_UNZIPFILE	93001 
/** @brief NUMBERS ���Ϸκ��� ���� ������ ���� ���� ����
*/
#define ERROR_SN3NUMBERS_CANNOT_ARCHIVE_ZIP		93002 
/** @brief NUMBERS ���Ϸκ��� ���� ������ XML���� �Ľ̽� ���� �߻�
*/
#define ERROR_SN3NUMBERS_CANNOT_PARSE_XML		93003 
/** @brief xml ������ ���� ���� �Ҵ� ����
*/
#define ERROR_SN3NUMBERS_NO_MEMMORY				93004

//////////////////////////////////////////////////////////////////////////////////////////

// DRM ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief DRM ������ �������� �ʽ��ϴ�.
*/
#define ERROR_SN3FMT_DRM_DOCUMENT				94001

//////////////////////////////////////////////////////////////////////////////////////////

// KEYNOTE ERROR ////////////////////////////////////////////////////////////////////////////

/** @brief ���� ������ ������ ���� SN3MFI ���� ����
*/
#define ERROR_SN3HWPX_CANNOT_OPEN_UNZIPFILE	95001 
/** @brief HWPX ���Ϸκ��� ���� ������ ���� ���� ����
*/
#define ERROR_SN3HWPX_CANNOT_ARCHIVE_ZIP		95002 
/** @brief HWPX ���Ϸκ��� ���� ������ XML���� �Ľ̽� ���� �߻�
*/
#define ERROR_SN3HWPX_CANNOT_PARSE_XML		95003 
/** @brief HWPX ó�� �� xml parser �ʱ�ȭ ����
*/
#define ERROR_SN3HWPX_FAILED_TO_INIT_XML_PARSER		95004
 
//////////////////////////////////////////////////////////////////////////////////////////

// XLSB ERROR ////////////////////////////////////////////////////////////////////////////
/** @brief XLSB �޸� �Ҵ� ����
*/
#define ERROR_SN3XLSB_MEMORY_ALLOC_FAILURE	96001
//////////////////////////////////////////////////////////////////////////////////////////

// DICOM ERROR ////////////////////////////////////////////////////////////////////////////
/** @brief 
*/
#define ERROR_SN3DICOM_QA_PARSE_FAILURE	98000
//////////////////////////////////////////////////////////////////////////////////////////

// COMMON ERROR ////////////////////////////////////////////////////////////////////////////
/** @brief ���� �������� �������� ����
*/
#define ERROR_NOT_SUPPORTED_IN_CURRENT_VERSION		97000

/**************************************************************
 * Function Declarations
 **************************************************************/
/***************************************************************/

/***************************************************************/
