#----------------------------------------------------------------------
# FastAPI 이용한 임베딩 서버 예제2
# - 설치 :pip install fastapi[all]
# - python 업데이트(옵션) : conda install -c anaconda python=3.10 (3.10이상 필요)
# - 실행 : python model1.py 혹은 uvicorn model1:app --reload --host=0.0.0.0 --port=8000
# - POST 테스트 docs : IP/docs
# - 출처 : https://fastapi.tiangolo.com/ko/
# - elasticsearh는 7.17 설치해야 함. => pip install elasticsearch==7.17
#----------------------------------------------------------------------
import torch
import argparse
import time
import os
import platform
import pandas as pd
import numpy as np
from tqdm.notebook import tqdm

# os가 윈도우면 from eunjeon import Mecab 
if platform.system() == 'Windows':
    os.environ["OMP_NUM_THREADS"] = '1' # 윈도우 환경에서는 쓰레드 1개로 지정함

# FastAPI 관련    
import uvicorn
from enum import Enum
from typing import Union, Dict, List, Optional
from typing_extensions import Annotated
from fastapi import FastAPI, Query, Cookie, Form, Request, HTTPException, BackgroundTasks
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import asyncio
import threading
    
# ES 관련
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk

# myutils 관련
import sys
sys.path.append('..')
from myutils import bi_encoder, dense_model, onnx_model, onnx_embed_text
from myutils import seed_everything, GPU_info, mlogging, getListOfFiles, get_options
from myutils import remove_reverse, clean_text, make_query_script, create_index, mpower_index_batch
from myutils import embed_text, clustering_embedding, kmedoids_clustering_embedding
from myutils import split_sentences, split_sentences1, make_docs_df, get_sentences

# FutureWarning 제거
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) 

#---------------------------------------------------------------------------
# 전역 변수로 선언 => 함수 내부에서 사용할때 global 해줘야 함.

# FastAPI 서버 관련 
SETTINGS_FILE = './data/settings.yaml'  # 설정파일 경로 (yaml 파일)
HOST = '0.0.0.0'
PORT = '9200'

# 모델 관련
MODEL_PATH = 'bongsoo/kpf-sbert-128d-v1'
BI_ENCODER1 = 0          # bi_encoder 모델 인스턴스 
WORD_EMBDDING_MODEL1 = 0 # bi_encoder 워드임베딩모델 인스턴스
OUT_DIMENSION = 128      # 임베딩 모델 차원 수 (128, 0=768)

# 임베딩 방식 (0=문장클러스터링, 1=문장평균임베딩, 2=문장임베딩)
EMBEDDING_METHOD = 0   
FLOAT_TYPE = 'float16'   # 임베딩 벡터 float 타입('float32', 'float16')

LOGGER = 0               # 로그 인스턴스
DEVICE = 'cpu'           # 디바이스 (예: 'cpu', 'cuda:0') 
SEED = 111

# ES 관련 전역 변수
ES_URL = "http://localhost:9200/"
ES_INDEX_NAME = 'test_index'
ES_INDEX_FILE = './data/mpower10u_128d_10.json'  # 인덱스 파일 경로
BATCH_SIZE = 10  # 배치 사이즈 = 20이면 20개씩 ES에 인덱싱함.

# 클러스터링 전역 변수
# 클러스트링 param
CLUSTRING_MODE = "kmeans"  # "kmeans" = k-평균 군집 분석, kmedoids =  k-대표값 군집 분석
NUM_CLUSTERS = 10          # 클러스터링 계수 
OUTMODE = "mean"           # 클러스터링후 출력벡터 정의(kmeans 일때 => mean=평균벡터 출력, max=최대값벡터출력 / kmedoids 일때=>mean=평균벡터, medoid=대표값벡터)

# 문장 전처리
REMOVE_SENTENCE_LEN = 8     # 문장 길이가 8이하면 제거 
REMOVE_DUPLICATION = False  # 중복된 문장 제거(*중복된 문장 제거 안할때 1%정도 정확도 좋음)

# 검색 관련
SEARCH_SIZE = 5             # 검색 계수

# ES 벡터 크기 값(임의이 값지정) =>벡터의 크기는 각 구성 요소의 제곱 합의 제곱근으로 정의된다.. 
# 예를 들어, 벡터 [1, 2, 3]의 크기는 sqrt(1^2 + 2^2 + 3^2) 즉, 3.7416이 된다.
# 클수록 -> 스코어는 작아짐, 작을수록 -> 스코어 커짐.
VECTOR_MAG = 0.8   
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# 임베딩 처리 함수 
# -in : paragrphs 문단 리스트
#---------------------------------------------------------------------------
# 조건에 맞게 임베딩 처리하는 함수 
def embedding(paragrphs:list)->list:
    # 한 문단에 대한 40개 문장 배열들을 한꺼번에 임베딩 처리함
    embeddings = embed_text(model=BI_ENCODER1, paragraphs=paragrphs, return_tensor=False).astype(FLOAT_TYPE)  
    return embeddings

#---------------------------------------------------------------------------
# 비동기 임베딩 처리 함수
#---------------------------------------------------------------------------
async def async_embedding(paragraphs: list) -> list:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, embedding, paragraphs)
#---------------------------------------------------------------------------
      
#---------------------------------------------------------------------------
#문단에 문장들의 임베딩을 구하여 각각 클러스터링 처리함.
#---------------------------------------------------------------------------
def index_data(es, df_contexts, doc_sentences:list):
    #클러스터링 계수는 문단의 계수보다는 커야 함. 
    #assert num_clusters <= len(doc_sentences), f"num_clusters:{num_clusters} > len(doc_sentences):{len(doc_sentences)}"
    #-------------------------------------------------------------
    # 각 문단의 문장들에 벡터를 구하고 리스트에 저장해 둠.
    start = time.time()
    cluster_list = []

    rfile_names = df_contexts['contextid'].values.tolist()
    rfile_texts = df_contexts['question'].values.tolist()

    if OUT_DIMENSION == 0:
        dimension = 768
    else:
        dimension = 128

    docs = []
    count = 0
    for i, sentences in enumerate(tqdm(doc_sentences)):
        embeddings = embedding(sentences)
        if i < 3:
            print(f'[{i}] sentences-------------------')
            if len(sentences) > 10:
                print(sentences[:10])
            else:
                print(sentences)
                
        LOGGER.info(f'*[index_data] embeddings.shape: {embeddings.shape}')
        print()

        # 0=문장클러스터링 임베딩
        if EMBEDDING_METHOD == 0:
            if CLUSTRING_MODE == "kmeans":
                # 각 문단에 분할한 문장들의 임베딩 값을 입력해서 클러스터링 하고 평균값을 구함.
                #emb1 = clustering_embedding(embeddings = embeddings, outmode=outmode, num_clusters= 50, seed=seed)
                emb = clustering_embedding(embeddings = embeddings, outmode=OUTMODE, num_clusters= NUM_CLUSTERS, seed=SEED).astype(FLOAT_TYPE) 
            else:
                emb = kmedoids_clustering_embedding(embeddings = embeddings, outmode=OUTMODE, num_clusters= NUM_CLUSTERS, seed=SEED).astype(FLOAT_TYPE) 
        # 1= 문장평균임베딩
        elif EMBEDDING_METHOD == 1:
            # 문장들에 대해 임베딩 값을 구하고 평균 구함.
            arr = np.array(embeddings).astype(FLOAT_TYPE)
            emb = arr.mean(axis=0).reshape(1,-1) #(128,) 배열을 (1,128) 형태로 만들기 위해 reshape 해줌
        # 2=문장임베딩
        else:
            emb = embeddings

        #--------------------------------------------------- 
        count += 1
        doc = {} #dict 선언

        doc['rfile_name'] = rfile_names[i]      # contextid 담음
        doc['rfile_text'] = rfile_texts[i]      # text 담음.
        doc['dense_vectors'] = emb

        docs.append(doc)
        #---------------------------------------------------    

        if count % BATCH_SIZE == 0:
            mpower_index_batch(es, ES_INDEX_NAME, docs, vector_len=NUM_CLUSTERS, dim_size=dimension)
            docs = []
            LOGGER.info("[index_data] Indexed {} documents.".format(count))

    if docs:
        mpower_index_batch(es, ES_INDEX_NAME, docs, vector_len=NUM_CLUSTERS, dim_size=dimension)
        LOGGER.info("[index_data] Indexed {} documents.".format(count))   

    es.indices.refresh(index=ES_INDEX_NAME)

    LOGGER.info(f'*인덱싱 시간 : {time.time()-start:.4f}\n')
    print()
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# ES 임베딩 벡터 쿼리 실행 함수
# - in : query=쿼리 , search_size=검색출력계수
#---------------------------------------------------------------------------
def es_embed_query(esindex:str, query:str, search_size:int):
    
    query = query.strip()
    
    if not query:
        LOGGER.error(f'[es_embed_query] query is empty')
        return
    
    if search_size < 1:
        LOGGER.error(f'[es_embed_query] search_size < 1')
        return
    
    # 1.elasticsearch 접속
    es = Elasticsearch(ES_URL)
    
    #time.sleep(20)
    
    # LOGGER.info(f'es.info:{es.info()}')

    # 2. 검색 문장 embedding 후 벡터값 
    # 쿼리들에 대해 임베딩 값 구함
    start_embedding_time = time.time()
    embed_query = embedding([query])
    end_embedding_time = time.time() - start_embedding_time
    print("*embedding time: {:.2f} ms".format(end_embedding_time * 1000)) 
    print(f'*embed_querys.shape:{embed_query.shape}\n')

    # 3. 쿼리 만듬
    # - 쿼리 1개만 하므로, embed_query[0]으로 입력함.
    script_query = make_query_script(query_vector=embed_query[0], vectormag=VECTOR_MAG, vectornum=10) # 쿼리를 만듬.

    #print(script_query)
    #print()

    # 4. 실제 ES로 검색 쿼리 날림
    response = es.search(
        index=esindex,
        body={
            "size": search_size,
            "query": script_query,
            "_source":{"includes": ["rfile_name","rfile_text"]}
        }
    )
    
    LOGGER.info(f'[es_embed_query] response:{response}')

    # 5. 결과 리턴
    # - 쿼리 응답 결과값에서 _id, _score, _source 등을 뽑아내고 내림차순 정렬후 결과값 리턴
    #print(response)
    
    rfilename = []
    rfiletext = [] 
    bi_scores = []
    for hit in response["hits"]["hits"]: 
        # 리스트에 저장해둠
        rfilename.append(hit["_source"]["rfile_name"])
        rfiletext.append(hit["_source"]["rfile_text"])
        bi_scores.append(hit["_score"])

    # 내림 차순으로 정렬 
    dec_bi_scores = reversed(np.argsort(bi_scores))

    des_rfilename=[]
    des_rfiletext=[]
    des_bi_scores=[]
    for idx in dec_bi_scores:
        des_rfilename.append(rfilename[idx])
        des_rfiletext.append(rfiletext[idx])
        des_bi_scores.append(bi_scores[idx])

    return query, des_rfilename, des_rfiletext, des_bi_scores # 쿼리,  rfilename, rfiletext,  스코어 리턴 

#---------------------------------------------------------------------------
# 비동기 ES 임베딩 벡터 쿼리 실행 함수
#---------------------------------------------------------------------------
async def async_es_embed_query(esindex:str, query:str, search_size:int):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, es_embed_query, esindex, query, search_size)
#---------------------------------------------------------------------------

app = FastAPI() #FastAPI 인스턴스 생성

#=========================================================
# 루트=>정보 출력
# => http://127.0.0.1:9000/
#=========================================================
@app.get("/")
async def root():
    return {"서버": "문장 임베딩 AI 모델", 
            "*host":HOST, 
            "*port":PORT, 
            "*임베딩모델":{"모델경로": MODEL_PATH, "출력차원": OUT_DIMENSION,"임베딩방식": EMBEDDING_METHOD, "출력벡터타입": FLOAT_TYPE},
            "*ES서버":{"URL":ES_URL, "인덱스파일": ES_INDEX_FILE, "인덱스명": ES_INDEX_NAME, "배치크기": BATCH_SIZE},
            "*클러스터링":{"방식": CLUSTRING_MODE, "계수": NUM_CLUSTERS, "출력": OUTMODE},
            "*문장전처리":{"제거문장길이": REMOVE_SENTENCE_LEN, "중복제거": REMOVE_DUPLICATION},
            "*검색":{"검색수": SEARCH_SIZE, "*검색비교벡터값": VECTOR_MAG}
            }

#=========================================================
# 입력 문장 리스트에 대한 임베딩값 리턴
# => http://127.0.0.1:9000/embed/
# - in : 문장 리스트 (예: ['오늘 날씨가 좋다', '내일은 비가 온다'] ), uid(문서 고유id)
# - out: 문장 리스트에 대한 임베딩 벡터
#=========================================================
class EmbedIn(BaseModel):
    uid: str            # uid(문서 고유id)->rfilename
    sentences: list      # 문장리스트  

@app.post("/embed")
def embed(Data:EmbedIn):
    sentences = Data.sentences
    uid = Data.uid
    #return {"uid":uid, "sentences":sentences}
    embeddings = embedding(sentences)

    # json 전송하기위해, 각 변수에 ,(쉼표) 를 추가해서 문자열로 만듬.
    embeddings_str = [",".join(str(elem) for elem in sublist) for sublist in embeddings]
    return {"uid": uid, "embed": embeddings_str}

#========================================================
# async def로 지정하면, embedding 비동기 함수도 동기화로 wrapping하여 실행해야 한다.
@app.post("/async-embed")
async def embed(data: EmbedIn, background_tasks: BackgroundTasks):
    sentences = data.sentences
    uid = data.uid

    # embedding 함수를 async 함수로 wrapping한 async_embedding 함수를 실행합니다.
    embeddings = await async_embedding(sentences)

    embeddings_str = [",".join(str(elem) for elem in sublist) for sublist in embeddings]
    return {"uid": uid, "embed": embeddings_str}
#========================================================

#=========================================================
# 입력 문장 리스트에 대한 임베딩값 구하고 ElasticSearch(이하:ES) 추가.
# => http://127.0.0.1:9000/embed/es?esindex=myindex
# - in : docs: 문서 (예: ['오늘 날씨가 좋다', '내일은 비가 온다'] ), titles: 문서제목, uids(문서 고유id)
# - in : esindexname : ES 인덱스명, createindex=True(True=무조건 인덱스생성. 만약 있으면 삭제후 생성/ Flase=있으면 추가, 없으면 생성)
# - out: ES 성공 실패??
#=========================================================
class DocsEmbedIn(BaseModel):
    uids: list       # uid(문서 고유id)->rfilename
    titles: list     # 제목->rfiletext
    documents: list  # 문서내용  

@app.post("/embed/es")
def embed_documents(esindex:str, Data:DocsEmbedIn, createindex:bool=False):
    documents = Data.documents
    uids = Data.uids
    titles = Data.titles
    
    LOGGER.info(f'/embed/es start-----\nES_URL:{ES_URL}, esindex:{esindex}, createindex:{createindex}, uids:{uids}, titles:{titles}')

    # 인자 검사
    if len(documents) < 1:
        LOGGER.error(f'/embed/es documents len < 1')
        raise HTTPException(status_code=404, detail="documents len < 1", headers={"X-Error": "documents len < 1"},)

    if len(uids) < 1:
        LOGGER.error(f'/embed/es uid not found')
        raise HTTPException(status_code=404, detail="uid not found", headers={"X-Error": "uid is empty"},)
    
    if len(titles) < 1:
        LOGGER.error(f'/embed/es titles not found')
        raise HTTPException(status_code=404, detail="titles not found", headers={"X-Error": "titles is empty"},)
    
    if not esindex:
        LOGGER.error(f'/embed/es esindex not found')
        raise HTTPException(status_code=404, detail="esindex not found", headers={"X-Error": "esindex is empty"},)
    
    # 전역변수로 ES 인덱스명 저장해 둠.
    global ES_INDEX_NAME
    ES_INDEX_NAME = esindex

    # 1. 추출된 문서들 불러와서 df로 만듬
    df_contexts = make_docs_df(documents, titles, uids)
    LOGGER.info(f'/embed/es 1.load_docs success')
    
    # 2. 문장 추출
    doc_sentences = get_sentences(df=df_contexts, remove_sentnece_len=REMOVE_SENTENCE_LEN, remove_duplication=REMOVE_DUPLICATION)
    LOGGER.info(f'/embed/es 2.get_sentences success=>len(doc_sentences):{len(doc_sentences)}')

    # 3.elasticsearch 접속
    es = Elasticsearch(ES_URL)
    LOGGER.info(f'/embed/es 3.Elasticsearch connect success')
    #LOGGER.info(f'es.info:{es.info()}')

    # 4.ES 인덱스 생성
    create_index(es, ES_INDEX_FILE, ES_INDEX_NAME, createindex)
    LOGGER.info(f'/embed/es 4.create_index success=>index_file:{ES_INDEX_FILE}, index_name:{ES_INDEX_NAME}')

    # 5. index 처리
    index_data(es, df_contexts, doc_sentences)
    LOGGER.info(f'/embed/es 5.index_data success\nend-----\n')
            
#=========================================================

#=========================================================
# ES 검색(GET)
# => http://127.0.0.1:9000/search/test3?query=쿼리문장&search_size=5
# - in : query=쿼리할 문장, search_size=검색계수(몇개까지 검색 출력 할지)
# - out: 검색 결과(스코어, rfile_name, rfile_text)
#=========================================================

@app.get("/search/{esindex}")
def search_documents(esindex:str, 
                     query: str = Query(..., min_length=1),     # ... 는 필수 입력 이고, min_length=1은 최소값이 1임. 작으면 422 Unprocessable Entity 응답반환됨
                     search_size: int = Query(..., gt=0)):      # ... 는 필수 입력 이고, gt=0은 0보다 커야 한다. 작으면 422 Unprocessable Entity 응답반환됨
       
    query = query.strip()
    
    # 인자 검사
    if not query:
        LOGGER.error(f'/search/ query is empty')
        raise HTTPException(status_code=404, detail="query is empty", headers={"X-Error": "query is empty"},)
  
    if search_size < 1:
        LOGGER.error(f'/search/ search_size < 1')
        raise HTTPException(status_code=404, detail="search_size < 1", headers={"X-Error": "search_size < 1"},)
        
    if not esindex:
        LOGGER.error(f'/search/ esindex not found')
        raise HTTPException(status_code=404, detail="esindex not found", headers={"X-Error": "esindex is empty"},)
        
    LOGGER.info(f'\nget /search/ start-----\nquery:{query}, search_size:{search_size}')
    
    # es로 임베딩 쿼리 실행
    q, des_rfilename, des_rfiletext, des_bi_scores = es_embed_query(esindex, query, search_size)
    
    return {"query":q, "rfilename": des_rfilename, "rfiletext": des_rfiletext, "scores": des_bi_scores}

#========================================================
# 비동기 get searh 함수 
# => async def 비동기로 쿼리 할때 내부에 함수가 비동기 함수가 아니면, blocking되므로, 비동기 함수를 호출해야 함. 
@app.get("/async-search/{esindex}")
async def search_documents(esindex:str, 
                     query: str = Query(..., min_length=1),     # ... 는 필수 입력 이고, min_length=1은 최소값이 1임. 작으면 422 Unprocessable Entity 응답반환됨
                     search_size: int = Query(..., gt=0)):      # ... 는 필수 입력 이고, gt=0은 0보다 커야 한다. 작으면 422 Unprocessable Entity 응답반환됨
       
    query = query.strip()
    
    # 인자 검사
    if not query:
        LOGGER.error(f'/async-search query is empty')
        raise HTTPException(status_code=404, detail="query is empty", headers={"X-Error": "query is empty"},)
  
    if search_size < 1:
        LOGGER.error(f'/sasync-search search_size < 1')
        raise HTTPException(status_code=404, detail="search_size < 1", headers={"X-Error": "search_size < 1"},)
        
    if not esindex:
        LOGGER.error(f'/async-search esindex not found')
        raise HTTPException(status_code=404, detail="esindex not found", headers={"X-Error": "esindex is empty"},)
        
    LOGGER.info(f'\nget /async-search start-----\nquery:{query}, search_size:{search_size}')
    
    # 비동기 es search 함수 호출
    q, des_rfilename, des_rfiletext, des_bi_scores = await async_es_embed_query(esindex, query, search_size)
    
    return {"query":q, "rfilename": des_rfilename, "rfiletext": des_rfiletext, "scores": des_bi_scores}
#========================================================

#=========================================================
# ES 검색(POST)
# => http://127.0.0.1:9000/search/?esindex=test3
# - in : query=쿼리할 문장, search_size=검색계수(몇개까지 검색 출력 할지)
# - out: 검색 결과(스코어, rfile_name, rfile_text)
#=========================================================
class QueryIn(BaseModel):
    query: str              # 쿼리 문장  
    search_size: int        # 검색 계수

@app.post("/search")
def search_documents(esindex:str, Data:QueryIn):

    query = Data.query.strip()
    search_size = Data.search_size

    # 인자 검사        
    if not query:
        LOGGER.error(f'/search query is empty')
        raise HTTPException(status_code=404, detail="query is empty", headers={"X-Error": "query is empty"},)
  
    if search_size < 1:
        LOGGER.error(f'/search search_size < 1')
        raise HTTPException(status_code=404, detail="search_size < 1", headers={"X-Error": "search_size < 1"},)
    
    if not esindex:
        LOGGER.error(f'/search esindex not found')
        raise HTTPException(status_code=404, detail="esindex not found", headers={"X-Error": "esindex is empty"},)

    LOGGER.info(f'\npost /search start-----\nquery:{query}, search_size:{search_size}')

    # es로 임베딩 쿼리 실행
    q, des_rfilename, des_rfiletext, des_bi_scores = es_embed_query(esindex, query, search_size)
    
    return {"query":q, "rfilename": des_rfilename, "rfiletext": des_rfiletext, "scores": des_bi_scores}

#=========================================================
# 비동기 put search  
# => async def 비동기로 쿼리 할때 내부에 함수가 비동기 함수가 아니면, blocking되므로, 비동기 함수를 호출해야 함. 
@app.post("/async-search")
async def search_documents(esindex:str, Data:QueryIn):

    query = Data.query.strip()
    search_size = Data.search_size

    # 인자 검사
    if not query:
        LOGGER.error(f'/search/async/ query is empty')
        raise HTTPException(status_code=404, detail="query is empty", headers={"X-Error": "query is empty"},)
  
    if search_size < 1:
        LOGGER.error(f'/search/async/ search_size < 1')
        raise HTTPException(status_code=404, detail="search_size < 1", headers={"X-Error": "search_size < 1"},)
    
    if not esindex:
        LOGGER.error(f'/search/async/ esindex not found')
        raise HTTPException(status_code=404, detail="esindex not found", headers={"X-Error": "esindex is empty"},)

    LOGGER.info(f'\npost /search/async/ start-----\nquery:{query}, search_size:{search_size}')

     # 비동기 es search 함수 호출
    q, des_rfilename, des_rfiletext, des_bi_scores = await async_es_embed_query(esindex, query, search_size)
    
    return {"query":q, "rfilename": des_rfilename, "rfiletext": des_rfiletext, "scores": des_bi_scores}
  
#=========================================================

#=========================================================
# main()
# - 인자를 파싱. bi_encoder 모델 로딩. FastAPI서버 실행
#=========================================================
def main():
    #------------------------------------
    # args 처리
    #------------------------------------
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-host', dest='host', help='', default='0.0.0.0')  # FastAPI 서버 바인딩 host
    parser.add_argument('-port', dest='port', help='', default=9000)       # FastAPI 서버 바인딩 port
      
    args = parser.parse_args()

    global OUT_DIMENSION, EMBEDDING_METHOD, FLOAT_TYPE, ES_INDEX_FILE, ES_URL
    global BATCH_SIZE, CLUSTRING_MODE, NUM_CLUSTERS, OUTMODE, REMOVE_SENTENCE_LEN
    global LOGGER, DEVICE, REMOVE_DUPLICATION, VECTOR_MAG, HOST, PORT, MODEL_PATH

    # 설정값 settings.yaml 파일 로딩
    settings = get_options(file_path=SETTINGS_FILE)
    assert len(settings) > 2, f'load settings error!!=>len(settigs):{len(settings)}'
    
    #------------------------------------
    # param
    #------------------------------------
    logfilepath = settings['env']['LOG_PATH']
    seed = settings['env']['SEED']
    DEVICE = settings['env']['GPU']
    assert DEVICE=='auto' or DEVICE=='cpu', f'DEVICE setting error!!. DEVICE is auto or cpu=>DEVICE:{DEVICE}'
    
    LOGGER = mlogging(loggername="embed-server", logfilename=logfilepath) # 로그
    seed_everything(seed)
    if DEVICE == 'auto':
        DEVICE = GPU_info() # GPU 혹은 CPU
    
    LOGGER.info(f'*환경 Settings: LOG_PATH:{logfilepath}, SEED:{seed}, DEVICE:{DEVICE}')

    HOST = args.host 
    PORT = args.port
    LOGGER.info(f'*host:{HOST}, port:{PORT}')
    
    # 모델 정보 로딩
    MODEL_PATH = settings['model']['MODEL_PATH']  
    POLLING_MODE = settings['model']['POLLING_MODE']
    OUT_DIMENSION = settings['model']['OUT_DIMENSION']
    if OUT_DIMENSION == 768:
        OUT_DIMENSION = 0
    LOGGER.info(f'*모델 Settings: MODEL_PATH:{MODEL_PATH}, POLLING_MODE:{POLLING_MODE}, OUT_DIMENSION:{OUT_DIMENSION}')
    
    # 임베딩 정보 로딩
    EMBEDDING_METHOD = settings['embedding']['EMBEDDING_METHOD']
    FLOAT_TYPE = settings['embedding']['FLOAT_TYPE']
    LOGGER.info(f'*임베딩 Settings: EMBEDDING_METHOD:{EMBEDDING_METHOD}, FLOAT_TYPE:{FLOAT_TYPE}')

    # ES 관련 전역 변수
    ES_URL = settings['es']['ES_URL']
    ES_INDEX_FILE = settings['es']['ES_INDEX_FILE']
    BATCH_SIZE = settings['es']['BATCH_SIZE']
    LOGGER.info(f'*ES Settings: ES_URL:{ES_URL}, ES_INDEX_FILE:{ES_INDEX_FILE}, BATCH_SIZE:{BATCH_SIZE}')

    # 클러스터링 전역 변수
    CLUSTRING_MODE = settings['custring']['CLUSTRING_MODE']
    NUM_CLUSTERS = settings['custring']['NUM_CLUSTERS']
    OUTMODE = settings['custring']['OUTMODE']
    LOGGER.info(f'*클러스터링 Settings: CLUSTRING_MODE:{CLUSTRING_MODE}, NUM_CLUSTERS:{NUM_CLUSTERS}, OUTMODE:{OUTMODE}')

    # 문장 전처리
    REMOVE_SENTENCE_LEN = settings['preprocessing']['REMOVE_SENTENCE_LEN']
    REMOVE_DUPLICATION = settings['preprocessing']['REMOVE_DUPLICATION']
    LOGGER.info(f'*문장전처리 Settings: REMOVE_SENTENCE_LEN:{REMOVE_SENTENCE_LEN}, REMOVE_DUPLICATION:{REMOVE_DUPLICATION}')

    # 검색 관련
    VECTOR_MAG = settings['search']['VECTOR_MAG']
    LOGGER.info(f'*검색 Settings: VECTOR_MAG:{VECTOR_MAG}')

    #------------------------------------
    # 임베딩 BERT 모델 로딩
    # => bi_encoder 모델 로딩, polling_mode 설정
    # => bi_encoder1 = SentenceTransformer(bi_encoder_path) # 오히려 성능 떨어짐. 이유는 do_lower_case나, max_seq_len등 세부 설정이 안되므로.
    #------------------------------------
    global BI_ENCODER1, WORD_EMBDDING_MODEL1
    WORD_EMBDDING_MODEL1, BI_ENCODER1 = bi_encoder(model_path=MODEL_PATH, max_seq_len=512, do_lower_case=True, 
                                                   pooling_mode=POLLING_MODE, out_dimension=OUT_DIMENSION, device=DEVICE)
    
    LOGGER.info(f'\n---bi_encoder---------------------------')
    LOGGER.info(BI_ENCODER1)
    LOGGER.info(WORD_EMBDDING_MODEL1)
    LOGGER.info(f'\n----------------------------------------')
    #------------------------------------
  
    # 모델 저장
    #output_path = "../../data11/model/kpf-sbert-128d-v1"
    #BI_ENCODER1.save(output_path)

    #------------------------------------
    # FastAPI 서버 실행 - uvicorn으로 실행.
    #------------------------------------
    print(f'embedding server start')
    print()
    uvicorn.run(app, host=HOST, port=PORT)
#=========================================================

if __name__ == "__main__":
    main()

    