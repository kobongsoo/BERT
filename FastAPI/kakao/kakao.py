#----------------------------------------------------------------------
# GPT를 카카오톡과 연동 예제
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
import openai    
# ES 관련
from elasticsearch import Elasticsearch, helpers

# FutureWarning 제거
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) 

from utils import seed_everything, GPU_info, mlogging, get_options, create_index, make_docs_df, get_sentences
from utils import load_embed_model, async_embedding, index_data, async_es_embed_query, async_es_embed_delete
from utils import async_chat_search, remove_prequery, get_title_with_urllink, make_prompt, generate_text_GPT
#----------------------------------------------------------------------

# 전역 변수로 선언 => 함수 내부에서 사용할때 global 해줘야 함.
# 설정값 settings.yaml 파일 로딩
settings = get_options(file_path='./data/settings.yaml')
assert len(settings) > 2, f'load settings error!!=>len(settigs):{len(settings)}'

LOGGER = mlogging(loggername="kakao", logfilename=settings['LOG_PATH']) # 로그
seed_everything(settings['SEED'])  # seed 설정
DEVICE = settings['GPU']
if DEVICE == 'auto':
    DEVICE = GPU_info() # GPU 혹은 CPU
    
# 임베딩 모델 로딩
WORD_EMBDDING_MODEL1, BI_ENCODER1 = load_embed_model(settings['E_MODEL_PATH'], settings['E_POLLING_MODE'], settings['E_OUT_DIMENSION'], DEVICE)
  
# LLM 모델 지정                                                     
openai.api_key = settings['GPT_TOKEN']# **GPT  key 지정
# 모델 - GPT 3.5 Turbo 지정
# => 모델 목록은 : https://platform.openai.com/docs/models/gpt-4 참조
gpt_model = settings['GPT_MODEL']  #"gpt-4"#"gpt-3.5-turbo" #gpt-4-0314

#---------------------------------------------------------------------------

# http://10.10.4.10:9002/docs=>swagger UI, http://10.10.4.10:9000/redoc=>ReDoc UI 각각 비활성화 하려면
# => docs_url=None, redoc_url=None 하면 된다.
#app = FastAPI(redoc_url=None) #FastAPI 인스턴스 생성(*redoc UI 비활성화)

app = FastAPI()
templates = Jinja2Templates(directory="templates") # html 파일이 있는 경로를 지정.

#----------------------------------------------------------------------
@app.get("/")
async def root():
    embedding_model = settings['E_MODEL_PATH']
    return { "MoI(모아이)":"카카오톡 연동 AI 모델", "1.임베딩모델": settings["E_MODEL_PATH"], "2.LLM모델": settings["GPT_MODEL"], "3.ES" : settings["ES_URL"]}
#----------------------------------------------------------------------

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
        embeddings = await async_embedding(paragraphs=sentences, bi_encoder=BI_ENCODER1, float_type=settings["E_FLOAT_TYPE"])
    except Exception as e:
        error = f'async_embedding fail({settings["ES_URL"]})'
        msg = f'{error}=>{e}'
        LOGGER.error(f'/vectors {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
        
    embeddings_str = [",".join(str(elem) for elem in sublist) for sublist in embeddings]
    return {"vectors": embeddings_str}
#----------------------------------------------------------------------

#=========================================================
# POST: es/{인덱스명}/docs (입력 docs(문서)에 대한 임베딩값 구하고 ElasticSearch(이하:ES) 추가.(동기))
# => http://127.0.0.1:9000/es/{인덱스명}/docs
# - in : docs: 문서 (예: ['오늘 날씨가 좋다', '내일은 비가 온다'] ), titles: 문서제목, uids(문서 고유id)
# - in : esindexname : ES 인덱스명, createindex=True(True=무조건 인덱스생성. 만약 있으면 삭제후 생성/ Flase=있으면 추가, 없으면 생성)
# - in : infilepath : True이면 documnets에 filepath 입력되고, 이때는 file를 로딩함. False이면 documents로는 문서내용이 들어옴.
# - out: ES 성공 실패??
#=========================================================
class DocsEmbedIn(BaseModel):
    uids: list       # uid(문서 고유id)->rfile_name
    titles: list     # 제목->rfiletext
    documents: list  # 문서내용 혹은 file 경로 (infilepath=True이면, filepath 입력됨)
    
@app.post("/es/{esindex}/docs")    
def embed_documents(esindex:str, Data:DocsEmbedIn, infilepath:bool=False, createindex:bool=False):
    error:str = 'success'
        
    documents = Data.documents
    uids = Data.uids
    titles = Data.titles
    
    ES_URL = settings['ES_URL']
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
        df_contexts = make_docs_df(mydocuments=documents, mytitles=titles, myuids=uids, infilepath=infilepath) # myutils/kss_utils.py
        LOGGER.info(f'/embed/es 2.load_docs success')
    except Exception as e:
        error = f'load docs fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'/embed/es {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
                                                                    
    # 3. 문장 추출
    try:
        doc_sentences = get_sentences(df=df_contexts, 
                                      remove_sentnece_len=settings['REMOVE_SENTENCE_LEN'], 
                                      remove_duplication=settings['REMOVE_DUPLICATION']) # myutils/kss_utils.py
        
        LOGGER.info(f'/embed/es 3.get_sentences success=>len(doc_sentences):{len(doc_sentences)}')
    except Exception as e:
        error = f'get_sentences fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'/embed/es {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
   
    # 4.ES 인덱스 생성
    try:
        ES_INDEX_FILE = settings['ES_INDEX_FILE']
        create_index(es=es, index_file_path=ES_INDEX_FILE, index_name=esindex, create=createindex) # myutils/es_utils.py
        LOGGER.info(f'/embed/es 4.create_index success=>index_file:{ES_INDEX_FILE}, index_name:{esindex}')
    except Exception as e:
        error = f'create_index fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'/embed/es {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)

    # 5. index 처리
    try:    
        # utils/es_embed.py        
        index_data(es=es, df_contexts=df_contexts, doc_sentences=doc_sentences, 
                   es_index_name=esindex, out_dimension=settings['E_OUT_DIMENSION'], num_clusters=settings['NUM_CLUSTERS'], 
                   num_clusters_variable=settings['NUM_CLUSTERS_VARIABLE'], embedding_method=settings['E_METHOD'], clu_mode=settings['CLU_MODE'],
                   clu_outmode=settings['CLU_OUTMODE'], bi_encoder=BI_ENCODER1, float_type=settings['E_FLOAT_TYPE'],
                   seed=settings['SEED'], batch_size=settings['ES_BATCH_SIZE'])
        
        LOGGER.info(f'/embed/es 5.index_data success\nend-----\n')
    except Exception as e:
        error = f'index_data fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'/embed/es {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)

#----------------------------------------------------------------------
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
                     qmethod: int=2,                            # option: qmethod=0 혹은 1(0=max벡터 구하기, 1=평균벡터 구하기 (default=0))
                     ):                          
                    
    error:str = 'success'
    query = query.strip()
    LOGGER.info(f'\nget /es/{esindex}/docs start-----\nquery:{query}, search_size:{search_size}')
    
    try:
        # es로 임베딩 쿼리 실행      
        error, docs = await async_es_embed_query(settings=settings, esindex=esindex, query=query, 
                                                 search_size=search_size,bi_encoder=BI_ENCODER1, qmethod=qmethod)
    except Exception as e:
        error = f'async_es_embed_query fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'get /es/{esindex}/docs {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
    
    if error != 'success':
        raise HTTPException(status_code=404, detail=error, headers={"X-Error": error},)
            
    return {"query":query, "docs": docs}
#----------------------------------------------------------------------

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
                     qmethod: int=2,                            # option: qmethod=0 혹은 1(0=max벡터 구하기, 1=평균벡터 구하기 (default=0))
                     ):    
    
    error:str = 'success'
    docs = []
    query = query.strip()
    uids = Data.uids 
    LOGGER.info(f'\npost /es/{esindex}/docs/uids start-----\nquery:{query}, search_size:{search_size}, len(uids):{len(uids)}')

    
    try:
        # es로 임베딩 쿼리 실행
        error, docs = await async_es_embed_query(settings=settings, esindex=esindex, query=query, 
                                                 search_size=search_size, bi_encoder=BI_ENCODER1, qmethod=qmethod, 
                                                 uids=uids)
    except Exception as e:
        error = f'async_es_embed_query fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'get /es/{esindex}/docs {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
    
    if error != 'success':
        raise HTTPException(status_code=404, detail=error, headers={"X-Error": error},)
            
    return {"query":query, "docs": docs}
#----------------------------------------------------------------------

#=========================================================
# DELETE : ES/{인덱스명}/docs 검색(비동기)
# => http://127.0.0.1:9000/es/{인덱스}/docs?uid=rfile_name
# - in : uid=삭제할 문서 유니크한 id
# - out: ??
#=========================================================
@app.delete("/es/{esindex}/docs")
async def delete_documents(esindex:str,
                           uids:str = Query(...,min_length=1)):
    error:int = 0
    uids = uids.strip()
    LOGGER.info(f't==>delete /es/{esindex}/docs : id:{uids}')
    
    es_url = settings['ES_URL']
    
    try:
        error = await async_es_embed_delete(esindex=esindex, uids=uids, es_url=es_url)
    except Exception as e:
        error = f'async_es_embed_delete fail'
        msg = f'{error}=>{e}'
        LOGGER.error(f'delete /es/{esindex}/docs {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
        
    if error != 0:
        raise HTTPException(status_code=404, detail=error, headers={"X-Error": error},)
#----------------------------------------------------------------------

#=========================================================================================
# 체팅 UI
# - gpt 이용
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
    search_size = 3
    
    query = form.get("query").strip()
    prefix_query = query[0]
           
    prequery = form.get("prequery").strip()
    checkdocsstr = form.get("checkdocs")
    #print(f'==>checkdocsstr :{checkdocsstr}')
    
    # 내용검색 체크버튼 값은 False일때 None으로 들어오고, True이면 on으로 들어옴. 따라서 None으로 들어오면 True 해줌.
    checkdocs = False
    if checkdocsstr != None:
        checkdocs=True
       
    #print(f'1) /es/{esindex}/docs/bard/chat')
    #print(f'2) prequery:{prequery}')
    #print(f'3) query:{query}')
    
    # 이전 답변/응답 문단들 계수가 4를 넘으면, 가장오래된 문단을 제거하고, 각 문단별 <hr> 구분자를 넣어서 prequery를 만든다.
    prequery = remove_prequery(prequery, 4)

    # 새로운 대화 시도인 경우, 기존 preanswer 초기화 함.
    if query.startswith("?새로운 대화"):
        checkdocs=False
        prequery=""
   
    print(f'\t==>search_documents: checkdocs :{checkdocs}')
     
    # 검색 시작.
    question, answer, context1 = await async_chat_search(settings=settings, esindex=esindex, query=query, 
                                                         search_size=search_size, bi_encoder=BI_ENCODER1, checkdocs=checkdocs)
        
    # context에서 title만 뽑아내서 url링크 만듬.
    if context1:
        titles_str = get_title_with_urllink(context=context1, data_folder='')
    else:
        titles_str =''
        
     # 소요된 시간을 계산합니다.
    end_time = time.time()
    elapsed_time = end_time - start_time

    # html로 표기할때 중간에 "(쌍따옴표) 있으면 안되므로 , 쌍따옴표를 '(홑따옴표)로 치환
    question = question.replace('"',"'")
    answer = answer.replace('"',"'") + '\n( 응답시간:' + str(elapsed_time) + ')'
    prequery = prequery.replace('"',"'")
    titles_str = titles_str.replace('"',"'")
 
    LOGGER.info(f'\t==>search_documents: question:{question}, answer:{answer}')
    
    return templates.TemplateResponse("chat01.html", {"request": request, "question":question, "answer": answer, "preanswer": prequery, "titles": titles_str})

#----------------------------------------------------------------------

#=========================================================
# 카카오 쳇봇 연동 테스트 3
# - 콜백함수 정의 : 카카오톡은 응답시간이 5초로 제한되어 있어서, 5초이상 응답이 필요한 경우(LLM 응답은 10~20초) AI 챗봇 설정-콜백API 사용 신청하고 연동해야한다. 
#=========================================================
async def call_callback(settings:dict, callback_url:str, query_prompt:str, docs:list):
    async with httpx.AsyncClient() as client:
        #api_response = await client.get("https://some-api.com/data")
        #api_data = api_response.json()
        assert settings, f'Error:settings is empty'
        assert query_prompt, f'Error:query_prompt is empty'
        assert callback_url, f'Error:callback_url is empty'
    
        start_time = time.time()
        callbackurl = callback_url
        #query = "답변:" + query1
        
        query = query_prompt
        print(f'\t==>call_callback: query:{query}, callbackurl:{callbackurl}')
        
        gpt_model = settings['GPT_MODEL']
        system_prompt = settings['SYSTEM_PROMPT']
        min_score = settings['ES_SEARCH_MIN_SCORE']
        
        #--------------------------------
        # GPT text 생성
        messages = []
        try:
            response = generate_text_GPT(gpt_model=gpt_model, prompt=query, system_prompt=system_prompt, messages=messages)
        except Exception as e:
            error = f'generate_text_xxx fail=>model:{gpt_model}'
            msg = f'{error}=>{e}'
            print(f'[search_docs]: {msg}\n')
            raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)         
        
        # 소요된 시간을 계산합니다.
        end_time = time.time()
        elapsed_time = end_time - start_time
        formatted_elapsed_time = "{:.2f}".format(elapsed_time)
        #answer += '\n(time:' + str(formatted_elapsed_time) + ')'   # 응답시간 추가
        
        #--------------------------------
        # 답변 Text 구성
        context:str = ''

        # docs가 있으면, 회사문서검색(내용검색)이므로, gpt 응답(response) + 검색내용 해서 리턴함
        if len(docs) > 0:
            for doc in docs:
                score = doc['score']

                if score > min_score:
                    rfile_text = doc['rfile_text']
                    if rfile_text:
                        #score -=1
                        formatted_score = "{:.2f}".format(score)
                        context += '\n'+rfile_text+' [score:'+str(formatted_score)+']' + '\n'  # 내용과 socore 출력
       
        LOGGER.info(f"\t==>답변: {response}")
        #--------------------------------
        
        response += '\n(time:' + str(formatted_elapsed_time) + ')'
        
        if len(docs) > 0:
            '''
            template ={
              "version": "2.0",
              "template": {
                "outputs": [
                  {
                    "textCard": {
                      "title": "답변입니다",
                      "description": response,
                      "buttons": [
                        {
                          "action": "message",
                          "label": "관련 내용보기",
                          "messageText": context
                        }
                      ]
                    }
                  }
                ]
              }
            }
            '''
            template = {
                "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "simpleText": {
                                    "text": '답변:\n' + response + '\n\n검색내용:' + context
                                }
                            }
                        ]
                    }
                }
        else:
      
            template ={
              "version": "2.0",
              "template": {
                "outputs": [
                  {
                    "textCard": {
                      "title": "답변:",
                      "description": response
                    }
                  }
                ]
              }
            }
        
        # 콜백 url로 anwer 값 전송
        callback_response = await client.post(
            callbackurl,
            json=template
        )
        
        LOGGER.info(f"\t==>callback_response:{callback_response}")

        if callback_response.status_code == 200:
            printf(f"call_callback 호출 성공")
        else:
            printf(f"call_callback 호출 실패: {callback_response.status_code}")
        
#=========================================================
# 카카오 쳇봇 연동 테스트
#=========================================================        
@app.post("/chatbot3")
async def chabot3(content: Dict):
        
    assert settings, f'Error:settings is empty'

    query1 = content["userRequest"]["utterance"]  # 질문
    callbackurl = content["userRequest"]["callbackUrl"] # callbackurl
    qmethod = settings['ES_Q_METHOD']
    
    # 로그 초기화 하기 작상 시작
    global LOGGER
    LOGGER = None
    LOGGER = mlogging(loggername="kakao", logfilename=settings['LOG_PATH']) # 로그

    assert query1, f'Error:query1 is empty'
    assert callbackurl, f'Error:callbackurl is empty'
    assert 0 <= qmethod <= 2, 'Error: qmethod should be in the range 0 to 2'
       
    content1 = content["userRequest"]
    LOGGER.info(f't\==>chatbot3: content1:{content1}')
    
    search_size = 3      # 검색 계수
    esindex = "qaindex"  # qaindex    
   
    bFind_docs = True   # True이면 회사문서임베딩 찾은 경우
    content = {}
    docs = []
    
    # prefix에 ? 붙여서 질문하면 index 검색함.
    checkdocs = False
    prefix_query1 = query1[0]
    if prefix_query1 == '?':
        checkdocs = True
        query = query1[1:]
    else:
        query = query1
    
    # 인덱싱 데이터 검색
    if checkdocs == True:
        try:
            # es로 임베딩 쿼리 실행      
            error, docs = await async_es_embed_query(settings=settings, esindex=esindex, query=query, 
                                                     search_size=search_size, bi_encoder=BI_ENCODER1, qmethod=qmethod)
        except Exception as e:
            error = f'\t==>chatbot3: async_es_embed_query fail'
            msg = f'{error}=>{e}'
            LOGGER.error(f'get /es/{esindex}/docs {msg}')
            raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
                    
        # prompt 생성 => min_score 보다 작은 conext는 제거함.
        prompt, embed_context = make_prompt(settings=settings, docs=docs, query=query)
        
        query = prompt # 이때는 query 가 prompt로 설정.
        
        # 컨텍스트가 없으면. 임베딩을 못찾은 것이므로, bFind_docs=False로 설정
        if len(embed_context) < 2: 
            bFind_docs = False
            
    #----------------------------------------
    # 응답 메시지 출력 및 콜백 호출  
    # 회사문서 검색(checkdocs == True)인데 검색에 맞는 내용을 못찾으면(bFind_docs == False), gpt 콜백 호출하지 않고, 답을 찾지 못했다는 메시지 출력함.       
    if checkdocs == True and bFind_docs == False:
        answer = "회사 자료에서는 질문에 답을 찾지 못했습니다.\n질문을 다르게 해보세요."
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
    # 회사문서검색이 아닌경우(checkdocs == False), 혹은 회사문서 검색(checkdocs == True)인데 맞는 내용을 찾은 경우(bFind_docs == True)에는 gpt 콜백 호출함.
    else:
        # 비동기 작업을 스케줄링 콜백 호출
        asyncio.create_task(call_callback(settings=settings, callback_url=callbackurl, query_prompt=query, docs=docs))
             
        # 답변 설정
        content = {
            "version": "2.0",
            "useCallback": True,
            "data": {
                "text" : "답변 검색 중..최대 50초 대기.."
            }
        }
          
    return JSONResponse(content=content)
#----------------------------------------------------------------------
