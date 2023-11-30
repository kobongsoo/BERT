from typing import Any, Callable, overload
from pympower.classes.snf import *
from pympower.classes.snf_define import *

class SNFError(Exception):
    '''
    native 에러 정보

    다음과 같이 정보를 조회한다.
    error_func, error_code = e.args

    이 때, error_code는 snf_error_code_to_status_code 함수를 사용해 StatusCode 값으로 변환할 수 있다.
    '''


def snf_gbl_setcfg(license_key: str, file_type: SN3FILETYPE, option: SN3OPTION, base_buffer_size: int) -> None:
    '''
    license_key: 생략.
    file_type: 텍스트를 추출할 파일 유형 설정
    option: 텍스트 추출 옵션
    '''


def snf_gbl_setcfgEx(license_key: str, file_type: SN3FILETYPE, option: SN3OPTION, base_buffer_size: int, opt: Any) -> None:
    '''
    license_key: 생략.
    file_type: 텍스트를 추출할 파일 유형 설정
    option: 텍스트 추출 옵션
    opt: 생략.
    '''


def snf_fmt_detect(path: str) -> int:
    '''
    path: 파일 경로
    '''


def snf_fmt_format_name(format: int) -> str:
    '''
    format: snf_fmt_detect 함수가 반환한 값
    '''


def snf_fmt_formatNameByCode(format: int) -> str:
    '''
    format: snf_fmt_detect 함수가 반환한 값
    '''

def snf_fmt_isFilterFormat(path:str) -> bool:
    '''
    필터링을 지원하는 포맷인지 확인한다.
    윈도우에서 유니코드를 지원하지 않는다.
    '''

def snf_error_code_to_status_code(snf_error_code:SN3ERROR) -> int:
    '''
    리턴 값은 StatusCode이다. StatusCode로 변환하기 위해서 다음과 같이 사용한다.
    status_code = snf_error_code_to_status_code(error_code)
    statusCode = StatusCode(status_code)
    '''

class SN3MFI:
    def fopen(self, path: str) -> None: ...
    def fclose(self) -> None: ...

    def unload(self, path: str) -> None:
        '''
        MFI 파일을 로컬에 파일로 저장한다.
        fopen(path)을 호출한 후에 바로 unload()를 호출하면 파일을 복사하는 것과 동일하다.

        SN3BUF.filter의 콜백 함수에서 압축 파일 내 DRM 파일을 로컬에 저장한 후,
        DRM을 복호화 하고 다시 파일을 검사하는 용도로 사용한다.
        '''

    def fmt_detect(self) -> int:
        '''
        파일 포맷 유형을 리턴
        '''

class SN3MARKER:
    state:SN3BUF_STATE_TYPE
    marker:str
    unzipMFI:SN3MFI
    depth:int
    ret:int

class SN3BUF:
    def __init__(self, callback_chunk_size:int):
        '''
        콜백을 호출할 텍스트 추출 크기.

        예를 들어 4096글자를 추출할 때 마다 콜백이 호출되게 하려면 다음과 같이 사용한다.

        >>> SN3BUF(callback_chunk_size=4096)
        '''

    def isempty(self) -> bool:
        '''
        버퍼가 비어있는지 확인
        '''

    def size(self) -> int:
        '''
        버퍼에 들어있는 텍스트 크기를 반환한다.

        set_user_func을 통해 등록한 콜백에서 이 함수를 호출하는 경우
        추출할 파일의 모든 텍스트 크기가 아닌 지금 버퍼에 들어있는 용량만을 반환한다.
        '''

    @overload
    def get_text(self) -> str:
        '''
        버퍼에서 추출한 텍스트를 가져온다.
        '''

    @overload
    def get_text(self, size:int) -> str:
        '''
        버퍼에서 추출한 텍스트를 size만큼 가져온다.
        '''

    def set_user_func(self, user_func:Callable) -> None:
        '''
        텍스트 추출 콜백 함수 등록
        --
        이 함수를 이용해 콜백 함수를 등록한 후에 filter 또는 filter_m 함수를 호출하면
        1글자 추출할 때 마다 등록한 콜백 함수를 호출한다.
        '''

    def set_user_data(self, user_data:Any) -> None:
        '''
        set_user_func함수를 통해 등록한 콜백 함수가 호출될 때 전달할 인자 값을 설정한다.
        '''

    def set_user_command(self, user_command:int) -> None:
        '''
        텍스트 추출 중, 콜백 함수에서 SN3_USER_STOP를 설정하면 텍스트 추출을 중지할 수 있다.
        '''

    def set_marker_func(self, marker_func:Callable) -> None:
        '''
        압축 파일, 메일 첨부 파일등 파일에 포함된 파일을 추출 시작하거나, 끝날 때 마다
        호출할 콜백을 설정한다.

        콜백 함수의 원형은 다음과 같다.

        def marker_callback(buf:BUF, marker_data:Any, marker:MARKER): ...
        '''

    def set_marker_data(self, marker_data:Any) -> None:
        '''
        set_marker_func가 호출될 때 함께 전달할 인자 값
        '''

    def set_skip_command(self, skip_command:SN3BUF_SKIP_TYPE):
        '''
        스킵
        '''

    @overload
    def filter(self, path:str):
        '''
        경로 이름을 인자 값으로 받아 텍스트를 추출한다.

        set_user_func 메소드를 통해 콜백 함수를 등록한 경우 콜백 함수가 호출된다.
        '''

    @overload
    def filter(self, path:str, with_page:bool):
        '''
        with_page
        '''

    @overload
    def filter_m(self, mfi:SN3MFI):
        '''
        filter와 동일한 함수이나 문자열 경로 대신, MFI를 인자 값으로 받는다.
        filter_m을 호출하기전, MFI.fopen을 호출해야 한다.

        set_user_func 메소드를 통해 콜백 함수를 등록한 경우 콜백 함수가 호출된다.

        snf C언어 API는 wchar_t *를 인자 값으로 받는 wsnf_buf_wfilter함수를 제공하지 않는다.

        대신에 wsnf_mfi_wfopen이라는 wchar_t *를 사용할 수 있는 MFI 함수가 있어,
        C언어에서는 wsnf_buf_filter 대신, wsnf_buf_filter_m을 사용한다.

        하지만 Python 버전에는 filter만 호출해도 내부적으로 MFI.fopen을 이용해 filter_m을
        호출하기 때문에 그냥 filter 함수만 사용해도 무방하다.
        '''

    @overload
    def filter_m(self, mfi:SN3MFI, with_page:bool):
        '''
        with_page
        '''
