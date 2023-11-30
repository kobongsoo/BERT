from pympower.classes.snf_define import *
from pympower.common.statuscode import StatusCode
import pympower_ext._snf as _snf
from pympower_ext._snf import *

# snf_gbl_setcfg를 호출하지 않으면 텍스트 추출 자체가 안된다.
# 때문에 처음 import될 때 기본 값으로 초기화 하고, 필요한 경우 다시 초기화한다.
_snf.snf_gbl_setcfg(
	None,
     SN3FILETYPE.ALL
    # SN3FILETYPE.MP3
    # | SN3FILETYPE.ZIP
    # | SN3FILETYPE.TAR
    # | SN3FILETYPE.GZ
    # | SN3FILETYPE.TXT
    # | SN3FILETYPE.RTF
    # | SN3FILETYPE.HTM
    # | SN3FILETYPE.XML
    # | SN3FILETYPE.MHT
    # | SN3FILETYPE.PDF
    # | SN3FILETYPE.HWD
    # | SN3FILETYPE.DOC
    # | SN3FILETYPE.PPT
    # | SN3FILETYPE.XLS
    # | SN3FILETYPE.H2K
    # | SN3FILETYPE.HWP3
    # | SN3FILETYPE.CHM
    # | SN3FILETYPE.DWG
    # | SN3FILETYPE.SXW
    # | SN3FILETYPE.SXC
    # | SN3FILETYPE.SXI
    # | SN3FILETYPE.MDI
    # | SN3FILETYPE.MSG
    # | SN3FILETYPE.DOCX
    # | SN3FILETYPE.XLSX
    # | SN3FILETYPE.PPTX
    # | SN3FILETYPE.SWF
    # | SN3FILETYPE.JTD
    # | SN3FILETYPE.WPD
    # | SN3FILETYPE.BZIP
    # | SN3FILETYPE.ALZIP
    # | SN3FILETYPE.OLE10NATIVE
    # | SN3FILETYPE.HWX
    # | SN3FILETYPE.HWN
    # | SN3FILETYPE.OFFICE_XML
    # | SN3FILETYPE.HWP_HML
    # | SN3FILETYPE._7Z
    # | SN3FILETYPE.NDOC
    # | SN3FILETYPE.MDB
    # | SN3FILETYPE.RAR
    # | SN3FILETYPE.OLE_CONTENTS
    # | SN3FILETYPE.DGN
    # | SN3FILETYPE.OVBA
    # | SN3FILETYPE.DCM
    # | SN3FILETYPE.NPPT
    # | SN3FILETYPE.NXLS
    # | SN3FILETYPE.PST
    # | SN3FILETYPE.KEYNOTE
    # | SN3FILETYPE.PAGES
    # | SN3FILETYPE.NUMBERS
    # | SN3FILETYPE.SHOW
    # | SN3FILETYPE.NXL
    # | SN3FILETYPE.CELL
    # | SN3FILETYPE.BAT
    # | SN3FILETYPE.XPS
    # | SN3FILETYPE.HWPX
    # | SN3FILETYPE.KEYNOTE13
    # | SN3FILETYPE.PAGES13
    # | SN3FILETYPE.NUMBERS13
    # | SN3FILETYPE.XLSB
    ,
	# 콜백 함수에서 오류가 발생한 경우 사이냅에서 Exception을 핸들링해
	# 덤프를 뜨거나 하는 작업을 할 수 없다.
	# 해당 Exception 핸들링을 제거하는 옵션으로 필수 옵션이다.
	SN3OPTION.DONT_USE_EXCEPTION_HANDLING
	# 압축 파일도 해제하는 옵션
	| SN3OPTION.ARCHIVE_EXTRACT
	# 확장자를 확인하지 않고 필터링 하는 옵션
	| SN3OPTION.EXTENSION_NO_CHECK
	# 엑셀 파일은 기본적으로 1,000,000개 셀만 추출하고 이를 넘어가면
	# 40400오류를 리턴하는데 이 기능을 끄는 옵션
	| SN3OPTION.EXCEL_NOLIMIT
    # 엑셀 구분자 출력
    | SN3OPTION.EXCEL_SEPARATE
	# 연속된 공백이 있는 경우 공백은 기본적으로 1개로 줄어드는데
	# 이 옵션을 제거
	| SN3OPTION.NO_USE_SPACE_REMOVER
	# 오피스 문서 내부의 첨부 파일도 추출하는 옵션
    # OLE문서의 경우 포맷 타입을 알 수 없기 때문에
    # 타입별로 전처리를 하는 방식을 사용할 수 없어 추출하지 않는다.
	#| SN3OPTION.EMBEDED_OLE_FILTER
	# 엑셀 구분자 출력
	| SN3OPTION.EXCEL_SEPARATE
	# 빈 셀도 엑셀 구분자 출력
	#| SN3OPTION.EXCEL_SEPARATE_EMPTY_CELL
	# 페이지 번호 출력
	| SN3OPTION.WITHPAGE
	| SN3OPTION.WITHPAGE_SHEETNAME
    | SN3OPTION.NO_WITHPAGE
	# 메일 첨부파일도 필터링
	| SN3OPTION.MAIL_ATTACH_FILTER
    # PDF 좌표순 출력 옵션
    #| SN3OPTION.PDF_COORD_BASED_OUTPUT
    ,
	512 * 1024
)

__all__ = [
    'SNFError',
	'snf_gbl_setcfg',
	'snf_gbl_setcfgEx',
    'snf_fmt_detect',
    'snf_fmt_format_name',
    'snf_fmt_format_name',
    'snf_fmt_formatNameByCode',
    'snf_fmt_isFilterFormat',
    'snf_error_code_to_status_code',
	'SN3MFI',
	'SN3MARKER',
	'SN3BUF',
	'SN3SUM',
]
