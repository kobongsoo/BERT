import os
import random
import numpy as np
from typing import Dict, List, Optional
import re

#---------------------------------------------------------------
# 입력 text가 한국어, 영어 문장인지 확인
# - in: text : 입력 텍스트 1개  예: 'hellow world'
# - out: true=한국어혹은 영어 문장, false=한국어 혹은 영어문장 아님.
#---------------------------------------------------------------
def is_language(text) -> bool:
    if has_korean(text) == True:
        return True
    else:
        if en_language(text) == True:
            return True
        
    return False
#---------------------------------------------------------------
# 입력 text가 영어 문장인지 확인
# - in: text : 입력 텍스트 1개  예: 'hellow world'
# - out: true=영어 문장, false=영어문장 아님.
#---------------------------------------------------------------
def en_language(text) -> bool:
    # 영어 문장 패턴
    english_pattern = r'^[A-Za-z0-9\s\.\'\",:;?!]+$'
    # 입력된 문자열이 영어 문장인지 확인
    if re.match(english_pattern, text):
        return True
    return False

#---------------------------------------------------------------
# 입력 text에 한국어가 있는지 확인하는 함수
# - in: text : 입력 텍스트 1개  예: '오늘은^^ 날씨가 좋다~~'
# - out: true=한국어 문장, false=한국어문장이 아님.
#---------------------------------------------------------------
def has_korean(text) -> bool:
    for char in text:
        if '가' <= char <= '힣':
            return True
    return False

#---------------------------------------------------------------
# 입력 text에서 pattern이 아닌 문자들을 제거하는 함수
# - in: text : 입력 텍스트 1개  예: '오늘은^^ 날씨가 좋다~~'
# - in: pattern : 포함시킬 re 패턴 예: r'[^ㄱ-ㅎㅏ-ㅣ가-힣]'
# - out: 패턴이 아닌 문자들 제거된 텍스트 1개 예: '오늘은 날씨가 좋다'
#---------------------------------------------------------------
def clean_text(text:str, pattern=r'[^\w\sㄱ-ㅎㅏ-ㅣ가-힣(){}\[\]%,."\']+')->str:
    
    regex_pattern = pattern # 포함시킬 패턴 (영문, 숫자, 한글, (),{},[],%,,,",') 이외는 제거
    cleaned_text = re.sub(regex_pattern, '', text)     # 패턴이 아니면 공백''으로 처리
    
    # 이 φιλεῖν 단어가 들어가면 kss 에러뜸. 이유 모름. 따라서 이 단어는 제거함.
    # => 제거할 단어들은 remove_text 배열에 추가하면 됨.
    remove_text = ['φιλεῖν', 'σοφία']
    for word in remove_text:  
        cleaned_text = cleaned_text.replace(word, '')
        
    return cleaned_text