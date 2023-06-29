#----------------------------------------------------------------------
# FastAPI 이용한 sLLM 질의응답 예제
# - sLLM 모델과 kpf-sbert-128d-v1 임베딩 모델 이용함. sLLM은 KoAlpaca-Polyglot-5.8B LoRA 기법으로 파인튜닝한 KoAlpaca-Polyglot-5.8B-LoRA-qa-moco 사용.
#
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
import re
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

# llm 관련
import transformers
from peft import PeftModel
from transformers import GenerationConfig

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
SETTINGS_FILE = './data/sllm_settings.yaml'  # 설정파일 경로 (yaml 파일)
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
FLOAT_TYPE = settings['embedding']['FLOAT_TYPE']             # 임베딩 벡터 float 타입('float32', 'float16')
MIN_SCORE = settings['embedding']['MIN_SCORE']               # 검색 1.4 스코어 이하면 제거
LOGGER.info(f'*임베딩 Settings: EMBEDDING_METHOD:{EMBEDDING_METHOD}, FLOAT_TYPE:{FLOAT_TYPE}, MIN_SCORE: {MIN_SCORE}')

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

# ES
ES_URL = settings['es']['ES_URL']
ES_INDEX_FILE = settings['es']['ES_INDEX_FILE']
BATCH_SIZE = settings['es']['BATCH_SIZE'] 
LOGGER.info(f'*ES Settings: ES_URL:{ES_URL}, ES_INDEX_FILE:{ES_INDEX_FILE}, BATCH_SIZE:{BATCH_SIZE}')

# sLLM 모델
lora_weights = settings['sllm']['lora_weights']
llm_model_path = settings['sllm']['llm_model_path']
uselora_weight = settings['sllm']['uselora_weight']
load_8bit = settings['sllm']['load_8bit']
LOGGER.info(f'*sllm Settings: lora_weights:{lora_weights}, llm_model_path:{llm_model_path}, uselora_weight:{uselora_weight}, load_8bit:{load_8bit}, load_8bit:{load_8bit}')

# LLM 모델 타입
LLM_MODEL_TYPE = settings['llmmodel']['LLM_MODEL_TYPE']
#PROMPT_DICT = settings['llmmodel']['PROMPT_DICT']

# PROMPT 사전
PROMPT_DICT = {   
    "prompt_context":("###지시: 문단]에서 [질의]에 대해 가장 적합한 내용들을 찾고, 찾은 내용을 [질의]에 맞게 잘 정리해서 문장으로 답변해 주\n\n##[문단]: {context}\n\n##[질의]: {query}\n\n####[응답]:"),
    "prompt_no_context":("###지시: [질의]에 대해, 자세하게 문장으로 작성해 주세요\n\n###[질의]: {query}\n\n###[응답]:")
}

LOGGER.info(f'*llmmodel Settings: LLM_MODEL_TYPE:{LLM_MODEL_TYPE}, PROMPT_DICT:{PROMPT_DICT}')

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
# sLLM 모델 로딩
#---------------------------------------------------------------------------
if LLM_MODEL_TYPE == 0:     # 0=아래 지정한 sLLM 모델, 1=GPT 모델, 2=BARD 모델. == True:
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

#------------------------------------------------------------------------
# ES임베딩 쿼리 벡터
# -쿼리 임베딩 벡터를 구하고, es에 접속해서 rfile_text 뽑아냄
# - in : esindex=인덱스명, query=쿼리 , search_size=검색출력계수
#------------------------------------------------------------------------
def es_embed_query(esindex:str, query:str, search_size:int):
    error: str = 'success'
    
    query = query.strip()
    
    # 1.elasticsearch 접속
    es = Elasticsearch(ES_URL)  
    
    if not query:
        error = 'query is empty'
    elif search_size < 1:
        error = 'search_size < 1'
    elif not es.indices.exists(esindex):
         error = 'esindex is not exist'
    
    if error != 'success':
        LOGGER.error(f'[es_embed_query] {error}')
        return error, None

    # 임베딩 구함.
    start_time = time.time()
    embed_query = embedding([query])[0]
    print(f'*len(embed_query) : {len(embed_query)}')
    
    # 쿼리 구성
    script_query = {
        "script_score":{
            "query":{
                "match_all": {}},
            "script":{
                "source": "cosineSimilarity(params.query_vector, doc['vector1']) + 1.0",  # 뒤에 1.0 은 코사인유사도 측정된 값 + 1.0을 더해준 출력이 나옴
                "params": {"query_vector": embed_query}
            }
        }
    }
    
    #print(script_query)

    # 실제 ES로 검색 쿼리 날림
    start_search_time = time.time()
    response = es.search(
        index=esindex,
        body={
            "size": search_size,
            "query": script_query,
            "_source":{"includes": ["rfile_name", "rfile_text"]}
        }
    )
    end_time = time.time() - start_time
    LOGGER.info("*ES 검색시간: {:.2f} ms".format(end_time * 1000)) 

    count = 0
    docs = []
    for hit in response["hits"]["hits"]: 
        doc = {}  #dict 선언
        doc['rfile_name'] = hit["_source"]["rfile_name"]      # contextid 담음
        doc['rfile_text'] = hit["_source"]["rfile_text"]      # text 담음.
        doc['score'] = hit["_score"]
        docs.append(doc) 
            
    return error, docs
#------------------------------------------------------------------------

#---------------------------------------------------------------------------
# 비동기 ES 임베딩 벡터 쿼리 실행 함수
#---------------------------------------------------------------------------
async def async_es_embed_query(esindex:str, query:str, search_size:int):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, es_embed_query, esindex, query, search_size)
#---------------------------------------------------------------------------

#------------------------------------------------------------------------
# PROMPT 생성
#------------------------------------------------------------------------
def make_prompt(docs, query)->str:
     # prompt 구성
    context:str = ''

    for doc in docs:
        score = doc['score']
        if score > MIN_SCORE:
            rfile_text = doc['rfile_text']
            if rfile_text:
                context += rfile_text + '\n\n'
                
    if context:
        prompt = PROMPT_DICT['prompt_context'].format(query=query, context=context)
    else:
        prompt = PROMPT_DICT['prompt_no_context'].format(query=query)
                
    # KoAlpaca 프롬프트
    #prompt = f"### 질문: {query}\n질문에 대해 아래 내용을 바탕으로 간략히 답변해 주세요\n\n### 문맥: {context}\n\n### 답변:" if context else f"### 질문: {query}\n질문에 대해 간략히 답변해 주세요\n\n### 답변:"
    
    # llama 프롬프트
    #prompt = f"아래는 작업을 설명하는 명령어입니다. 요청을 적절히 완료하는 응답을 작성하세요. ### Instruction: {context}\n{query} ### Response:"

    #print(prompt)
    #print()
    return prompt
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

#---------------------------------------------------------------------------
# 비동기 sLLM 이용한 text 생성
#---------------------------------------------------------------------------
async def async_generate_text_sLLM(prompt:str):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, generate_text_sLLM, prompt)
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
    return {"서버": "질의응답 AI 봇", 
            "*임베딩모델":{"모델경로": MODEL_PATH, "폴링방식((mean=평균값, cls=문장대표값, max=최대값)": POLLING_MODE, "출력차원(128, 0=768)": OUT_DIMENSION,"임베딩방식(0=문장클러스터링, 1=문장평균임베딩, 2=문장임베딩)": EMBEDDING_METHOD, "출력벡터타입('float32', 'float16')": FLOAT_TYPE},
            "*클러스터링":{"클러스터링 가변(True=문장계수에 따라 클러스터링계수를 다르게함)": NUM_CLUSTERS_VARIABLE, "방식(kmeans=k-평균 군집 분석, kmedoids=k-대표값 군집 분석)": CLUSTRING_MODE, "계수": NUM_CLUSTERS, "출력(mean=평균벡터 출력, max=최대값벡터출력)": OUTMODE},
            "*문장전처리":{"제거문장길이(설정길이보다 작은 문장은 제거됨)": REMOVE_SENTENCE_LEN, "중복문장제거(True=중복된문장은 제거됨)": REMOVE_DUPLICATION},
            "*ES":{"ES서버URL": ES_URL, "INDEX 파일경로": ES_INDEX_FILE, "BATCH 크기": BATCH_SIZE},
            "*LLM 모델":{"모델타입(0=아래 sLLM 모델, 1=GPT 모델, 2=BARD 모델.)": LLM_MODEL_TYPE},
            "*sLLM 모델":{"LoRA 사용유.무": uselora_weight, "LoRA 8bit 사용": load_8bit, "LoRA 가중치 경로": lora_weights, "sLLM 모델 경로": llm_model_path},
            "*환경설정":{"로그경로": LOG_PATH, "SEED값": SEED, "GPU사용(auto'=gpu 서버면 gpu, 아니면 cpu, 'cpu'=무조건 CPU로 동작)": GPU, "sLLM 모델 경로": llm_model_path}
           }

#=========================================================
# GET : es/{인덱스명}/docs 검색(비동기)
# => http://127.0.0.1:9000/es/{인덱스}/docs?query=쿼리문장&search_size=5
# - in : query=쿼리할 문장, search_size=검색계수(몇개까지 검색 출력 할지)
# - out: 
#=========================================================
@app.get("/es/{esindex}/docs")
async def search_documents(esindex:str, 
                     query: str = Query(..., min_length=1),     # ... 는 필수 입력 이고, min_length=1은 최소값이 1임. 작으면 422 Unprocessable Entity 응답반환됨
                     search_size: int = Query(..., gt=0)       # ... 는 필수 입력 이고, gt=0은 0보다 커야 한다. 작으면 422 Unprocessable Entity 응답반환됨
                     ):                          
                    
      
    error:str = 'success'
    query = query.strip()
    LOGGER.info(f'\nget /es/{esindex}/docs start-----\nquery:{query}, search_size:{search_size}')
    
    query_split = query.split('##')
    prefix = query_split[0]  
    
    if prefix == '@':  # 일반쿼리일때는 @## prefix 입력후 질문입력함. 
        query1 = query_split[1]
        prompt = await async_make_prompt(docs='', query=query1)
    else:
        query1 = query
        
        # es로 임베딩 쿼리 실행
        try:
            error, docs = await async_es_embed_query(esindex, query1, search_size)
        except Exception as e:
            error = f'async_es_embed_query fail'
            msg = f'{error}=>{e}'
            LOGGER.error(f'get /es/{esindex}/docs {msg}')
            raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
            
        print(docs)
        print()
        # prompt 생성    
        prompt = await async_make_prompt(docs=docs, query=query1)
   
    # sllM으로 text 생성
    try:
        response = await async_generate_text_sLLM(prompt)
    except Exception as e:
        error = f'async_generate_text_sLLM fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'get /es/{esindex}/docs {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
    
    if error != 'success':
        raise HTTPException(status_code=404, detail=error, headers={"X-Error": error},)
     
    # 응답을 파싱해서 응답만 뽑아내서 return 함.
    answer:str = "답변 없음."
    answers:list = []
    questions:list = []
    contexts:list = []
    context:str = ""
    if response:
        answers = response.split("###[응답]:")
        #print(answer[0])
        #print()
        questions = answers[0].split("###[질의]:")
        #print(questions[0])
        #print()
        contexts = questions[0].split("###[문단]:")
        #print(contexts[1])
        #print()
       
    if answers[1]:
        answer = answers[1].strip()
        
    if contexts[1]:
        context = contexts[1].strip()
        
    return {"query":query, "answer": answer, "context": context}
#=========================================================
