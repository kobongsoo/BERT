import os
import random
import numpy as np
import torch
import torch.nn as nn
import logging
import warnings
from tqdm.notebook import tqdm
from torch import Tensor

#from sentence_transformers import SentenceTransformer
#from sentence_transformers import models

#------------------------------------------------------------------------------------------------------------------------------
# 임력된 문단을 510 토큰 단위로 나누고, 100단위로 슬라이딩 윈도우 하면서 나눈 문단을 1차원 배열로 출력
# -in : tokenizer : tokenizer
# -in : paragraph : 임력 문단 => str 형식으로 입력 (예: '독도 해역 헬기 추락사고가 발생한 지 열하루가 지났지만 실종자 추가 발견 소식은 들려오지 않고 있다')
# -in : window_size : 나눌 토큰 수 (예: 10=토큰 10개 단위로 문장을 나눔)
# -in : sliding_size : 슬라이딩 토큰 수 ( 예: 5 이면 5씩 이전문장 포함해서 문장 나눔 : 반드시 windows_size보다는 작아야 함)
# -out : 한 문단에 대한 슬라이딩 처리한 문장리스트(1차원) 예: ['독도 해역 헬기 추락사고가 발생한 지 열',  # '가 발생한 지 열하루가 지났지만 실종자', ...,]
#------------------------------------------------------------------------------------------------------------------------------
def sliding_window_tokenizer(tokenizer, paragraph:str, window_size:int=510, sliding_size:int=100):

    step_size = window_size - sliding_size    

    assert paragraph != None, f'error!! paragraphs is None' 
    assert window_size > sliding_size, f'error!! window_size({window_size}) < sliding_size({sliding_size})' 
    
    tokens = tokenizer.tokenize(paragraph)
    
    # text가 '독도 해역 헬기 추락사고가 발생한 지 열하루가 지났지만 실종자 추가 발견 소식은 들려오지 않고 있다' 일때
    # 토큰별로 분리하고 아래처럼 2차원 토큰 배열로 출력됨
    # [['독도', '해역', '헬기', '추락', '##사고', '##가', '발생', '##한', '지', '열'], 
    # ['##가', '발생', '##한', '지', '열', '##하루', '##가', '지났', '##지만', '실종자'], 
    # ['##하루', '##가', '지났', '##지만', '실종자', '추가', '발견', '소식', '##은', '들려오'], 
    # ['추가', '발견', '소식', '##은', '들려오', '##지', '않', '##고', '있', '##다'], 
    # ['##지', '않', '##고', '있', '##다']]

    newtokens = []
    for i in range(0, len(tokens), step_size):
        if i + window_size <= len(tokens):
            newtokens.append(tokens[i:i+window_size])
        else:
            newtokens.append(tokens[i:])

    #print(newtokens)

    # 위 2차원 배열 토큰들을 합쳐서 문장으로 만듬.
    # 이때 각 토큰(token)에 대해, ##로 시작하는 경우 ##를 제거하고 new_lst에 추가
    # 첫 번째 토큰인 경우, token을 그대로 new_lst에 추가
    # 첫 번째 토큰이 아닌 경우 , new_lst의 마지막 요소와 token 사이에 띄어쓰기(" ")를 추가하여 new_lst에 추가

    # ['독도 해역 헬기 추락사고가 발생한 지 열', 
    # '가 발생한 지 열하루가 지났지만 실종자', 
    # '하루가 지났지만 실종자 추가 발견 소식은 들려오', 
    # '추가 발견 소식은 들려오지 않고 있다', 
    # '지 않고 있다']

    result = []
    for lst in newtokens:
        new_lst = []
        for token in lst:
            if token.startswith("##"): # 각 토큰(token)에 대해, ##로 시작하는 경우 ##를 제거하고 new_lst에 추가
                new_lst.append(token[2:])
            else:
                if len(new_lst) == 0:  # new_lst가 비어 있는 경우(첫 번째 토큰인 경우), token을 그대로 new_lst에 추가
                    new_lst.append(token)
                else:
                    new_lst.append(" " + token) # 첫 번째 토큰이 아닌 경우 , new_lst의 마지막 요소와 token 사이에 띄어쓰기(" ")를 추가하여 new_lst에 추가
        result.append("".join(new_lst))

    return result


# main    
if __name__ == '__main__':
    main()

    