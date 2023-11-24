import torch
import time
import os
import numpy as np
from tqdm.notebook import tqdm
import asyncio
import numpy as np

from sentence_transformers import models
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from typing import Dict, List, Optional
from sklearn.cluster import KMeans
from sklearn_extra.cluster import KMedoids

from .es_model import bi_encoder
from .sklearn_utils import clustering_embedding, kmedoids_clustering_embedding

#---------------------------------------------------------------------------
# ES 인덱스 생성
# -in : es : ElasticSearch 객체.
# -in : index_file_path: 인덱스 파일명
# -in : index_name: 인덱스명
# -in : create : 기존에 동일한 인덱스는 삭제하고 다시 생성.
#---------------------------------------------------------------------------
def create_index(es, index_file_path:str, index_name:str, create:bool = True):
    
    assert es is not None, f'error!!=>es is None'
    assert index_file_path is not None, f'error!!=>index_file_path is None'
    assert index_name is not None, f'error!!=>index_name is None'
        
    if create == True or not es.indices.exists(index_name):
        es.indices.delete(index=index_name, ignore=[404])
        count = 0
        
        # 인덱스 생성
        with open(index_file_path) as index_file:
            source = index_file.read().strip()
            count += 1
            print(f'{count}:{source}') # 인덱스 구조 출력
            es.indices.create(index=index_name, body=source)
            
        print(f'new create index=>index_file:{index_file_path}, index_name:{index_name}')
#---------------------------------------------------------------------------
     
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
    
#---------------------------------------------------------------------------
# 엠파워 문서 인덱스 batch 처리
# - in: ES 객체
# - in: docs=인덱스 처리할 data
# - in : index_name = 인덱스명
# - in: vector_len=한문서에 인덱싱할 벡터수=클러스터링수와 동일(기본=10개)
# - in: dim_size=벡터 차원(기본=128)
#---------------------------------------------------------------------------
def mpower_index_batch(es, index_name:str, docs, vector_len:int=10, dim_size:int=128):
        
    requests = []
    assert index_name is not None, f'error!!=>index_name is None'
    assert len(docs) > 0, f'error!! len(docs) < 1=>len(docs):{len(docs)}'

    for i, doc in enumerate(tqdm(docs)):
        rfile_name = doc['rfile_name']
        rfile_text = doc['rfile_text']
        dense_vectors = doc['dense_vectors']
        
        #--------------------------------------------------------------------
        # ES에 문단 인덱싱 처리
        request = {}  #dict 정의
        request["rfile_name"] = rfile_name   # 제목               
        request["rfile_text"] = rfile_text   # 문장
        
        request["_op_type"] = "index"        
        request["_index"] = index_name
        
        # vector 1~40 까지 값을 0으로 초기화 해줌.
        for i in range(vector_len):
            request["vector"+str(i+1)] = np.zeros((dim_size))
            
        # vector 값들을 담음.
        for i, dense_vector in enumerate(dense_vectors):
            request["vector"+str(i+1)] = dense_vector
            
        requests.append(request)
        #--------------------------------------------------------------------
                
    # batch 단위로 한꺼번에 es에 데이터 insert 시킴     
    bulk(es, requests)
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# 임베딩 BERT 모델 로딩
# => bi_encoder 모델 로딩, polling_mode 설정
# => bi_encoder1 = SentenceTransformer(bi_encoder_path) # 오히려 성능 떨어짐. 이유는 do_lower_case나, max_seq_len등 세부 설정이 안되므로.
#--------------------------------------------------------------------------- 
def load_embed_model(model_path:str, polling_mode:str, out_demension:int, device:str): 
    #BI_ENCODER1 = 0          # bi_encoder 모델 인스턴스 
    #WORD_EMBDDING_MODEL1 = 0 # bi_encoder 워드임베딩모델 인스턴스

    try:
        WORD_EMBDDING_MODEL1, BI_ENCODER1 = bi_encoder(model_path=model_path, max_seq_len=512, do_lower_case=True, 
                                                       pooling_mode=polling_mode, out_dimension=out_demension, device=device)
    except Exception as e:
         assert False, f'bi_encoder load fail({model_path})=>{e}'
    
    return WORD_EMBDDING_MODEL1, BI_ENCODER1

#---------------------------------------------------------------------------
# 임베딩 처리 함수 
# -in : paragrphs 문단 리스트
#---------------------------------------------------------------------------
# 조건에 맞게 임베딩 처리하는 함수 
def embedding(paragraphs:list, bi_encoder, float_type)->list:
    # 한 문단에 대한 40개 문장 배열들을 한꺼번에 임베딩 처리함
    embeddings = embed_text(model=bi_encoder, paragraphs=paragraphs, return_tensor=False).astype(float_type)    
    return embeddings

#---------------------------------------------------------------------------
# 비동기 임베딩 처리 함수
#---------------------------------------------------------------------------
async def async_embedding(paragraphs: list, bi_encoder, float_type) -> list:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, embedding, paragraphs, bi_encoder, float_type)
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
#문단에 문장들의 임베딩을 구하여 각각 클러스터링 처리함.
#---------------------------------------------------------------------------
def index_data(es, df_contexts, doc_sentences:list, 
               es_index_name:str, out_dimension:int, num_clusters:int, 
               num_clusters_variable:bool, embedding_method:int, clu_mode:str, 
               clu_outmode:str, bi_encoder, float_type, 
               seed:int, batch_size:int):
    
    #클러스터링 계수는 문단의 계수보다는 커야 함. 
    #assert num_clusters <= len(doc_sentences), f"num_clusters:{num_clusters} > len(doc_sentences):{len(doc_sentences)}"
    #-------------------------------------------------------------
    # 각 문단의 문장들에 벡터를 구하고 리스트에 저장해 둠.
    start = time.time()
    cluster_list = []

    rfile_names = df_contexts['contextid'].values.tolist()
    rfile_texts = df_contexts['question'].values.tolist()

    if out_dimension == 0:
        dimension = 768
    else:
        dimension = 128

    clustering_num = num_clusters
        
    docs = []
    count = 0
    for i, sentences in enumerate(tqdm(doc_sentences)):
        embeddings = embedding(sentences, bi_encoder, float_type)
        if i < 3:
            print(f'[{i}] sentences-------------------')
            if len(sentences) > 5:
                print(sentences[:5])
            else:
                print(sentences)
        
        #----------------------------------------------------------------
        multiple = 1
        
        # [bong][2023-04-28] 임베딩 출력 계수에 따라 클러스터링 계수를 달리함.
        if num_clusters_variable == True:
            embeddings_len = embeddings.shape[0]
            if embeddings_len > 2000:
                multiple = 6
            elif embeddings_len > 1000:
                multiple = 5 # 5배
            elif embeddings_len > 600:
                multiple = 4 # 4배
            elif embeddings_len > 300:
                multiple = 3 # 3배
            elif embeddings_len > 100:
                multiple = 2 # 2배
        #----------------------------------------------------------------
        
        # 0=문장클러스터링 임베딩
        if embedding_method == 0:
            if clu_mode == "kmeans":
                # 각 문단에 분할한 문장들의 임베딩 값을 입력해서 클러스터링 하고 평균값을 구함.
                # [bong][2023-04-28] 문장이 많은 경우에는 클러스터링 계수를 2,3배수로 함
                emb = clustering_embedding(embeddings = embeddings, outmode=clu_outmode, num_clusters=(clustering_num*multiple), seed=seed).astype(float_type) 
            else:
                emb = kmedoids_clustering_embedding(embeddings = embeddings, outmode=clu_outmode, num_clusters=(clustering_num*multiple), seed=seed).astype(float_type) 
            
        # 1= 문장평균임베딩
        elif embedding_method == 1:
            # 문장들에 대해 임베딩 값을 구하고 평균 구함.
            arr = np.array(embeddings).astype(float_type)
            emb = arr.mean(axis=0).reshape(1,-1) #(128,) 배열을 (1,128) 형태로 만들기 위해 reshape 해줌
            clustering_num = 1  # 평균값일때는 NUM_CLUSTERS=1로 해줌.
        # 2=문장임베딩
        else:
            emb = embeddings
      
        #--------------------------------------------------- 
        # docs에 저장 
        #  [bong][2023-04-28] 여러개 벡터인 경우에는 벡터를 10개씩 분리해서 여러개 docs를 만듬.
        for j in range(multiple):
            count += 1
            doc = {}                                #dict 선언
            doc['rfile_name'] = rfile_names[i]      # contextid 담음
            doc['rfile_text'] = rfile_texts[i]      # text 담음.
            doc['dense_vectors'] = emb[j * clustering_num : (j+1) * clustering_num] # emb 담음.
            docs.append(doc)
        #---------------------------------------------------    

            if count % batch_size == 0:
                mpower_index_batch(es, es_index_name, docs, vector_len=clustering_num, dim_size=dimension)
                docs = []

    if docs:
        mpower_index_batch(es, es_index_name, docs, vector_len=clustering_num, dim_size=dimension)

    es.indices.refresh(index=es_index_name)
    
    print(f'*인덱싱 시간 : {time.time()-start:.4f}\n')
#---------------------------------------------------------------------------

# main    
if __name__ == '__main__':
    main()