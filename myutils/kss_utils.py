import os
import random
import numpy as np
from typing import Dict, List, Optional
import kss
from myutils import clean_text
from tqdm import tqdm
#---------------------------------------------------------------
# 입력 문단들(1차원리스트) 를 문장으로 분리해서 2차원 리스트를 리턴함함. 
# - in: paragraphs : 입력 문단 리스트 (예: ['오늘은^^ 날씨가 좋다~~','오늘은 비가 온다', '오늘은 춥다'])
# - in: sentences_split_num : 문장 최대 분리할 계수 (예: 10=>최대 10개 문장만 사용)
# - in: paragraphs_num : 문단 글자 최대 계수 (예: 999 => 최대 999개 글자까지만 사용)
# - out: 분리된 문장들 목록 (2차원 리스트) (예: [['오늘은 날씨가 좋다','날씨가 좋다','비가온다'],[...],[...]])
#---------------------------------------------------------------
def split_sentences(paragraphs:list, 
                    sentences_split_num:int=10, 
                    paragraphs_num:int = 999,
                    debug:bool=False):
    
    result = []
    
    split_num = sentences_split_num
    paragraphs_num = paragraphs_num
    
    for idx, paragraph in enumerate(tqdm(paragraphs)):  

        if debug == True:
            if idx % 100 == 0 or idx == 0:
                print(f'idx:{idx}, {paragraph[:paragraphs_num]}\n')
            
        clean_context = clean_text(paragraph)  # 전처리 : (한글, 숫자, 영문, (), {}, [], %, ,,.,",')  등을 제외한 특수문자 제거
        
        # 입력 문단 길이가 999개 크면, 속도가 느려지므로 최대 999개 까지만 문자 입력 받음.
        if len(clean_context) > paragraphs_num:
            #print(f'paragraph_len:{len(paragraph)}')
            clean_context = clean_context[0:paragraphs_num]

            
        #sentences = [sentence for sentence in clean_context.split('.') if sentence != '' and len(sentence) > 10]  # '.'(마침표) 로 구분해서 sub 문장을 만듬.
        #sentences = [sentence for sentence in kss.split_sentences(clean_context) if sentence != '' and len(sentence) > 10] # kss 이용해서 sub 문장을 만듬
        
        # 최대 10개 문장만 추출함.
        sentences = []
        count = 0
        for sentence in kss.split_sentences(clean_context):
            if sentence != '' and len(sentence) > 10:
                sentences.append(sentence)
                if count > split_num:
                    break

        # 만약 sentences(sub 문장) 가 하나도 없으면 원본문장을 담고, 10이상이면  10개만 담음.
        result.append([clean_context] if len(sentences) < 1 else sentences[0:split_num] if len(sentences) > split_num else sentences)

    return result