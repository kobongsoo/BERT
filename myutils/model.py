import os
import random
import numpy as np
import torch
import torch.nn as nn
import logging
import warnings
from tqdm.notebook import tqdm
from torch import Tensor

from sentence_transformers import SentenceTransformer
from sentence_transformers import models
#from sentence_transformers.cross_encoder import CrossEncoder

#------------------------------------------------------------------------------------------------------------------------------
# 문장을 .(마침표)로 여러 문장으로 나누고 나눈문장을 1개씩 임베딩 구한후 계수만큼 나워서 평균 임베딩 구하기
# => 속도 느림, 최대 10개만 함.(CPU 환경에서는 좋음)
#------------------------------------------------------------------------------------------------------------------------------
def embed_text_avg2(model, paragraph:list, dimension:int=768, return_tensor=False):
    avg_paragraph_vec = np.zeros((1,dimension))
    sent_count = 0
    
    # ** kss로 분할할때 히브리어: מר, 기타 이상한 특수문자 있으면 에러남. 
    # 따라서 여기서는 그냥 . 기준으로 문장을 나누고 평균을 구함
    # 하나의 문장을 읽어와서 .기준으로 나눈다.
    #for sent in kss.split_sentences(paragraph):
    sentences = [sentence for sentence in paragraph.split('. ') if sentence != '' and len(sentence) > 20]

    for sentence in sentences:
        # 문장으로 나누고, 해당 vector들의 평균을 구함.
        #avg_paragraph_vec += embed_text([sent])
        avg_paragraph_vec += embed_text(model=model, paragraph=[sentence], return_tensor=return_tensor)
        sent_count += 1
  
        # 최대 10개 문장만 처리함 
        if sent_count >= 10:
            break
            
    # 0으로 나누면 배열이 nan(not a number)가 되어 버리므로, 반드시 0>큰지 확인해야 함
    if sent_count > 0:
        avg_paragraph_vec /= sent_count
    
    return avg_paragraph_vec.ravel(order='C') # 1차원 배열로 변경
            
#------------------------------------------------------------------------------------------------------------------------------
# 입력 문장을 '.' 기준으로 여러 문장으로 나누고, 임베딩을 구한후 평균 embed vector 를 리턴하는 함수
# - in : model=bi_encoder 모델 인스턴스
# - in : paragraphs=1차원 리스트 예: ['오늘 날씨가 너무 좋다']
# - in : dimension=임베딩차원(기본:768), return_tensor=True 이면 tensor값으로 임베딩벡터생성됨.
# - out : 문단을 나눈 문장들에 대한 평균 => 1차원 배렬 예: (768)
#------------------------------------------------------------------------------------------------------------------------------
def embed_text_avg(model, paragraph:list, dimension:int=768, return_tensor=False):
    avg_paragraph_vec = np.zeros((1,dimension))
    
    # 2차원 문장 배열로 만든다.
    sentences = [sentence for sentence in paragraph.split('.') if sentence != '' and len(sentence) > 20]
    #print(sentences)
    
    # 문장이 10보다 크면 10개 까지만 처리함.
    #if len(sentences) > 10:
    #    sentences = sentences[0:10]
    #elif len(sentences) < 1:
    #    sentences = paragraph
    
    if len(sentences) < 1:
         sentences = paragraph
            
    # 한꺼번에 문장 배열을 임베딩 처리함
    #avg_paragraph_vecs = embed_text(sentences)
    avg_paragraph_vecs = embed_text(model=model, paragraphs=sentences, return_tensor=return_tensor)
    
    #print(type(avg_paragraph_vecs))
    #print(avg_paragraph_vecs.shape)
    
    # 배열로 만든 후 평균을 구함.
    arr = np.array(avg_paragraph_vecs)
    avg_paragraph_vec = arr.mean(axis=0)
    return avg_paragraph_vec.ravel(order='C') # 1차원 배열로 변경

#------------------------------------------------------------------------------------------------------------------------------
# 입력 text(리스트)에 대한 embed vector 생성 후 배열로 리턴함
# - in : model=모델 인스턴스
# - in : paragraphs=1차원 text 리스트 예: ['오늘 날씨가 너무 좋다','내일은 비가 온다']
# - in : return_tensor=True 이면 tensor값으로 임베딩벡터생성됨.
# - in : token_embeddings=출력을 어떻게 할지 False=>'sentence embeddings'->768 문장 임베딩 값, True=> token_embeddings=>토큰별 임베딩값
# - in : normalize : True=임베딩 정규화 화면 출력벡터이 길이가 1이 된다.
# - out : token_embeddings=True 일때=>토큰별 embedding 으로 출력함=> list[tensor(250,768), tensor(243,768), tensor(111,768),..] tensor 리스트 타입으로 리턴됨.
#         token_embeddings=False 일때 =>1개의 embedding으로 출력함=> array[768, 768, 768,...] float32 array 타입으로 리턴함.
#------------------------------------------------------------------------------------------------------------------------------
def embed_text(model, paragraphs:list, token_embeddings=False, return_tensor=False, normalize=True):
    
    if token_embeddings == True:  # contexts를 토큰별 embedding 으로 출력함.
        output_value = 'token_embeddings'
    else:                         # contexts를 1개의 embedding으로 출력=
        output_value = 'sentence_embedding'
        
    vectors =  model.encode(paragraphs, output_value=output_value, convert_to_tensor=return_tensor, normalize_embeddings=normalize)
    
    if token_embeddings == True:
        # [tensor(250,768), tensor(243,768), tensor(111,768),..] tensor 리스트 타입으로 리턴됨. 
        #따라서 tenosor.cpu().numpy()로 numpy로 변경해서 연산해야함.
        return vectors
    else:
        return np.array([embedding for embedding in vectors]).astype("float32")#float32 로 embeddings 타입 변경 =>numpy 타입으로 리턴됨

    
#------------------------------------------------------------------------------------------------------------------------------
# sbert.net에 Dense 함수를 이용하여 768 차원을 줄여서 128 차원 벡터 만드는 함수
# -in : embed_tensor : 원본 2차원 tensor 배열 (예:tensor(27, 768) )
# -in : out_features : 줄일 차원 숫자 
# -out : 차원 변경된 tensor 배열 (예:tensor(27,128))
#------------------------------------------------------------------------------------------------------------------------------
def dense_model(embed_tensor, out_f:int=128, weight:Tensor=None , bias:Tensor=None, debug=False, idd:int=0):
    
    if debug == True:
        print(f'[dense_model]embed_tensor:{embed_tensor.size()}')
        print(f'[dense_model]embed_tensor-----------------------------------------------')
        print(f'{embed_tensor}')
        print(f'[dense_model]embed_tensor0:{embed_tensor.shape[0]}')
        print(f'[dense_model]embed_tensor1:{embed_tensor.shape[1]}')
        print()
        print(f'[dense_model]out_features:{out_f}')
        print(f'[dense_model]weight:{weight.size()}')
        print(f'[dense_model]bias:{bias.size()}')
        print(f'[dense_model]idd:{idd}')
        
        
    in_f = embed_tensor.shape[1]
    
    assert in_f > 0, f"in_features is bed"
    assert out_f > 0, f"out_features is bed"
    
    # Dense 모델 정의하기
    dmodel = models.Dense(in_features=in_f, out_features=out_f, bias=False, init_weight=weight, init_bias=bias, activation_function=nn.Tanh())  
    #state_dict = torch.load(os.path.join(model_path, 'pytorch_model.bin'))
    #dmodel.load_state_dict(state_dict, map_location=torch.device('cpu'))
    #dense_model.load(model)
    
    # dict로 변경 하고 입력
    embed_dict = {"sentence_embedding":embed_tensor.cpu()}
    dense_embed = dmodel(embed_dict)
    
    return dense_embed['sentence_embedding']
    
    
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
