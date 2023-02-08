import os
import random
import numpy as np
import torch
import logging
import warnings
from tqdm.notebook import tqdm

from sentence_transformers import SentenceTransformer
from sentence_transformers import models
#from sentence_transformers.cross_encoder import CrossEncoder

#------------------------------------------------------------------------------------------------------------------------------
# 입력 문장을 '.' 기준으로 여러 문장으로 나누고, 임베딩을 구한후 평균 embed vector 를 리턴하는 함수
# => IN : model=모델 인스턴스, contexts=text 리스트, dimension=임베딩차원(기본:768), return_tensor=True 이면 tensor값으로 임베딩벡터생성됨.
#------------------------------------------------------------------------------------------------------------------------------
def embed_text_avg(model, contexts, dimension:int=768, return_tensor=False):
    avg_paragraph_vec = np.zeros((1,dimension))
    
    # 2차원 문장 배열로 만든다.
    sentences = [sentence for sentence in contexts.split('.') if sentence != '' and len(sentence) > 20]
    #print(sentences)
    
    # 한꺼번에 문장 배열을 임베딩 처리함
    #avg_paragraph_vecs = embed_text(sentences)
    avg_paragraph_vecs = embed_text(model=model, contexts=sentences, return_tensor=False)
    
    #print(type(avg_paragraph_vecs))
    #print(avg_paragraph_vecs.shape)
    
    # 배열로 만든 후 평균을 구함.
    arr = np.array(avg_paragraph_vecs)
    avg_paragraph_vec = arr.mean(axis=0)
    return avg_paragraph_vec.ravel(order='C') # 1차원 배열로 변경

#------------------------------------------------------------------------------------------------------------------------------
# 입력 text(리스트)에 대한 embed vector 생성 후 배열로 리턴함
# => IN : model=모델 인스턴스, contexts=text 리스트, return_tensor=True 이면 tensor값으로 임베딩벡터생성됨.
#------------------------------------------------------------------------------------------------------------------------------
def embed_text(model, contexts, return_tensor=False):
    vectors =  model.encode(contexts, convert_to_tensor=return_tensor)
    return np.array([embedding for embedding in vectors]).astype("float32")#float32 로 embeddings 타입 변경

#------------------------------------------------------------------------------------------------------------------------------
# bi_encoer 모델 불러오기
# => IN: model_path=모델경로, max_seq_len=최대토큰계수, do_lower_case=true이면 영어일때 소문자로 변환
#        pooling_mode=임베딩 벡터 폴링 모드 선택 (*아래값중 문자열로 입력함, 기본=mean)
#        ['mean', 'max', 'cls', 'weightedmean', 'lasttoken'] (mean=단어 평균, max=최대값, cls=문장) 
#------------------------------------------------------------------------------------------------------------------------------
def bi_encoder(model_path: str=None, max_seq_len: int=512, do_lower_case: bool=True, pooling_mode: str = 'mean'):
    
    assert model_path is not None, f"Input model_path cannot be None"
    word_embedding_model = models.Transformer(model_path, max_seq_length=max_seq_len, do_lower_case=do_lower_case, tokenizer_name_or_path=model_path)     
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(), pooling_mode=pooling_mode)  
    bi_encoder = SentenceTransformer(modules=[word_embedding_model, pooling_model])
    
    return bi_encoder
