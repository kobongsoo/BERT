import os
import random
import numpy as np
from typing import Dict, List, Optional
import re

#---------------------------------------------------------------
# 입력 text에서 pattern이 아닌 문자들을 제거하는 함수
# - in: text : 입력 텍스트 1개  예: '오늘은^^ 날씨가 좋다~~'
# - in: pattern : 포함시킬 re 패턴 예: r'[^ㄱ-ㅎㅏ-ㅣ가-힣]'
# - out: 패턴이 아닌 문자들 제거된 텍스트 1개 예: '오늘은 날씨가 좋다'
#---------------------------------------------------------------
def clean_text(text:str, pattern=r'[^\w\sㄱ-ㅎㅏ-ㅣ가-힣(){}\[\]%,."\']+'):
    regex_pattern = pattern # 포함시킬 패턴 (영문, 숫자, 한글, (),{},[],%,,,",') 이외는 제거
    cleaned_text = re.sub(regex_pattern, '', text)     # 패턴이 아니면 공백''으로 처리
    return cleaned_text