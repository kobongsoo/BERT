#----------------------------------------------------------------------
# FastAPI 이용한 문서 분류 서버 예제
# - 설치 :pip install fastapi[all]
# - python 업데이트(옵션) : conda install -c anaconda python=3.10 (3.10이상 필요)
# - 실행 : uvicorn model1:app --host=0.0.0.0 --port=9000 --limit-concurrency=200
# - POST 테스트 docs : IP/docs
# - 출처 : https://fastapi.tiangolo.com/ko/
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
    
# Faiss 관련
import faiss

# myutils 관련
import sys
sys.path.append('..')
from myutils import bi_encoder, dense_model
from myutils import seed_everything, GPU_info, mlogging, getListOfFiles, get_options
from myutils import remove_reverse, clean_text, make_max_query_script, make_avg_query_script, create_index, mpower_index_batch
from myutils import embed_text, clustering_embedding, kmedoids_clustering_embedding
from myutils import split_sentences1, make_docs_df, get_sentences
from myutils import fassi_index, find_max

# FutureWarning 제거
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) 

#---------------------------------------------------------------------------
# 전역 변수로 선언 => 함수 내부에서 사용할때 global 해줘야 함.

# FastAPI 서버 관련 
SETTINGS_FILE = './data/class_settings.yaml'  # 설정파일 경로 (yaml 파일)
#------------------------------------
# args 처리
#------------------------------------

# 설정값 settings.yaml 파일 로딩
settings = get_options(file_path=SETTINGS_FILE)
assert len(settings) > 2, f'load settings error!!=>len(settigs):{len(settings)}'
    
#------------------------------------
# param
#------------------------------------
logfilepath = settings['env']['LOG_PATH']
SEED = settings['env']['SEED']
DEVICE = settings['env']['GPU']
assert DEVICE=='auto' or DEVICE=='cpu', f'DEVICE setting error!!. DEVICE is auto or cpu=>DEVICE:{DEVICE}'
    
LOGGER = mlogging(loggername="classification-server", logfilename=logfilepath) # 로그
seed_everything(SEED)
if DEVICE == 'auto':
    DEVICE = GPU_info() # GPU 혹은 CPU
    
LOGGER.info(f'*환경 Settings: LOG_PATH:{logfilepath}, SEED:{SEED}, DEVICE:{DEVICE}')
    
# 모델 정보 로딩
MODEL_PATH = settings['model']['MODEL_PATH']  
POLLING_MODE = settings['model']['POLLING_MODE']   # 폴링모드*(mean, cls, max 중 1나)
OUT_DIMENSION = settings['model']['OUT_DIMENSION'] # 임베딩 모델 차원 수 (128, 0=768)
if OUT_DIMENSION == 768:
    OUT_DIMENSION = 0
LOGGER.info(f'*모델 Settings: MODEL_PATH:{MODEL_PATH}, POLLING_MODE:{POLLING_MODE}, OUT_DIMENSION:{OUT_DIMENSION}')
    
# 임베딩 정보 로딩
EMBEDDING_METHOD = settings['embedding']['EMBEDDING_METHOD'] # 임베딩 방식 (0=문장클러스터링, 1=문장평균임베딩, 2=문장임베딩)
FLOAT_TYPE = settings['embedding']['FLOAT_TYPE'] # 임베딩 벡터 float 타입('float32', 'float16')
LOGGER.info(f'*임베딩 Settings: EMBEDDING_METHOD:{EMBEDDING_METHOD}, FLOAT_TYPE:{FLOAT_TYPE}')

# 클러스터링 전역 변수
CLUSTRING_MODE = settings['custring']['CLUSTRING_MODE'] # "kmeans" = k-평균 군집 분석, kmedoids =  k-대표값 군집 분석
NUM_CLUSTERS = settings['custring']['NUM_CLUSTERS'] # 클러스터링 계수 
OUTMODE = settings['custring']['OUTMODE']# 클러스터링후 출력벡터 정의(kmeans 일때 => mean=평균벡터 출력, max=최대값벡터출력 / kmedoids 일때=>mean=평균벡터, medoid=대표값벡터)
NUM_CLUSTERS_VARIABLE = settings['custring']['NUM_CLUSTERS_VARIABLE']# True이면 문장길이에 따라 클러스터링수를 다르게 함, False이면 클러스터링 계수가 고정.
LOGGER.info(f'*클러스터링 Settings: CLUSTRING_MODE:{CLUSTRING_MODE}, NUM_CLUSTERS:{NUM_CLUSTERS}, NUM_CLUSTERS_VARIABLE:{NUM_CLUSTERS_VARIABLE}, OUTMODE:{OUTMODE}')

# 문장 전처리
REMOVE_SENTENCE_LEN = settings['preprocessing']['REMOVE_SENTENCE_LEN'] # 문장 길이가 8이하면 제거 
REMOVE_DUPLICATION = settings['preprocessing']['REMOVE_DUPLICATION']# 중복된 문장 제거(*중복된 문장 제거 안할때 1%정도 정확도 좋음)
LOGGER.info(f'*문장전처리 Settings: REMOVE_SENTENCE_LEN:{REMOVE_SENTENCE_LEN}, REMOVE_DUPLICATION:{REMOVE_DUPLICATION}')

# FAISS 
FAISS_INDEX_METHOD = settings['faiss']['INDEX_METHOD'] # 0= Cosine Similarity 적용(IndexFlatIP 사용), 1= Euclidean Distance 적용(IndexFlatL2 사용)

#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# 임베딩 BERT 모델 로딩
# => bi_encoder 모델 로딩, polling_mode 설정
# => bi_encoder1 = SentenceTransformer(bi_encoder_path) # 오히려 성능 떨어짐. 이유는 do_lower_case나, max_seq_len등 세부 설정이 안되므로.
#------------------------------------    
#BI_ENCODER1 = 0          # bi_encoder 모델 인스턴스 
#WORD_EMBDDING_MODEL1 = 0 # bi_encoder 워드임베딩모델 인스턴스

try:
    WORD_EMBDDING_MODEL1, BI_ENCODER1 = bi_encoder(model_path=MODEL_PATH, max_seq_len=512, do_lower_case=True, 
                                                   pooling_mode=POLLING_MODE, out_dimension=OUT_DIMENSION, device=DEVICE)
except Exception as e:
    LOGGER.error(f'bi_encoder load fail({MODEL_PATH})=>{e}')
    assert False, f'bi_encoder load fail({MODEL_PATH})=>{e}'
    
LOGGER.info(f'\n---bi_encoder---------------------------')
LOGGER.info(BI_ENCODER1)
LOGGER.info(WORD_EMBDDING_MODEL1)
LOGGER.info(f'\n----------------------------------------')
  
#---------------------------------------------------------------------------
# 임베딩 처리 함수 
# -in : paragrphs 문단 리스트
#---------------------------------------------------------------------------
# 조건에 맞게 임베딩 처리하는 함수 
def embedding(paragraphs:list)->list:
    # 한 문단에 대한 40개 문장 배열들을 한꺼번에 임베딩 처리함
    embeddings = embed_text(model=BI_ENCODER1, paragraphs=paragraphs, return_tensor=False).astype(FLOAT_TYPE)    
    return embeddings

#---------------------------------------------------------------------------
# 비동기 임베딩 처리 함수
#---------------------------------------------------------------------------
async def async_embedding(paragraphs: list) -> list:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, embedding, paragraphs)
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# 문서분류를 위해 문서에 문장들의 임베딩을 구하고 faiss 인덱싱 처리하는 함수
# -in : doc_sentences: 문서들에 대한 문장리스트(2차원)(예: [['오늘은 날씨가 좋다','날씨가 좋다','비가온다'],[...],[...]])
#---------------------------------------------------------------------------
def docs_faiss_index(doc_sentences:list):
    
    error: str = 'success'
    start = time.time()
    
    # 인자 검사
    if len(doc_sentences) < 1:
        error = 'doc_sentences is empty'
    
    if error != 'success':
        LOGGER.error(f'[docs_faiss_index] {error}')
        return error, None
    
    clustering_num = NUM_CLUSTERS
    faissindexlist = []
    
    # 문장들에 대한 임베딩 벡터를 구함.
    for i, sentences in enumerate(tqdm(doc_sentences)):
        embeddings = embedding(sentences)
        if i < 3:
            print(f'[{i}] sentences-------------------')
            if len(sentences) > 5:
                print(sentences[:5])
            else:
                print(sentences)
                
        LOGGER.info(f'*[docs_faiss_index] embeddings.shape: {embeddings.shape}')
        print()
        
        #----------------------------------------------------------------
        # [bong][2023-04-28] 임베딩 출력 계수에 따라 클러스터링 계수를 달리함.
        multiple = 1
        
        if NUM_CLUSTERS_VARIABLE == True:
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
        
        #----------------------------------------------------------------
        # 0=문장클러스터링 임베딩
        if EMBEDDING_METHOD == 0:
            if CLUSTRING_MODE == "kmeans":
                # 각 문단에 분할한 문장들의 임베딩 값을 입력해서 클러스터링 하고 평균값을 구함.
                # [bong][2023-04-28] 문장이 많은 경우에는 클러스터링 계수를 2,3배수로 함
                emb = clustering_embedding(embeddings = embeddings, outmode=OUTMODE, num_clusters=(clustering_num*multiple), seed=SEED).astype(FLOAT_TYPE) 
            else:
                emb = kmedoids_clustering_embedding(embeddings = embeddings, outmode=OUTMODE, num_clusters=(clustering_num*multiple), seed=SEED).astype(FLOAT_TYPE) 
            
        # 1= 문장평균임베딩
        elif EMBEDDING_METHOD == 1:
            # 문장들에 대해 임베딩 값을 구하고 평균 구함.
            arr = np.array(embeddings).astype(FLOAT_TYPE)
            emb = arr.mean(axis=0).reshape(1,-1) #(128,) 배열을 (1,128) 형태로 만들기 위해 reshape 해줌
        # 2=문장임베딩
        else:
            emb = embeddings

        LOGGER.info(f'*[docs_faiss_index] cluster emb.shape: {emb.shape}')
        print()
        #----------------------------------------------------------------
     
        # Faiss index 생성하고 추가 (*faiss를 사용할때는 float32형이어야함)
        emb = emb.astype('float32')
        index = fassi_index(embeddings=emb, method=FAISS_INDEX_METHOD)
        faissindexlist.append(index)
        
    return error, faissindexlist
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# faiss인덱스 쿼리
# -각 인덱스와 라벨들을 유사도 비교하여 최대값 같은 라벨을 찾는 함수
# -in : faiss_index: faiss 인덱스 리스트, label_uids: 라벨 uid 리스트, labels: 라벨(내용) 리스트
# -out : error, 라벨 리스트([{'uid':f11, 'label':'사업계획서'},{},{}]
#---------------------------------------------------------------------------
def search_label(faiss_index:list, 
                 label_uids:list, 
                 labels:list):
    
    error: str = 'success'
    
    # 인자 검사
    if len(faiss_index) < 1:
        error = 'faiss is empty'
    elif len(label_uids) < 1:
        error = 'label_uids is empty'
    elif len(labels) < 1:
        error = 'labels is empty'
    
    if error != 'success':
        LOGGER.error(f'[search_label] {error}')
        return error, None
    
    df_label_contexts = pd.DataFrame((zip(label_uids, labels)), columns = ['uid','label'])
    
    # 쿼리(라벨) 임베딩 값을 구함.
    querys = df_label_contexts['label'].values.tolist()
    embed_querys = embedding(querys)
    embed_querys = embed_querys.astype('float32')
    if FAISS_INDEX_METHOD == 0:
        faiss.normalize_L2(embed_querys)     # *cosine유사도 구할때는 반드시 normalize 처리함.
    
    predictions_list = []   
    for count, index in enumerate(faiss_index):
        max_distance = 0
        max_idx = 0
        for query_count, embed_query in enumerate(embed_querys):
            embed_query = [embed_query]
            distance, idx = index.search(np.array(embed_query).astype("float32"), k=1) # 가장 유사한 1개 sub 문장을 찾음.
            
            # 쿼리(라벨)중에서 최대값을 구함.
            if max_distance < distance:
                max_distance = distance[0][0]  # distance가 2차원배열로 1개 출력되므로, [0][0] 해줌.
                max_idx = query_count
         
        #print(f'max_distance:{max_distance}, max_idx:{max_idx}')
        
        # 최대값 라벨id를 리스트에 저장해 둠.
        max_label = {}
        max_label['uid'] = df_label_contexts['uid'][max_idx]
        max_label['score'] = str(max_distance)
        predictions_list.append(max_label)   
        
        #print('predictions_list')
        #print(f'{predictions_list}')
        
    return error, predictions_list
#---------------------------------------------------------------------------

# 모델 저장
#output_path = "../../data11/model/kpf-sbert-128d-v1"
#BI_ENCODER1.save(output_path)
#---------------------------------------------------------------------------
    
# http://10.10.4.10:9000/docs=>swagger UI, http://10.10.4.10:9000/redoc=>ReDoc UI 각각 비활성화 하려면
# => docs_url=None, redoc_url=None 하면 된다.
#app = FastAPI(redoc_url=None) #FastAPI 인스턴스 생성(*redoc UI 비활성화)
app = FastAPI()

#=========================================================
# 루트=>정보 출력
# => http://127.0.0.1:9000/
#=========================================================
@app.get("/")
async def root():
    return {"서버": "문서 분류 API 서버", 
            "*임베딩모델":{"모델경로": MODEL_PATH, "폴링방식((mean=평균값, cls=문장대표값, max=최대값)": POLLING_MODE, "출력차원(128, 0=768)": OUT_DIMENSION,"임베딩방식(0=문장클러스터링, 1=문장평균임베딩, 2=문장임베딩)": EMBEDDING_METHOD, "출력벡터타입('float32', 'float16')": FLOAT_TYPE},
            "*클러스터링":{"클러스터링 가변(True=문장계수에 따라 클러스터링계수를 다르게함)": NUM_CLUSTERS_VARIABLE, "방식(kmeans=k-평균 군집 분석, kmedoids=k-대표값 군집 분석)": CLUSTRING_MODE, "계수": NUM_CLUSTERS, "출력(mean=평균벡터 출력, max=최대값벡터출력)": OUTMODE},
            "*문장전처리":{"제거문장길이(설정길이보다 작은 문장은 제거됨)": REMOVE_SENTENCE_LEN, "중복문장제거(True=중복된문장은 제거됨)": REMOVE_DUPLICATION},
            "*Faiss":{"*방식(0=Cosine, 1=Euclidean)": FAISS_INDEX_METHOD}
            }

#=========================================================
# POST : /docs/label => 문서분류하기 : 입력 문서들을 클러스터링후 벡터 구하고,  입력 라벨(문장) 벡터와 비교하여 max 유사도 계산후 출력
# => http://127.0.0.1:9000/docs/label
# - in : docs: 문서 (예: ['오늘 날씨가 좋다', '내일은 비가 온다'] ), titles: 문서제목, uids(문서 고유id)
# - in : lable_uids : 분류 라벨 고유 id, labels: 라벨명(내용)
# - in : infilepath : True이면 documnets에 filepath 입력되고, 이때는 file를 로딩함. False이면 documents로는 문서내용이 들어옴.
# - out: 검색 결과(스코어, rfile_name, rfile_text)
#=========================================================
class DocsIn(BaseModel):
    uids: list       # uid(문서 고유id)->rfilename
    titles: list     # 제목->rfiletext
    documents: list  # 문서내용 혹은 file 경로 (infilepath=True이면, filepath 입력됨)
    
class LabelsIn(BaseModel):
    label_uids: list  # 분류라벨 고유 id
    label_text : list     # 분류 라벨(상세내용)
  
@app.post("/docs/label")
def documents_classification(Docs:DocsIn, 
                             Labels:LabelsIn,  
                             infilepath:bool=False):
    error:str = 'success'
    
    documents = Docs.documents
    uids = Docs.uids
    titles = Docs.titles
    
    label_uids = Labels.label_uids
    labels = Labels.label_text
    
    # 인자 검사
    if len(documents) < 1:
        error = 'documents len < 1'
    elif len(uids) < 1:
        error = 'uid is not found'
    elif len(titles) < 1:
        error = 'titles is not found'
    elif len(label_uids) < 1:
        error = 'label_uids not found'
    elif len(labels) < 1:
        error = 'labels is not found'
     
    if error != 'success':
        LOGGER.error(f'/embed/es {error}')
        raise HTTPException(status_code=404, detail=error, headers={"X-Error": error},)
          
    # 1. 추출된 문서들 불러와서 df로 만듬
    try:                                                                
        df_contexts = make_docs_df(documents, titles, uids, infilepath)
        LOGGER.info(f'/docs/label 1.load_docs success')
    except Exception as e:
        error = f'load docs fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'/docs/label {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
        
    # 2. 문장 추출
    try:
        doc_sentences = get_sentences(df=df_contexts, remove_sentnece_len=REMOVE_SENTENCE_LEN, remove_duplication=REMOVE_DUPLICATION)
        LOGGER.info(f'/docs/label 2.get_sentences success=>len(doc_sentences):{len(doc_sentences)}')
    except Exception as e:
        error = f'get_sentences fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'/docs/label {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
        
    # 3. faiss 인덱스 생성
    try:
        error, faissindexlist = docs_faiss_index(doc_sentences)
        LOGGER.info(f'/docs/label 3.docs_faiss_index success=>len(faissindexlist):{len(faissindexlist)}')
    except Exception as e:
        error = f'docs_faiss_index fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'/docs/label {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
        
    if error != 'success':
        raise HTTPException(status_code=404, detail=error, headers={"X-Error": error},)
     
    # 4. 라벨로 문서 인덱스에 쿼리하여 최대값을 구함.
    try:
        error, bi_predictions_list = search_label(faiss_index=faissindexlist, label_uids=label_uids, labels=labels)
        LOGGER.info(f'/docs/label 4.search_label success=>len(bi_predictions_list):{len(bi_predictions_list)}')
    except Exception as e:
        error = f'search_label fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'/docs/label {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
      
    if error != 'success':
        raise HTTPException(status_code=404, detail=error, headers={"X-Error": error},)
        
    # 5. 결과값 return
    return {"labels":bi_predictions_list} 