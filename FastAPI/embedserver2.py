#----------------------------------------------------------------------
# FastAPI 이용한 임베딩 서버 예제2
# - 설치 :pip install fastapi[all]
# - python 업데이트(옵션) : conda install -c anaconda python=3.10 (3.10이상 필요)
# - 실행 : uvicorn model1:app --host=0.0.0.0 --port=9000 --limit-concurrency=200
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
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import asyncio
import threading
import httpx
    
# ES 관련
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk

# myutils 관련
import sys
sys.path.append('..')
from myutils import bi_encoder, dense_model, onnx_model, onnx_embed_text
from myutils import seed_everything, GPU_info, mlogging, getListOfFiles, get_options
from myutils import remove_reverse, clean_text, make_max_query_script, make_avg_query_script, make_query_script, create_index, mpower_index_batch
from myutils import embed_text, clustering_embedding, kmedoids_clustering_embedding
from myutils import split_sentences1, make_docs_df, get_sentences, es_delete, es_delete_by_id, es_update, es_search

# FutureWarning 제거
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) 

import openai
from bardapi import Bard
from bardapi import BardCookies

#---------------------------------------------------------------------------
# 전역 변수로 선언 => 함수 내부에서 사용할때 global 해줘야 함.

# FastAPI 서버 관련 
SETTINGS_FILE = './data/settings.yaml'  # 설정파일 경로 (yaml 파일)
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
DATA_FOLDER = settings['env']['DATA_FOLDER']
ENV_URL = settings['env']['URL']
assert DEVICE=='auto' or DEVICE=='cpu', f'DEVICE setting error!!. DEVICE is auto or cpu=>DEVICE:{DEVICE}'
    
LOGGER = mlogging(loggername="embed-server", logfilename=logfilepath) # 로그
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

# ES 관련 전역 변수
ES_URL = settings['es']['ES_URL']
ES_INDEX_FILE = settings['es']['ES_INDEX_FILE'] # 인덱스 파일 경로
Q_METHOD = settings['es']['Q_METHOD']     # 검색시 ES 스크립트 어떤형식으로 만들지.(0=임베딩이 여러개일때 MAX(기본), 1=임베딩이 여러개일때 평균, 2=임베딩이1개일때)
BATCH_SIZE = settings['es']['BATCH_SIZE'] # 배치 사이즈 = 20이면 20개씩 ES에 인덱싱함.
MIN_SCORE = settings['es']['MIN_SCORE']   # 검색 1.30 스코어 이하면 제거

LOGGER.info(f'*ES Settings: ES_URL:{ES_URL}, Q_METHOD:{Q_METHOD}, ES_INDEX_FILE:{ES_INDEX_FILE}, BATCH_SIZE:{BATCH_SIZE}, MIN_SCORE:{MIN_SCORE}')

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

# 검색 관련
# VECTOR_MAG = ES 벡터 크기 값(임의이 값지정) =>벡터의 크기는 각 구성 요소의 제곱 합의 제곱근으로 정의된다.. 
# 예를 들어, 벡터 [1, 2, 3]의 크기는 sqrt(1^2 + 2^2 + 3^2) 즉, 3.7416이 된다.클수록 -> 스코어는 작아짐, 작을수록 -> 스코어 커짐.
VECTOR_MAG = settings['search']['VECTOR_MAG']
LOGGER.info(f'*검색 Settings: VECTOR_MAG:{VECTOR_MAG}')

# 어떤 LLM 모델을 사용할지
LLM_MODEL = settings['llm_model']['model_type']
LOGGER.info(f'*llm_model_type: {LLM_MODEL}(0=sllm, 1=gpt, 2=bard)')

# 프롬프트
PROMPT_CONTEXT = settings['llm_model']['prompt']['prompt_context']  # context 가 있을때(검색된 내용이 있을때)
PROMPT_NO_CONTEXT = settings['llm_model']['prompt']['prompt_no_context']
LOGGER.info(f'*PROMPT_CONTEXT: {PROMPT_CONTEXT}, PROMPT_NO_CONTEXT: {PROMPT_NO_CONTEXT}')

# sLLM 모델
lora_weights = settings['llm_model']['sllm']['lora_weights']
llm_model_path = settings['llm_model']['sllm']['llm_model_path']
uselora_weight = settings['llm_model']['sllm']['uselora_weight']
load_8bit = settings['llm_model']['sllm']['load_8bit']
LOGGER.info(f'--0.*sllm Settings: lora_weights:{lora_weights}, llm_model_path:{llm_model_path}, uselora_weight:{uselora_weight}, load_8bit:{load_8bit}, load_8bit:{load_8bit}')

# BARD 관련
BARD_TOKEN = settings['llm_model']['bard']['BARD_TOKEN']
BARD_1PSIDTS_TOKEN = settings['llm_model']['bard']['BARD_1PSIDTS_TOKEN']
BARD_1PSIDCC_TOKEN = settings['llm_model']['bard']['BARD_1PSIDCC_TOKEN']
LOGGER.info(f'*--1.bard Settings: BARD_TOKEN:{BARD_TOKEN}, BARD_1PSIDTS_TOKEN:{BARD_1PSIDTS_TOKEN}, BARD_1PSIDCC_TOKEN:{BARD_1PSIDCC_TOKEN}')

# GPT 관련
GPT_TOKEN = settings['llm_model']['gpt']['GPT_TOKEN']
GPT_MODEL = settings['llm_model']['gpt']['GPT_MODEL']
LOGGER.info(f'*--2.bard Settings: GPT_MODEL:{GPT_MODEL}')
            
# GPT 관련 값
# **key 지정
openai.api_key = GPT_TOKEN
# 모델 - GPT 3.5 Turbo 지정
# => 모델 목록은 : https://platform.openai.com/docs/models/gpt-4 참조
gpt_model = GPT_MODEL  #"gpt-4"#"gpt-3.5-turbo" #gpt-4-0314

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
  
# 모델 저장
#output_path = "../../data11/model/kpf-sbert-128d-v1"
#BI_ENCODER1.save(output_path)
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# sLLM 모델 로딩
#---------------------------------------------------------------------------
if llm_model_path:
    try:
        start_time = time.time()

        # tokenizer 로딩
        sllmtokenizer = transformers.AutoTokenizer.from_pretrained(llm_model_path)

        # 원본 모델 로딩
        sllmmodel = transformers.AutoModelForCausalLM.from_pretrained(llm_model_path, load_in_8bit=load_8bit, torch_dtype=torch.float16, device_map="auto")

        if uselora_weight:
            sllmmodel = PeftModel.from_pretrained(sllmmodel, lora_weights, torch_dtype=torch.float16) # loRA 모델 로딩

        if not load_8bit:
            sllmmodel.half()

        sllmmodel.eval()

        end_time = time.time() - start_time
        print("load sllm model time: {:.2f} ms\n".format(end_time * 1000)) 
        print(sllmmodel)
    except Exception as e:
        LOGGER.error(f'sllm load fail({llm_model_path})=>{e}')
        assert False, f'sllm load fail({llm_model_path})=>{e}'
        
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

    clustering_num = NUM_CLUSTERS
        
    docs = []
    count = 0
    for i, sentences in enumerate(tqdm(doc_sentences)):
        embeddings = embedding(sentences)
        if i < 3:
            print(f'[{i}] sentences-------------------')
            if len(sentences) > 5:
                print(sentences[:5])
            else:
                print(sentences)
                
        LOGGER.info(f'*[index_data] embeddings.shape: {embeddings.shape}')
        print()
        
        #----------------------------------------------------------------
        multiple = 1
        
        # [bong][2023-04-28] 임베딩 출력 계수에 따라 클러스터링 계수를 달리함.
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
            clustering_num = 1  # 평균값일때는 NUM_CLUSTERS=1로 해줌.
        # 2=문장임베딩
        else:
            emb = embeddings

        LOGGER.info(f'*[index_data] cluster emb.shape: {emb.shape}')
        print()
        
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

            if count % BATCH_SIZE == 0:
                mpower_index_batch(es, ES_INDEX_NAME, docs, vector_len=clustering_num, dim_size=dimension)
                docs = []
                LOGGER.info("[index_data](1) Indexed {} documents.".format(count))

    if docs:
        mpower_index_batch(es, ES_INDEX_NAME, docs, vector_len=clustering_num, dim_size=dimension)
        LOGGER.info("[index_data](2) Indexed {} documents.".format(count))   

    es.indices.refresh(index=ES_INDEX_NAME)

    LOGGER.info(f'*인덱싱 시간 : {time.time()-start:.4f}\n')
    print()
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# ES 임베딩 벡터 쿼리 실행 함수
# - in : esindex=인덱스명, query=쿼리 , search_size=검색출력계수
# - option: qmethod=0 혹은 1 혹은 2(0=max벡터 구하기, 1=평균벡터 구하기, 2=임베딩벡터가 1개인 경우 (default=0)), uid_list=검색할 uid 리스트(*엠파워에서는 검색할 문서id를 지정해서 검색해야 검색속도가 느리지 않음)
#---------------------------------------------------------------------------
def es_embed_query(esindex:str, query:str, search_size:int, qmethod:int=0, uids:list=None):
    
    error: str = 'success'
    
    query = query.strip()
    
    #print(f'search_size: {search_size}')
    
    # 1.elasticsearch 접속
    es = Elasticsearch(ES_URL)   
    
    if not query:
        error = 'query is empty'
    elif search_size < 1:
        error = 'search_size < 1'
    elif not es.indices.exists(esindex):
         error = 'esindex is not exist'
    elif qmethod < 0 or qmethod > 2:
        error = 'qmenthod is not variable'
    
    if error != 'success':
        LOGGER.error(f'[es_embed_query] {error}')
        return error, None
        
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
    if qmethod == 0:
        script_query = make_max_query_script(query_vector=embed_query[0], vectormag=VECTOR_MAG, vectornum=10, uid_list=uids) # max 쿼리를 만듬.
    elif qmethod == 1:
        script_query = make_avg_query_script(query_vector=embed_query[0], vectormag=VECTOR_MAG, vectornum=10, uid_list=uids) # 평균 쿼리를 만듬.
    else:
        script_query = make_query_script(query_vector=embed_query[0], uid_list=uids) # 임베딩 벡터가 1개인경우=>기본 쿼리 만듬.
        
    #print(script_query)
    #print()

    # 4. 실제 ES로 검색 쿼리 날림
    response = es.search(
        index=esindex,
        body={
            #"size": search_size * 3, # 3배 정도 얻어옴
            "size": search_size,
            "query": script_query,
            "_source":{"includes": ["rfile_name","rfile_text"]}
        }
    )
    
    #LOGGER.info(f'[es_embed_query] response:{response}')

    # 5. 결과 리턴
    # - 쿼리 응답 결과값에서 _id, _score, _source 등을 뽑아내고 내림차순 정렬후 결과값 리턴
    #print(response)
    
    rfilename = []
    count = 0
    docs = []
    for hit in response["hits"]["hits"]: 
        tmp = hit["_source"]["rfile_name"]
        
        # 중복 제거
        if tmp and tmp not in rfilename:
            rfilename.append(tmp)
            doc = {}  #dict 선언
            doc['rfile_name'] = hit["_source"]["rfile_name"]      # contextid 담음
            doc['rfile_text'] = hit["_source"]["rfile_text"]      # text 담음.
            doc['score'] = hit["_score"]
            docs.append(doc)
            
            count += 1
            if count >= search_size:
                break
                
    LOGGER.info(f'[es_embed_query] query:{query} docs:{docs}')

    return error, docs # 쿼리,  rfilename, rfiletext, 스코어 리턴 

#---------------------------------------------------------------------------
# 비동기 ES 임베딩 벡터 쿼리 실행 함수
#---------------------------------------------------------------------------
async def async_es_embed_query(esindex:str, query:str, search_size:int, qmethod:int, uids:list=None):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, es_embed_query, esindex, query, search_size, qmethod, uids)
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# ES 임베딩 도큐먼트 삭제 함수
# -> 삭제할 _id를 얻어와서 삭제함.
# - in : esindex=인덱스명, rfile_name=파일 유니크한 값(sfileid, contxtsid) 
#---------------------------------------------------------------------------
def es_embed_delete(esindex:str, rfile_name:str):
    
    error: int = 0
    
    # 1.elasticsearch 접속
    es = Elasticsearch(ES_URL)   
        
    data = {'rfile_name': rfile_name}
    
    # 2. 쿼리 검색후 _id 얻어옴.
    id_list = []
    res=es_search(es, index_name=esindex, data=data)
    for hits in res['hits']['hits']:
        esid=hits['_id']
        #print(f'id:{esid}')
        id_list.append(esid)
        
    # 3. 삭제함.
    if len(id_list) > 0:  
        for id in id_list:
            print(f'id:{id}')
            res=es_delete_by_id(es, index_name=esindex, id=id)
            print(f'res:{res}')
            
        return 0
    else:
        return 1002
#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
# 비동기 ES 임베딩 도큐먼트 삭제 함수
#---------------------------------------------------------------------------
async def async_es_embed_delete(esindex:str, rfile_name:str):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, es_embed_delete, esindex, rfile_name)
#---------------------------------------------------------------------------

#------------------------------------------------------------------------
# PROMPT 생성
#------------------------------------------------------------------------
def make_prompt(docs, query):
     # prompt 구성
    context:str = ''

    for doc in docs:
        score = doc['score']
        if score > MIN_SCORE:
            rfile_text = doc['rfile_text']
            if rfile_text:
                context += rfile_text + '\n\n'
                
    if context:
        prompt = PROMPT_CONTEXT.format(query=query, context=context)
    else:
        prompt = PROMPT_NO_CONTEXT.format(query=query)
        '''
        if LLM_MODEL == 0:  #SLLM 모델일때 
            prompt = PROMPT_NO_CONTEXT.format(query=query)
        else:   # GPT 혹은 BARD인 경우, context가 없으면  프롬프트는 쿼리만 생성함.
            prompt = query
        '''  
    return prompt, context
#------------------------------------------------------------------------

#---------------------------------------------------------------------------
# 비동기 PROMPT 생성
#---------------------------------------------------------------------------
async def async_make_prompt(docs, query:str):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, make_prompt, docs, query)
#---------------------------------------------------------------------------

#------------------------------------------------------------------------
# sLLM 이용한 text 생성
#------------------------------------------------------------------------
def generate_text_sLLM(prompt):
    
    max_new_tokens = 256
    eos_str = sllmtokenizer.decode(sllmtokenizer.eos_token_id)
    start_time = time.time()
    #print(f'eos_str:{eos_str}')
    
    #prompt = query
    #prompt = f"### 질문: {input_text}\n\n### 맥락: {context}\n\n### 답변:" if context else f"### 질문: {input_text}\n\n### 답변:"
    #prompt = f"### 질문 : 간략히 답변해줘.{query}\r\n###답변:"
    #prompt = f"### 질문: {query}\n\n### 답변:"
    #print(prompt)

    # config 설정
    generation_config = GenerationConfig(
        temperature=0.5,
        top_p=0.75,
        top_k=40,
        num_beams=1,
        bos_token_id=sllmtokenizer.bos_token_id,  # 시작토큰 
        eos_token_id=sllmtokenizer.eos_token_id,  # end 토큰
        pad_token_id=sllmtokenizer.pad_token_id   # padding 토큰
    )

    # 프롬프트 tokenizer 
    inputs = sllmtokenizer(prompt, return_tensors="pt").to(DEVICE)
    input_ids = inputs["input_ids"]
    #print(input_ids)
       
    # Without streaming
    # generate 처리
    with torch.no_grad():
        generation_output = sllmmodel.generate(
            input_ids=input_ids,
            generation_config=generation_config,
            return_dict_in_generate=True,
            output_scores=False,
            max_new_tokens=max_new_tokens,
        )

    # 출력
    s = generation_output.sequences[0]
    output = sllmtokenizer.decode(s)

    end_time = time.time() - start_time
    print("*Text생성시간: {:.2f} ms\n".format(end_time * 1000)) 
    #print(output.replace(eos_str, ''))
    #print()
    return output.replace(eos_str, '')
#------------------------------------------------------------------------

#------------------------------------------------------------------
# 구글 bard를 이용한 text 생성
#
# 세션키를 이용하여 구글 bard 테스트 예제
# 출처 : https://github.com/dsdanielpark/Bard-API
#
# token 값얻기
# https://bard.google.com/ 방문
# 콘솔용 F12
# 세션: 애플리케이션 → 쿠키 → 쿠키 값을 복사합니다 __Secure-1PSID.
# -> 참고로 반드시 뒤에 .으로 끝나고 .포함해서 길이가 72자임.
#------------------------------------------------------------------
from bardapi import BardCookies
#token = 'XQhPmzE3Wa_GqgDH1Z9YcRwZieE0STZi0ANZ557Zcm9Lio8QeIQtQvdd8evImbUrF-ZapQ.' # bard __Secure-1PSID 토큰 입력
#token1 = 'XQhPmzE3Wa_GqgDH1Z9YcRwZieE0STZi0ANZ557Zcm9Lio8QeIQtQvdd8evImbUrF-ZapQ.' # bard __Secure-1PSIDTS 토큰 입력
def generate_text_bard(prompt:str, token:str, token1:str=None, token2:str=None):
    #print(f'[generate_text_bard] prompt: {prompt}')
    print(f'[generate_text_bard] token: {token}, token1: {token1}, token2:{token2}')
   
    assert token, f'token is not empty'
    
    token = token.strip()
    
    # __Secure-1PSID 토큰만 이용하는 경우 "SNlM0e value not found. Double-check __Secure-1PSID value or pass it as token='xxxxx'" 에러가 자주 발생하여,
    # __Secure-1PSIDTS 함께 이용하는 멀티토큰 방식으로 함. (출처 : https://github.com/dsdanielpark/Bard-API/issues/99)
    if token1 and token2:
        token1 = token1.strip()
        token2 = token2.strip()
        cookie_dict = {
            "__Secure-1PSID": token,
            "__Secure-1PSIDTS": token1,
            "__Secure-1PSIDCC": token2,
            # Any cookie values you want to pass session object.
        }
        
        bard = BardCookies(cookie_dict=cookie_dict)
    else:
        bard = Bard(token=token,timeout=30) # Set timeout in seconds
        
    output = bard.get_answer(prompt)['content']
    
    #print(f'[generate_text_bard] output: {output}')
    return output
#------------------------------------------------------------------

#-----------------------------------------
# GPT를 이용한 text 생성
#-----------------------------------------
MESSAGES:list = []
def generate_text_GPT(prompt, messages):
    
    #print(f'len(messages):{len(messages)}') 
    #print()
    
    #-----------------------------------------
    # *** gpt에 메시지는 계속 대화 내용이 유지가 되므로, 비용이 발생함.
    # 따라서 최근 2개 대화만 유지함.
    #if len(messages) >= 2:
    #    messages = messages[len(messages)-2:]  # 최근 2개의 대화만 가져오기
    messages = []  # 무조건 최근대화 초기화
    #-----------------------------------------
        
    # 사용자 메시지 추가
    messages.append( {"role": "user", "content": prompt})
    print(messages)

    # ChatGPT-API 호출하기
    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=messages,
        max_tokens=512, # 토큰 수 
        temperature=1,  # temperature 0~2 범위 : 작을수록 정형화된 답변, 클수록 유연한 답변(2는 엉뚱한 답변을 하므로, 1.5정도가 좋은것 같음=기본값은=1)
        top_p=0.1, # 기본값은 1 (0.1이라고 하면 10% 토큰들에서 출력 토큰들을 선택한다는 의미)
        frequency_penalty=0.5, # 일반적으로 나오지 않는 단어를 억제하는 정도
        presence_penalty=0.5 # 동일한 단어나 구문이 반복되는 것을 억제하는 정도
        #stop=["다.","다!"] # . 나오면 중단
    )

    #print(response)
    #print()
    #answer = response['choices'][0]['message']['content'] + '다.' # 뒤에 '다' 붙여줌.
    answer = response['choices'][0]['message']['content']
    return answer
#------------------------------------------------------------------

#---------------------------------------------------------------------------
# 이전 답변/응답 문장들중 오래된것 제거하며, 문장을 구분자 <hr> 로 구분해서 답변/응답 문단을 만든는 함수
#---------------------------------------------------------------------------
def remove_prequery(prequery:str, remove_count:int=4):
    
    if prequery:
        # prequery는 5개 이상이면 무조건 오래된 문장/답변은 제거함
        hr_count = prequery.count("<hr>")
        #print(f'4) hr_count:{hr_count}')

        remove_count -= 1
        if hr_count > remove_count: # 4 개 이상이면 <hr>로 구분해서 오래된 문장/답변은 제거함.
            hr_list = prequery.split("<hr>") # <hr>로 구분
            hr_list.pop(0)                   # 제일 오래된 <hr> 구분해서 첫번째 문장/답변은 제거.
            prequery = "<hr>".join(hr_list)  # 다시 hr 구분된 문장/답변 조합.
            #print(f'5) prequery:{prequery}')
    
    return prequery
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# context 문자열을 입력받아서,\n\n 문단으로 구분후, 문단 맨 첫번째 문장 title들을
# 조합해서 title_str 만들고 ,return 하는 함수
# -> title에 해당하는 문서가 있으면 url링크 생성함
#---------------------------------------------------------------------------
def get_title_with_urllink(context:str):
    
    titles_str:str = ''  # titles를 str형으로 만들어서 전송함. 
    
    # context에서 title만 뽑아냄
    titles = []
    context_list = context.split("\n\n")  #\n\n으로 구분.
    for context1 in context_list:
        context1 = context1.strip()
        context2 = context1.split("\n")
        if len(context2) > 0:
            titles.append(context2[0].strip())
    
    # 중복 제거하면서 순서유지.
    titles2 = []
   
    for idx, title in enumerate(titles):
        if title and title not in titles2:
            titles2.append(title)
            
            # 실제 title에 해당하는 파일이 경로에 존재하는 경우에만 url 링크 생성함.
            if os.path.isfile(DATA_FOLDER + title + ".txt"):
                
                # html뿌릴때 중간에 쌍따옴표가 있으면 에러 나므로, "(쌍따옴표) 대신에 ;s&s; 로 치환해서 전송함. 
                # => 이후 chat01.html에서 ;s&s; 문자열을 다시 "(쌍따옴표)로 치환해줌.
                # => 참고로 " 대신에 홑따옴표(') 해도 되는데, openPopup 함수는 반드시 "(쌍따옴표)로 묶어져야 동작하므로 이렇게 처리함.
                title = f"<a href='javascript:void(0);' onclick=;s&s;;openPopup('{ENV_URL}/doc?name={title}');;s&s;>{title}</a>"
                #title = f"<a href='/doc?name={title}'>{title}</a>"
                
            if idx == 0:
                titles_str = title
            else:
                titles_str += ', ' + title
                
    return titles_str
#---------------------------------------------------------------------------

#------------------------------------------------------------------
# BERT로 문단 검색 후 sLLM 로 Text 생성.
#------------------------------------------------------------------
def search_docs(esindex:str, query:str, search_size:int, llm_model_type:int=0, model_key:str='', model_key1:str='', model_key2:str='', qmethod:int=0, checkdocs:bool=True):
    error:str = 'success'
    
    assert query, f'query is empty'
    assert esindex, f'esindex is empty'
    
    query = query.strip()
    esindex = esindex.strip()
    #print(f'model_key:{model_key}')
    
    if model_key:
        model_key = model_key.strip()
        #print(f'model_key:{model_key}')
    
    LOGGER.info(f'[search_docs] esindex:{esindex}, query:{query}, search_size:{search_size}, llm_model_type:{llm_model_type}, model_key:{model_key}')
    
    query_split = query.split('##')
    prefix = query_split[0]  
    docs = []
    response:str = '질문에 대한 답을 찾지 못했습니다. 다시 질문해 주세요'
    embed_context:str = ''
    bllm_model_query = True # True이면 llm_model 쿼리함.
    
    if checkdocs == False: # 회사문서검색 체크하지 않으면 그냥 쿼리 그대로 prompt 설정함.
        query1=query
        #prompt=query1
        prompt, embed_context = make_prompt(docs='', query=query1)   
    elif prefix == '@':  # 일반쿼리일때는 @## prefix 입력후 질문입력함. 
        query1 = query_split[1]
        #prompt=query1
        prompt, embed_context = make_prompt(docs='', query=query1)   
        LOGGER.error(f'[search_docs]: prefix: {prefix}\n')
    else:
        query1 = query
        
        # es로 임베딩 쿼리 실행
        try:
            error, docs = es_embed_query(esindex, query1, search_size, qmethod)
        except Exception as e:
            error = f'es_embed_query fail'
            msg = f'{error}=>{e}'
            LOGGER.error(f'[search_docs]: {msg}\n')
            raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
         
        # 검색된 문단들 출력
        print(docs)
        print()
        
        # prompt 생성    
        prompt, embed_context = make_prompt(docs=docs, query=query1)
        if len(embed_context) < 2:
            bllm_model_query = False
            
    LOGGER.info(f'[search_docs] prompt:{prompt}, bllm_model_query:{bllm_model_query}')
  
    # llm_model_query == True일때만 쿼리함.
    if bllm_model_query == True:
        # sllM으로 text 생성
        try:
            if llm_model_type == 0:
                response = generate_text_sLLM(prompt=prompt)
            elif llm_model_type == 1:
                response = generate_text_GPT(prompt=prompt, messages=MESSAGES)
            elif llm_model_type == 2: # bard 일때
                response = generate_text_bard(prompt=prompt, token=model_key, token1=model_key1, token2=model_key2)
        except Exception as e:
            error = f'generate_text_xxx fail=>model:{llm_model_type}'
            msg = f'{error}=>{e}'
            LOGGER.error(f'[search_docs]: {msg}\n')
            raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)

        if error != 'success':
            raise HTTPException(status_code=404, detail=error, headers={"X-Error": error},)
     
    # sllm모델일때
    if llm_model_type == 0:
        # 응답을 파싱해서 응답만 뽑아내서 return 함.
        answer:str = "답변 없음."
        answers:list = []
        questions:list = []
        contexts:list = []
        context:str = ""

        #print(f'response')
        #print(response)

        # 프롬프트에 따라 응답, 질의 ,문단으로 파싱하는 함수.
        if response:
            answers = response.split("###응답:")
            #print(answer[0])
            #print()
            questions = answers[0].split("###질의:")
            #print(questions[0])
            #print()
            contexts = questions[0].split("###문서:")
            #print(contexts[1])
            #print()

            if len(answers) > 1:
                answer = answers[1].strip()

            if len(contexts) > 1:
                context = contexts[1].strip()

            query = query1
            
            if context == '':
                context = '**질문과 관련된 회사 자료를 찾지 못했습니다.**'
                
            LOGGER.info(f'[search_docs] answer:{answer}')
  
        return query, answer, context
           
    # gpt 혹은 bard일때
    if llm_model_type == 1 or llm_model_type == 2:
        query = query1
        answer = response
        context:str = ''
        
        '''
        if checkdocs == True:
            if len(docs) > 0:
                for doc in docs:
                    score = doc['score']
                    if score > MIN_SCORE:
                        rfile_text = doc['rfile_text']
                        if rfile_text:
                            context += rfile_text + '\n\n'
        '''
        LOGGER.info(f'[search_docs] answer:{answer}')
        return query, answer, embed_context
    
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# 비동기 BERT로 문단 검색 후 LLM모델 로 Text 생성.
#---------------------------------------------------------------------------
async def async_search_docs(esindex:str, query:str, search_size:int, llm_model_type:int=0, model_key:str='', model_key1:str='', model_key2:str='', qmethod:int=0, checkdocs:bool=True):
    loop = asyncio.get_running_loop()
    #print(f'[async_search_docs] esindex :{esindex}')
    ##print(f'[async_search_docs] query :{query}')
    #print(f'[async_search_docs] llm_model_type :{llm_model_type}')
    #print(f'[async_search_docs] model_key :{model_key}')
    
    return await loop.run_in_executor(None, search_docs, esindex, query, search_size, llm_model_type, model_key, model_key1, model_key2, qmethod, checkdocs)

    
# http://10.10.4.10:9000/docs=>swagger UI, http://10.10.4.10:9000/redoc=>ReDoc UI 각각 비활성화 하려면
# => docs_url=None, redoc_url=None 하면 된다.
#app = FastAPI(redoc_url=None) #FastAPI 인스턴스 생성(*redoc UI 비활성화)
app = FastAPI()
templates = Jinja2Templates(directory="templates") # html 파일이 있는 경로를 지정.

#=========================================================
# 카카오 쳇봇 연동 테스트 
# - 임베딩 비교하여 가장 적합한 문서 리턴
#=========================================================
@app.post("/chatbot")
async def chabot(content: Dict):
    #user_id = content["userRequest"]["user"]["id"]  # id
    query = content["userRequest"]["utterance"]  # 질문
    content1 = content["userRequest"]
    LOGGER.info(f'/test-----\content1:{content1}')

    #text = "답변\n" + question 
    #LOGGER.info(f'/test-----\text:{text}')

    search_size = 2      # 검색 계수
    esindex = "qaindex"  # qaindex
    checkdocs = True     # True = index 검색 / False = index 검색 안하고, 바로 LLM 응답함
    
    LOGGER.info(f'/test-----\query:{query}, search_size:{search_size}, esindex:{esindex}, checkdocs:{checkdocs}, LLM_MODEL:{LLM_MODEL}, Q_METHOD:{Q_METHOD}')
    
    # es로 임베딩 쿼리 실행
    try:
        error, docs = es_embed_query(esindex, query, search_size, Q_METHOD)
    except Exception as e:
        error = f'es_embed_query fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'[search_docs]: {msg}\n')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
        
    #LOGGER.info(f'/test-----\question:{question}, answer:{answer}')
    
    context:str = ''

    for doc in docs:
        score = doc['score']
        if score > MIN_SCORE:
            rfile_text = doc['rfile_text']
            if rfile_text:
                 context += rfile_text+'\n['+str(score)+']' + '\n\n'  # 내용과 socore 출력
                
    if len(context) < 5:
        context = '질문에 맞는 답변을 찾지 못했습니다.'
        
    # 답변 테긋트 설정
    content = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": context
                    }
                }
            ]
        }
    }
    
    return JSONResponse(content=content)


async def call_callback(callback_url, query1):
    async with httpx.AsyncClient() as client:
        #api_response = await client.get("https://some-api.com/data")
        #api_data = api_response.json()
        
        start_time = time.time()
        callbackurl = callback_url
        query = "답변:" + query1
        
        LOGGER.info(f'callback-----query:{query}, callbackurl:{callbackurl}')
        
        search_size = 2      # 검색 계수
        esindex = "qaindex"  # qaindex
        checkdocs = False     # True = index 검색 / False = index 검색 안하고, 바로 LLM 응답함

        LOGGER.info(f'/callback-----\query:{query}, search_size:{search_size}, esindex:{esindex}, checkdocs:{checkdocs}, LLM_MODEL:{LLM_MODEL}, Q_METHOD:{Q_METHOD}')

        if LLM_MODEL == 0:       # SLLM
            question, answer, context1 = await async_search_docs(esindex, query, search_size, llm_model_type=0, model_key='', model_key1='', model_key2='', qmethod=Q_METHOD, checkdocs=checkdocs)
        elif LLM_MODEL == 1:     # gpt
            question, answer, context1 = await async_search_docs(esindex, query, search_size, llm_model_type=1, model_key='', model_key1='', model_key2='', qmethod=Q_METHOD, checkdocs=checkdocs)
        elif LLM_MODEL == 2:     # GPT
            question, answer, context1 = await async_search_docs(esindex, query, search_size, llm_model_type=2, model_key=BARD_TOKEN, model_key1=BARD_1PSIDTS_TOKEN, model_key2=BARD_1PSIDCC_TOKEN, qmethod=Q_METHOD, checkdocs=checkdocs)

        #LOGGER.info(f'/test-----\question:{question}, answer:{answer}')

        # 소요된 시간을 계산합니다.
        end_time = time.time()
        elapsed_time = end_time - start_time

        answer += '\n(' + str(elapsed_time) + ')'   # 응답시간 추가
    
        callback_response = await client.post(
            callbackurl,
            json={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": answer
                            }
                        }
                    ]
                }
            }
        )
        
        LOGGER.info(f"callback_response:{callback_response}")

        if callback_response.status_code == 200:
            LOGGER.info("Callback 호출 성공")
        else:
            LOGGER.info(f"Callback 호출 실패: {callback_response.status_code}")
        
        
@app.post("/chatbot3")
async def chabot3(content: Dict):
    query = content["userRequest"]["utterance"]  # 질문
    callbackurl = content["userRequest"]["callbackUrl"] # callbackurl
    
    content1 = content["userRequest"]
    LOGGER.info(f'/test-----\content1:{content1}')
    
    # 비동기 작업을 스케줄링
    asyncio.create_task(call_callback(callbackurl, query))
    
    LOGGER.info(f'chabot3-----query:{query}, callbackurl:{callbackurl}')
    
     # 답변 테긋트 설정
    content = {
        "version": "2.0",
        "useCallback": True,
        "data": {
           "text" : "답변을 찾는중 이에요😘 \n15초 정도 걸릴것 같아요. 잠시만 기다려주세요!"
        }
    }
    
    return JSONResponse(content=content)
   
#=========================================================
# 카카오 쳇봇 연동 테스트 2. 
#=========================================================
@app.post("/chatbot2")
async def chabot2(content: Dict):
       
    start_time = time.time()
    
    query = content["userRequest"]["utterance"]  # 질문
    callback_url = content["userRequest"]["callbackUrl"] # callbackurl
    
    content1 = content["userRequest"]
    LOGGER.info(f'/test-----\content1:{content1}')

    search_size = 2      # 검색 계수
    esindex = "qaindex"  # qaindex
    checkdocs = False     # True = index 검색 / False = index 검색 안하고, 바로 LLM 응답함
    
    LOGGER.info(f'/test-----\query:{query}, search_size:{search_size}, esindex:{esindex}, checkdocs:{checkdocs}, LLM_MODEL:{LLM_MODEL}, Q_METHOD:{Q_METHOD}')
    
    if LLM_MODEL == 0:       # SLLM
        question, answer, context1 = await async_search_docs(esindex, query, search_size, llm_model_type=0, model_key='', model_key1='', model_key2='', qmethod=Q_METHOD, checkdocs=checkdocs)
    elif LLM_MODEL == 1:     # gpt
        question, answer, context1 = await async_search_docs(esindex, query, search_size, llm_model_type=1, model_key='', model_key1='', model_key2='', qmethod=Q_METHOD, checkdocs=checkdocs)
    elif LLM_MODEL == 2:     # GPT
        question, answer, context1 = await async_search_docs(esindex, query, search_size, llm_model_type=2, model_key=BARD_TOKEN, model_key1=BARD_1PSIDTS_TOKEN, model_key2=BARD_1PSIDCC_TOKEN, qmethod=Q_METHOD, checkdocs=checkdocs)
        
    #LOGGER.info(f'/test-----\question:{question}, answer:{answer}')
    
    # 소요된 시간을 계산합니다.
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    answer += '(' + str(elapsed_time) + ')'   # 응답시간 추가
    
    # 답변 테긋트 설정
    content = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                }
            ]
        }
    }
    
    return JSONResponse(content=content)
    
#=========================================================
# 루트=>정보 출력
# => http://127.0.0.1:9000/
#=========================================================
@app.get("/")
async def root():
    return {"서버": "문서임베딩AI API 서버", 
            "*임베딩모델":{"모델경로": MODEL_PATH, "폴링방식((mean=평균값, cls=문장대표값, max=최대값)": POLLING_MODE, "출력차원(128, 0=768)": OUT_DIMENSION,"임베딩방식(0=문장클러스터링, 1=문장평균임베딩, 2=문장임베딩)": EMBEDDING_METHOD, "출력벡터타입('float32', 'float16')": FLOAT_TYPE},
            "*ES서버":{"URL":ES_URL, "인덱스파일경로": ES_INDEX_FILE, "최소스코어": MIN_SCORE, "배치크기": BATCH_SIZE, "검색스크립트((0=임베딩이 여러개일때 MAX(기본), 1=임베딩이 여러개일때 평균, 2=임베딩이1개일때))": Q_METHOD},
            "*클러스터링":{"클러스터링 가변(True=문장계수에 따라 클러스터링계수를 다르게함)": NUM_CLUSTERS_VARIABLE, "방식(kmeans=k-평균 군집 분석, kmedoids=k-대표값 군집 분석)": CLUSTRING_MODE, "계수": NUM_CLUSTERS, "출력(mean=평균벡터 출력, max=최대값벡터출력)": OUTMODE},
            "*문장전처리":{"제거문장길이(설정길이보다 작은 문장은 제거됨)": REMOVE_SENTENCE_LEN, "중복문장제거(True=중복된문장은 제거됨)": REMOVE_DUPLICATION},
            "*검색":{"*검색비교벡터값": VECTOR_MAG},
            "*LLM":{"모델타입(0=SLLM, 1=GPT, 2=BARD)":LLM_MODEL },
            "*프롬프트":{"컨텍스트 O": PROMPT_CONTEXT, "컨텍스트 X": PROMPT_NO_CONTEXT}
            }

#=========================================================
# GET : 입력 문장 리스트에 대한 임베딩값 리턴(비동기)
# => http://127.0.0.1:9000/vectors?sentence="오늘은 비가 온다"&sentence="오늘은 날씨가 좋다"
# - in : 문장 리스트 (예: ['오늘 날씨가 좋다', '내일은 비가 온다'] )
# - out: 문장 리스트에 대한 임베딩 벡터
#=========================================================
@app.get("/vectors", status_code=200)
async def get_vector(sentences: List[str] = Query(..., description="sentences", min_length=1, max_length=255, alias="sentence")):

    # embedding 함수를 async 함수로 wrapping한 async_embedding 함수를 실행합니다.
    try:
        embeddings = await async_embedding(sentences)
    except Exception as e:
        error = f'async_embedding fail({ES_URL})'
        msg = f'{error}=>{e}'
        LOGGER.error(f'/vectors {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
        
    embeddings_str = [",".join(str(elem) for elem in sublist) for sublist in embeddings]
    return {"vectors": embeddings_str}

#=========================================================
# POST: es/{인덱스명}/docs (입력 docs(문서)에 대한 임베딩값 구하고 ElasticSearch(이하:ES) 추가.(동기))
# => http://127.0.0.1:9000/es/{인덱스명}/docs
# - in : docs: 문서 (예: ['오늘 날씨가 좋다', '내일은 비가 온다'] ), titles: 문서제목, uids(문서 고유id)
# - in : esindexname : ES 인덱스명, createindex=True(True=무조건 인덱스생성. 만약 있으면 삭제후 생성/ Flase=있으면 추가, 없으면 생성)
# - in : infilepath : True이면 documnets에 filepath 입력되고, 이때는 file를 로딩함. False이면 documents로는 문서내용이 들어옴.
# - out: ES 성공 실패??
#=========================================================
class DocsEmbedIn(BaseModel):
    uids: list       # uid(문서 고유id)->rfilename
    titles: list     # 제목->rfiletext
    documents: list  # 문서내용 혹은 file 경로 (infilepath=True이면, filepath 입력됨)

@app.post("/es/{esindex}/docs")
def embed_documents(esindex:str, Data:DocsEmbedIn, infilepath:bool=False, createindex:bool=False):
    error:str = 'success'
        
    documents = Data.documents
    uids = Data.uids
    titles = Data.titles
    
    # 전역변수로 ES 인덱스명 저장해 둠.
    global ES_INDEX_NAME
    ES_INDEX_NAME = esindex
    
    LOGGER.info(f'/es/{esindex}/docs start-----\nES_URL:{ES_URL}, esindex:{esindex}, createindex:{createindex}, uids:{uids}, titles:{titles}')

    # 인자 검사
    if len(documents) < 1:
        error = 'documents len < 1'
    elif len(uids) < 1:
        error = 'uid not found'
    elif len(titles) < 1:
        error = 'titles not found'
    elif not esindex:
        error = 'esindex not found'
     
    if error != 'success':
        LOGGER.error(f'/embed/es {error}')
        raise HTTPException(status_code=404, detail=error, headers={"X-Error": error},)
    
    # 1.elasticsearch 접속
    try:
        es = Elasticsearch(ES_URL)
        LOGGER.info(f'/embed/es 1.Elasticsearch connect success=>{ES_URL}')
    except Exception as e:
        error = f'Elasticsearch connect fail({ES_URL})'
        msg = f'{error}=>{e}'
        LOGGER.error(f'/embed/es {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
        
    #LOGGER.info(f'es.info:{es.info()}')

    # 2. 추출된 문서들 불러와서 df로 만듬
    try:                                                                
        df_contexts = make_docs_df(documents, titles, uids, infilepath)
        LOGGER.info(f'/embed/es 2.load_docs success')
    except Exception as e:
        error = f'load docs fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'/embed/es {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
                                                                    
    # 3. 문장 추출
    try:
        doc_sentences = get_sentences(df=df_contexts, remove_sentnece_len=REMOVE_SENTENCE_LEN, remove_duplication=REMOVE_DUPLICATION)
        LOGGER.info(f'/embed/es 3.get_sentences success=>len(doc_sentences):{len(doc_sentences)}')
    except Exception as e:
        error = f'get_sentences fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'/embed/es {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
   
    # 4.ES 인덱스 생성
    try:
        create_index(es, ES_INDEX_FILE, ES_INDEX_NAME, createindex)
        LOGGER.info(f'/embed/es 4.create_index success=>index_file:{ES_INDEX_FILE}, index_name:{ES_INDEX_NAME}')
    except Exception as e:
        error = f'create_index fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'/embed/es {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)

    # 5. index 처리
    try:
        index_data(es, df_contexts, doc_sentences)
        LOGGER.info(f'/embed/es 5.index_data success\nend-----\n')
    except Exception as e:
        error = f'index_data fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'/embed/es {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
#=========================================================

#=========================================================
# GET : es/{인덱스명}/docs 검색(비동기)
# => http://127.0.0.1:9000/es/{인덱스}/docs?query=쿼리문장&search_size=5
# - in : query=쿼리할 문장, search_size=검색계수(몇개까지 검색 출력 할지)
# - out: 검색 결과(스코어, rfile_name, rfile_text)
#=========================================================

@app.get("/es/{esindex}/docs")
async def search_documents(esindex:str, 
                     query: str = Query(..., min_length=1),     # ... 는 필수 입력 이고, min_length=1은 최소값이 1임. 작으면 422 Unprocessable Entity 응답반환됨
                     search_size: int = Query(..., gt=0),       # ... 는 필수 입력 이고, gt=0은 0보다 커야 한다. 작으면 422 Unprocessable Entity 응답반환됨
                     qmethod: int=0,                            # option: qmethod=0 혹은 1(0=max벡터 구하기, 1=평균벡터 구하기 (default=0))
                     ):                          
                    
      
    error:str = 'success'
    query = query.strip()
    LOGGER.info(f'\nget /es/{esindex}/docs start-----\nquery:{query}, search_size:{search_size}')
    
    try:
        # es로 임베딩 쿼리 실행
        error, docs = await async_es_embed_query(esindex, query, search_size, qmethod)
    except Exception as e:
        error = f'async_es_embed_query fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'get /es/{esindex}/docs {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
    
    if error != 'success':
        raise HTTPException(status_code=404, detail=error, headers={"X-Error": error},)
            
    return {"query":query, "docs": docs}
#=========================================================

#=========================================================
# POST : es/{인덱스명}/docs/uids => uid 목록에 대한 검색(비동기)
# => http://127.0.0.1:9000/es/{인덱스}/docs/uid?query=쿼리문장&search_size=5
# - in : query=쿼리할 문장, search_size=검색계수(몇개까지 검색 출력 할지)
# - in(data) : DocsUidsIn=검색할 uid 목록
# - out: 검색 결과(스코어, rfile_name, rfile_text)
#=========================================================
class DocsUidsIn(BaseModel):
    uids: list       # uid(문서 고유id)->rfilename
    
@app.post("/es/{esindex}/docs/uids")
async def search_documents_uid(esindex:str, 
                     Data:DocsUidsIn,
                     query: str = Query(..., min_length=1),     # ... 는 필수 입력 이고, min_length=1은 최소값이 1임. 작으면 422 Unprocessable Entity 응답반환됨
                     search_size: int = Query(..., gt=0),       # ... 는 필수 입력 이고, gt=0은 0보다 커야 한다. 작으면 422 Unprocessable Entity 응답반환됨
                     qmethod: int=0,                            # option: qmethod=0 혹은 1(0=max벡터 구하기, 1=평균벡터 구하기 (default=0))
                     ):    
    
    error:str = 'success'
    query = query.strip()
    uids = Data.uids 
    LOGGER.info(f'\npost /es/{esindex}/docs/uids start-----\nquery:{query}, search_size:{search_size}, len(uids):{len(uids)}')
            
    try:
        # es로 임베딩 쿼리 실행
        error, docs = await async_es_embed_query(esindex, query, search_size, qmethod, uids)
    except Exception as e:
        error = f'async_es_embed_query fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'get /es/{esindex}/docs {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
    
    if error != 'success':
        raise HTTPException(status_code=404, detail=error, headers={"X-Error": error},)
            
    return {"query":query, "docs": docs}
#=========================================================

#=========================================================
# DELETE : ES/{인덱스명}/docs 검색(비동기)
# => http://127.0.0.1:9000/es/{인덱스}/docs?uid=rfile_name
# - in : uid=삭제할 문서 유니크한 id
# - out: ??
#=========================================================
@app.delete("/es/{esindex}/docs")
async def delete_documents(esindex:str,
                           uid:str = Query(...,min_length=1)):
    error:int = 0
    uid = uid.strip()
    LOGGER.info(f'\ndelete /es/{esindex}/docs start-----\nid:{uid}')
    
    try:
        error = await async_es_embed_delete(esindex, uid)
    except Exception as e:
        error = f'async_es_embed_delete fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'delete /es/{esindex}/docs {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
        
    if error != 0:
        raise HTTPException(status_code=404, detail=error, headers={"X-Error": error},)
  

#=========================================================================================
# 체팅 UI
# - bard 이용
#========================================================================================= 

#=========================================================
# 메인 bart_chat.html 호출하는 api  
#=========================================================
@app.get("/chat")
async def form(request: Request):
    return templates.TemplateResponse("chat01.html", {"request": request})

#=========================================================
# 검색 처리 api
#=========================================================
@app.post("/es/{esindex}/chat")
async def search_documents(esindex:str,
                     request: Request
                     ): 
    
    start_time = time.time()
    
    form = await request.form()
    search_size = 2
    
    query = form.get("query").strip()
    prequery = form.get("prequery").strip()
    checkdocsstr = form.get("checkdocs")
    #print(f'==>checkdocsstr :{checkdocsstr}')
    checkdocs = True
    if checkdocsstr == None: # 체크버튼 값은 False일때 None으로 들어오고, True이면 on으로 들어옴. 따라서 None으로 들어오면 False 해줌.
        checkdocs=False
    
    print(f'checkdocs :{checkdocs}')
    
    #print(f'1) /es/{esindex}/docs/bard/chat')
    #print(f'2) prequery:{prequery}')
    #print(f'3) query:{query}')
    
    # 이전 답변/응답 문단들 계수가 4를 넘으면, 가장오래된 문단을 제거하고, 각 문단별 <hr> 구분자를 넣어서 prequery를 만든다.
    prequery = remove_prequery(prequery, 4)

    # 새로운 대화 시도인 경우, 기존 preanswer 초기화 함.
    if query.startswith("@##새로운 대화"):
        prequery=""

    if LLM_MODEL == 0:       # SLLM
        question, answer, context1 = await async_search_docs(esindex, query, search_size, llm_model_type=0, model_key='', model_key1='', model_key2='', qmethod=Q_METHOD, checkdocs=checkdocs)
    elif LLM_MODEL == 1:     # gpt
        question, answer, context1 = await async_search_docs(esindex, query, search_size, llm_model_type=1, model_key='', model_key1='', model_key2='', qmethod=Q_METHOD, checkdocs=checkdocs)
    elif LLM_MODEL == 2:     # GPT
        question, answer, context1 = await async_search_docs(esindex, query, search_size, llm_model_type=2, model_key=BARD_TOKEN, model_key1=BARD_1PSIDTS_TOKEN, model_key2=BARD_1PSIDCC_TOKEN, qmethod=Q_METHOD, checkdocs=checkdocs)
        
     # context에서 title만 뽑아내서 url링크 만듬.
    titles_str = get_title_with_urllink(context1)
    
     # 소요된 시간을 계산합니다.
    end_time = time.time()
    elapsed_time = end_time - start_time

    # html로 표기할때 중간에 "(쌍따옴표) 있으면 안되므로 , 쌍따옴표를 '(홑따옴표)로 치환
    question = question.replace('"',"'")
    answer = answer.replace('"',"'") + '\n( 응답시간:' + str(elapsed_time) + ')'
    prequery = prequery.replace('"',"'")
    titles_str = titles_str.replace('"',"'")
    
    return templates.TemplateResponse("chat01.html", {"request": request, "question":question, "answer": answer, "preanswer": prequery, "titles": titles_str})

        
    
        