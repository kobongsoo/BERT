import os
import random
import numpy as np
from typing import Dict, List, Optional
import kss
#from kss import split_sentences
from .re_utils import clean_text, is_language
from tqdm import tqdm
#---------------------------------------------------------------
# 입력 문단들(1차원리스트) 를 문장으로 분리해서 2차원 리스트를 리턴함함. 
#  => kss로 분리 후 줄바꿈('\n')으로 문장 분리함.(문장이 길수록 kss로 분리하는것은 시간이 오래 걸림=>따라서 split_sentences1 사용 권장함)
#
# - in: paragraphs : 입력 문단 1차원 리스트  (예: ['오늘은^^ 날씨가 좋다~~.날씨가 좋다. 비가온다','오늘은 눈이 온다', '오늘은 춥다'])
# - in: sentences_split_num : 문장 최대 분리할 계수 (예: 10=>최대 10개 문장만 사용)
# - in: paragraphs_num : 문단 글자 최대 계수 (예: 999 => 최대 999개 글자까지만 사용)
# - in: remove_line : true=줄바꿈('\r', '\n' 등을 제거)
# - in: remove_sentence_len : 문장 길이가 10보다 작으면 제거 (예: 15=>한문장이 길이가 15보다 짧으면 추가 안함)
# - in: remove_duplication : 중복된 문장은 제거(true=중복된 문장은 1나만 추가됨)
# - in: check_en_ko : 한국어 혹은 영어 문장인지 체크(true=한국어 혹은 영어문장인지 체크) => **프로그래밍 문장은 제거용으로 사용)
# - out: 분리된 문장들 목록 (2차원 리스트) (예: [['오늘은 날씨가 좋다','날씨가 좋다','비가온다'],[...],[...]])
#---------------------------------------------------------------
def split_sentences(paragraphs:list, 
                    sentences_split_num:int=10, 
                    paragraphs_num:int = 999,
                    remove_line:bool=True,
                    remove_sentence_len:int = 10,
                    remove_duplication:bool=False,
                    check_en_ko:bool=False,
                    showprogressbar:bool=False,
                    debug:bool=False)-> List[str]:
    
    result = []
    
    split_num = sentences_split_num
    paragraphs_num = paragraphs_num
    remove_len = remove_sentence_len
    
    if showprogressbar == True:
        paragraphs = tqdm(paragraphs)
    
    for idx, paragraph in enumerate(paragraphs):  

            if debug == True:
                if idx % 100 == 0 or idx == 0:
                    print(f'idx:{idx}, {paragraph[:paragraphs_num]}\n')

            if remove_line == True:
                paragraph = paragraph.replace('\n', ' ').replace('\r', ' ') # 줄바꿈 제거 
                
            clean_context = clean_text(paragraph)  # 전처리 : (한글, 숫자, 영문, (), {}, [], %, ,,.,",')  등을 제외한 특수문자 제거
        
            # 입력 문단 길이가 999개 크면, 속도가 느려지므로 최대 999개 까지만 문자 입력 받음.
            if len(clean_context) > paragraphs_num:
                #print(f'paragraph_len:{len(paragraph)}')
                clean_context = clean_context[0:paragraphs_num]


            #sentences = [sentence for sentence in clean_context.split('.') if sentence != '' and len(sentence) > 10]  # '.'(마침표) 로 구분해서 sub 문장을 만듬.
            #sentences = [sentence for sentence in kss.split_sentences(clean_context) if sentence != '' and len(sentence) > 10] # kss 이용해서 sub 문장을 만듬

            # 최대 n개 문장만 추출함.
            sentences = []
            count = 0
            for sentence in kss.split_sentences(clean_context):
                # 줄바꿈 있으면 줄바꿈을 한문장으로 출력
                subsentences = sentence.split('\n')
                for subsentence in subsentences:
                    
                    pattern = r'^\d+(\.\d+)*'  # 문장 맨앞에 '4.1.2.3' 패턴 제거,  r'^\d+(\.\d+)*\s+' # 문장 맨앞에 '4.1.2.3띄어쓰기' 있는 패턴 제거
                    subsentence = clean_text(text=subsentence, pattern=pattern)

                    pattern = r'^\d+\.'  # 문장 맨 앞에 '4.' 패턴 제거
                    subsentence = clean_text(text=subsentence, pattern=pattern)

                    pattern = r'^\d+\)'  # 문장 맨 앞에 '4)' 패턴 제거
                    subsentence = clean_text(text=subsentence, pattern=pattern)
                
                    # 한국어 혹은 영어문장인지 체크
                    if check_en_ko == True:
                        check = is_language(subsentence)
                    else:
                        check = True
                            
                    if check == True:
       
                        if subsentence != '' and len(subsentence) > remove_len:
            
                            if remove_duplication == True: # 문장 중복 제거 
                                if subsentence not in sentences:
                                    sentences.append(subsentence)
                                    count += 1
                                    if count > split_num:
                                        break
                            else: # 문장 중복제거 안함
                                sentences.append(subsentence)
                                count += 1
                                if count > split_num:
                                    break

            # 만약 sentences(sub 문장) 가 하나도 없으면 원본문장을 담고, n개이상이면  n개만 담음.
            result.append([clean_context] if len(sentences) < 1 else sentences[0:split_num] if len(sentences) > split_num else sentences)

    return result


#---------------------------------------------------------------
# 입력 문단들(1차원리스트) 를 문장으로 분리해서 2차원 리스트를 리턴함함. 
#  => 줄바꿈('\n')으로 문장 분리 후 -> kss로 분리 함. (이때 짧은 문장은 kss 분리하지 않음=>kss 분리하면 공백이 제거되므로.)
#
# - in: paragraphs : 입력 문단 1차원 리스트  (예: ['오늘은^^ 날씨가 좋다~~.날씨가 좋다. 비가온다','오늘은 눈이 온다', '오늘은 춥다'])
# - in: sentences_split_num : 문장 최대 분리할 계수 (예: 10=>최대 10개 문장만 사용)
# - in: paragraphs_num : 문단 글자 최대 계수 (예: 999 => 최대 999개 글자까지만 사용)
# - in: remove_line : true=줄바꿈('\r', '\n' 등을 제거)
# - in: remove_sentence_len : 문장 길이가 10보다 작으면 제거 (예: 15=>한문장이 길이가 15보다 짧으면 추가 안함)
# - in: remove_duplication : 중복된 문장은 제거(true=중복된 문장은 1나만 추가됨)
# - in: check_en_ko : 한국어 혹은 영어 문장인지 체크(true=한국어 혹은 영어문장인지 체크) => **프로그래밍 문장은 제거용으로 사용)
# - out: 분리된 문장들 목록 (2차원 리스트) (예: [['오늘은 날씨가 좋다','날씨가 좋다','비가온다'],[...],[...]])
#---------------------------------------------------------------
def split_sentences1(paragraphs:list, 
                    sentences_split_num:int=10, 
                    paragraphs_num:int = 999,
                    remove_line:bool=True,
                    remove_sentence_len:int = 10,
                    remove_duplication:bool=False,
                    check_en_ko:bool=False,
                    showprogressbar:bool=False,
                    debug:bool=False)-> List[str]:
    
    result = []
    
    split_num = sentences_split_num
    paragraphs_num = paragraphs_num
    remove_len = remove_sentence_len
    
    if showprogressbar == True:
        paragraphs = tqdm(paragraphs)
    
    for idx, paragraph in enumerate(paragraphs):  

            if debug == True:
                if idx % 100 == 0 or idx == 0:
                    print(f'idx:{idx}, {paragraph[:paragraphs_num]}\n')

            if remove_line == True:
                paragraph = paragraph.replace('\n', ' ').replace('\r', ' ') # 줄바꿈 제거 
                
            clean_context = clean_text(paragraph)  # 전처리 : (한글, 숫자, 영문, (), {}, [], %, ,,.,",')  등을 제외한 특수문자 제거
        
            # 입력 문단 길이가 999개 크면, 속도가 느려지므로 최대 999개 까지만 문자 입력 받음.
            if len(clean_context) > paragraphs_num:
                #print(f'paragraph_len:{len(paragraph)}')
                clean_context = clean_context[0:paragraphs_num]

            #sentences = [sentence for sentence in clean_context.split('.') if sentence != '' and len(sentence) > 10]  # '.'(마침표) 로 구분해서 sub 문장을 만듬.
            #sentences = [sentence for sentence in kss.split_sentences(clean_context) if sentence != '' and len(sentence) > 10] # kss 이용해서 sub 문장을 만듬

            # 최대 n개 문장만 추출함.
            sentences = []
            count = 0
            for ccontext in clean_context.split('\n'):
                
                if len(ccontext) > remove_len+5:
                    subsentences = kss.split_sentences(ccontext)
                    #print(subsentences)
                else:
                    subsentences = [ccontext]
                      
                for subsentence in subsentences:
                    pattern = r'^\d+(\.\d+)*'  # 문장 맨앞에 '4.1.2.3' 패턴 제거,  r'^\d+(\.\d+)*\s+' # 문장 맨앞에 '4.1.2.3띄어쓰기' 있는 패턴 제거
                    subsentence = clean_text(text=subsentence, pattern=pattern)

                    pattern = r'^\d+\.'  # 문장 맨 앞에 '4.' 패턴 제거
                    subsentence = clean_text(text=subsentence, pattern=pattern)

                    pattern = r'^\d+\)'  # 문장 맨 앞에 '4)' 패턴 제거
                    subsentence = clean_text(text=subsentence, pattern=pattern)

                    # 한국어 혹은 영어문장인지 체크
                    if check_en_ko == True:
                        check = is_language(subsentence)
                    else:
                        check = True

                    if check == True:

                        #print(f'[{len(subsentence)}]:{subsentence}')
                        if subsentence != '' and len(subsentence) > remove_len:

                            if remove_duplication == True: # 문장 중복 제거 
                                if subsentence not in sentences:
                                    sentences.append(subsentence)
                                    count += 1
                                    if count > split_num:
                                        break
                            else: # 문장 중복제거 안함
                                sentences.append(subsentence)
                                count += 1
                                if count > split_num:
                                    break

            # 만약 sentences(sub 문장) 가 하나도 없으면 원본문장을 담고, n개이상이면  n개만 담음.
            result.append([clean_context] if len(sentences) < 1 else sentences[0:split_num] if len(sentences) > split_num else sentences)

    return result