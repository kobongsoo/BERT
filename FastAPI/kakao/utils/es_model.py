import torch
import torch.nn as nn
import time
import os
import numpy as np
from tqdm.notebook import tqdm
from sentence_transformers import SentenceTransformer
from sentence_transformers import models

#------------------------------------------------------------------------------------------------------------------------------
# bi_encoer 모델 불러오기
# - in: model_path=모델경로, max_seq_len=최대토큰계수, do_lower_case=true이면 영어일때 소문자로 변환
# - in: pooling_mode=임베딩 벡터 폴링 모드 선택 (*아래값중 문자열로 입력함, 기본=mean) ['mean', 'max', 'cls', 'weightedmean', 'lasttoken'] (mean=단어 평균, max=최대값, cls=문장) 
# - in: out_dimension=출력 임베딩 크기 지정 (0=기본 모델 embedding 사이즈, 0>=해당 임베딩 크기로 줄임)
# - out : Word 임베딩 모델, bi_encoder 모델
#------------------------------------------------------------------------------------------------------------------------------
def bi_encoder(model_path:str=None, max_seq_len:int=512, do_lower_case:bool=True, pooling_mode:str = 'mean', out_dimension:int = 0, device:str='cpu'):
    
    assert model_path is not None, f"Input model_path cannot be None"
   
    # word 임베딩 모델 설정
    word_embedding_model = models.Transformer(model_path, max_seq_length=max_seq_len, do_lower_case=do_lower_case, tokenizer_name_or_path=model_path)     
    
    # 폴링 모델 설정
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(), pooling_mode=pooling_mode)  
    
    # out_dimenison이 설정된 경우에는 Dense layer 추가함
    if out_dimension > 0:
        dense_model = models.Dense(in_features=pooling_model.get_sentence_embedding_dimension(), # 입력 dimension은 앞에 pooling모델 embedding dimension으로 지정
                               out_features=out_dimension,     # 출력 dimension
                               activation_function=nn.Tanh())  # activation function은 Tahn으로 정의
        
    # out_dimension이 설정된 경우
    if out_dimension > 0:
        bi_encoder = SentenceTransformer(modules=[word_embedding_model, pooling_model, dense_model], device=device)
    else:       
        bi_encoder = SentenceTransformer(modules=[word_embedding_model, pooling_model], device=device)
    
    return word_embedding_model, bi_encoder

# main    
if __name__ == '__main__':
    main()