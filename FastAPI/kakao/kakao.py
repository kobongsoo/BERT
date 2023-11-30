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
import random
from tqdm.notebook import tqdm

# mpowerai
from os import sys
sys.path.append('./mpowerai')
from pympower.classes.mshaai import MShaAI

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
from fastapi.responses import JSONResponse, HTMLResponse
import asyncio
import threading
import httpx
import openai    
# ES 관련
from elasticsearch import Elasticsearch, helpers

# FutureWarning 제거
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) 

from utils import create_index, make_docs_df, get_sentences
from utils import load_embed_model, async_embedding, index_data, async_es_embed_query, async_es_embed_delete
from utils import async_chat_search, remove_prequery, get_title_with_urllink, make_prompt
from utils import generate_text_GPT2, generate_text_davinci
from utils import IdManager, NaverSearchAPI, GoogleSearchAPI, ES_Embed_Text, MyUtils, SqliteDB, WebScraping

#----------------------------------------------------------------------
# 전역 변수로 선언 => 함수 내부에서 사용할때 global 해줘야 함.
# 설정값 settings.yaml 파일 로딩

myutils = MyUtils(yam_file_path='./data/settings.yaml')
settings = myutils.get_options()
assert len(settings) > 2, f'load settings error!!=>len(settigs):{len(settings)}'
myutils.seed_everything()  # seed 설정
DEVICE = settings['GPU']
if DEVICE == 'auto':
    DEVICE = myutils.GPU_info() # GPU 혹은 CPU
    
# 임베딩 모델 로딩
WORD_EMBDDING_MODEL1, BI_ENCODER1 = load_embed_model(settings['E_MODEL_PATH'], settings['E_POLLING_MODE'], settings['E_OUT_DIMENSION'], DEVICE)
  
# LLM 모델 지정                                                     
openai.api_key = settings['GPT_TOKEN']# **GPT  key 지정
# 모델 - GPT 3.5 Turbo 지정
# => 모델 목록은 : https://platform.openai.com/docs/models/gpt-4 참조
gpt_model = settings['GPT_MODEL']  #"gpt-4"#"gpt-3.5-turbo" #gpt-4-0314
#---------------------------------------------------------------------------
# 클래스 초기화
# chabot3함수에서 중복 질문 방지를 위한 id 관리 클래스 초기화
id_manager = IdManager()

# 현재 사용자 mode가 뭔지 확인(0=회사본문검색, 1=웹문서검색, 2=AI응답모드)
userdb = SqliteDB('./data/kakao.db')
#userdb.execute('CREATE TABLE search_site(user_id TEXT, site TEXT)')  # 맨처음 table 생성해야함

# 네이버 검색 클래스 초기화
naver_api = NaverSearchAPI(client_id=settings['NAVER_CLIENT_ID'], client_secret=settings['NAVER_CLINET_SECRET'])

# 구글 검색 클래스 초기화
google_api = GoogleSearchAPI(api_key=settings['GOOGLE_API_KEY'], search_engine_id=settings['GOOGLE_SEARCH_ENGINE_ID'])

# 지난대화 저장 
mapping = myutils.get_mapping_esindex() # es mapping index 가져옴.

# 회사본문검색 이전 답변 저장.(순서대로 회사검색, 웹문서검색, AI응답답변)
index_name:str = "preanswer"
preanswer_embed_classification:list = ["company", "web", "ai"]  
# es 임베딩 생성
preanswer_embed = ES_Embed_Text(es_url=settings['ES_URL'], index_name=index_name, mapping=mapping, 
                              bi_encoder=BI_ENCODER1, float_type=settings["E_FLOAT_TYPE"], uid_min_score=0.10)

# url 웹스크래핑
webscraping = WebScraping()
shaai = MShaAI() # mpowerai(synap 문서필터)
#---------------------------------------------------------------------------
# url 스크래핑 한후 synap으로 문서내용 추출하는 함수 
# url: 추출할 url(문서url 혹은 웹페이지), srcfilepath: url 다운로드후 저장할 파일경로, tarfilepath: synap으로 내용 추출후 저장할 파일 경로
def scraping_web(url:str, srcfilepath:str, tarfilepath:str):
    assert url ,f'url is empty'
    assert srcfilepath ,f'srcfilepath is empty'
    assert tarfilepath ,f'tarfilepath is empty'
    
    error:int = 0
    text:str = ""
    
    try:
        error = webscraping.url_download(url=url, filepath=srcfilepath) # url 다운로드
    except Exception as e:
        print(f'url_download error=>{e}')
        error = 1002
        return text, error
    
    if error == 0:
        try:
            shaai.extract(srcPath=srcfilepath, tgtPath=tarfilepath)   # srcPath 경로 문서내용추출후 tgtPath파일로 저장
            
            text = webscraping.readlines_file(filepath=tarfilepath, min_len=20) # 파일 한줄씩 읽어와서 text로 리턴
            if len(text) > 4000:
                text = text[0:3999]
        except Exception as e:
            print(f'extract error=>{e}')
            error = 1002
    
    return text, error
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
        myutils.log_message(f'[error] /vectors {msg}')
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
    myutils.log_message(f'[info] /es/{esindex}/docs start-----\nES_URL:{ES_URL}, esindex:{esindex}, createindex:{createindex}, uids:{uids}, titles:{titles}')

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
        myutils.log_message(f'[error] /embed/es {error}')
        raise HTTPException(status_code=404, detail=error, headers={"X-Error": error},)
    
    # 1.elasticsearch 접속
    try:
        es = Elasticsearch(ES_URL)
        myutils.log_message(f'[info] /embed/es 1.Elasticsearch connect success=>{ES_URL}')
    except Exception as e:
        error = f'Elasticsearch connect fail({ES_URL})'
        msg = f'{error}=>{e}'
        myutils.log_message(f'[error] /embed/es {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
        
    #myutils.log_message(settings, f'es.info:{es.info()}')

    # 2. 추출된 문서들 불러와서 df로 만듬
    try:              
        df_contexts = make_docs_df(mydocuments=documents, mytitles=titles, myuids=uids, infilepath=infilepath) # myutils/kss_utils.py
        myutils.log_message(f'[info] /embed/es 2.load_docs success')
    except Exception as e:
        error = f'load docs fail'
        msg = f'{error}=>{e}'
        myutils.log_message(f'[error] /embed/es {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
                                                                    
    # 3. 문장 추출
    try:
        doc_sentences = get_sentences(df=df_contexts, 
                                      remove_sentnece_len=settings['REMOVE_SENTENCE_LEN'], 
                                      remove_duplication=settings['REMOVE_DUPLICATION']) # myutils/kss_utils.py
        
        myutils.log_message(f'[info] /embed/es 3.get_sentences success=>len(doc_sentences):{len(doc_sentences)}')
    except Exception as e:
        error = f'get_sentences fail'
        msg = f'{error}=>{e}'
        myutils.log_message(f'[error] /embed/es {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
   
    # 4.ES 인덱스 생성
    try:
        ES_INDEX_FILE = settings['ES_INDEX_FILE']
        create_index(es=es, index_file_path=ES_INDEX_FILE, index_name=esindex, create=createindex) # myutils/es_utils.py
        myutils.log_message(f'[info] /embed/es 4.create_index success=>index_file:{ES_INDEX_FILE}, index_name:{esindex}')
    except Exception as e:
        error = f'create_index fail'
        msg = f'{error}=>{e}'
        myutils.log_message(f'[error] /embed/es {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)

    # 5. index 처리
    try:    
        # utils/es_embed.py        
        index_data(es=es, df_contexts=df_contexts, doc_sentences=doc_sentences, 
                   es_index_name=esindex, out_dimension=settings['E_OUT_DIMENSION'], num_clusters=settings['NUM_CLUSTERS'], 
                   num_clusters_variable=settings['NUM_CLUSTERS_VARIABLE'], embedding_method=settings['E_METHOD'], clu_mode=settings['CLU_MODE'],
                   clu_outmode=settings['CLU_OUTMODE'], bi_encoder=BI_ENCODER1, float_type=settings['E_FLOAT_TYPE'],
                   seed=settings['SEED'], batch_size=settings['ES_BATCH_SIZE'])
        
        myutils.log_message(f'[info] /embed/es 5.index_data success\nend-----\n')
    except Exception as e:
        error = f'index_data fail'
        msg = f'{error}=>{e}'
        myutils.log_message(f'[error] /embed/es {msg}')
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
                     show: int=1                                # 0=dict 형태로 보여줌, 1=txt 형태로 보여줌.
                     ):                          
                    
    error:str = 'success'
    query = query.strip()
    myutils.log_message(f'\n[info] get /es/{esindex}/docs start-----\nquery:{query}, search_size:{search_size}')
    
    min_score = settings['ES_SEARCH_MIN_SCORE']
    
    try:
        # es로 임베딩 쿼리 실행      
        error, docs = await async_es_embed_query(settings=settings, esindex=esindex, query=query, 
                                                 search_size=search_size,bi_encoder=BI_ENCODER1, qmethod=qmethod)
    except Exception as e:
        error = f'async_es_embed_query fail'
        msg = f'{error}=>{e}'
        myutils.log_message(f'[error] get /es/{esindex}/docs {msg}')
        raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
    
    if error != 'success':
        raise HTTPException(status_code=404, detail=error, headers={"X-Error": error},)
       
    context:str = ''
    response:dict = {}
    
    # show ==0 : dict 형태로 출력
    if show == 0:
        response = {"query":query, "docs": docs}
        return response
    else:
        for doc in docs:
            score = doc['score']
            if score > min_score:
                rfile_text = doc['rfile_text']
                if rfile_text:
                    formatted_score = "{:.2f}".format(score)
                    rfile_text = rfile_text.replace("\n", "<br>")
                    context += '<br>'+ rfile_text + '<br>[score:'+str(formatted_score)+']' + '<br>'  # 내용과 socore 출력
           
        #response = {"query":query, "docs": context}
        # HTML 문서 생성
        html_content = f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>내용보기</title>
        </head>
        <body>
            <p>Q: {query}<br>{context}</p>
        </body>
        </html>
        """

        return HTMLResponse(content=html_content)

    
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
    myutils.log_message(f'\n[info] post /es/{esindex}/docs/uids start-----\nquery:{query}, search_size:{search_size}, len(uids):{len(uids)}')

    try:
        # es로 임베딩 쿼리 실행
        error, docs = await async_es_embed_query(settings=settings, esindex=esindex, query=query, 
                                                 search_size=search_size, bi_encoder=BI_ENCODER1, qmethod=qmethod, 
                                                 uids=uids)
    except Exception as e:
        error = f'async_es_embed_query fail'
        msg = f'{error}=>{e}'
        myutils.log_message(f'[error] get /es/{esindex}/docs {msg}')
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
    myutils.log_message(f'[info] t==>delete /es/{esindex}/docs : id:{uids}')
    
    es_url = settings['ES_URL']
    
    try:
        error = await async_es_embed_delete(esindex=esindex, uids=uids, es_url=es_url)
    except Exception as e:
        error = f'async_es_embed_delete fail'
        msg = f'{error}=>{e}'
        myutils.log_message(f'[error] delete /es/{esindex}/docs {msg}')
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
 
    myutils.log_message(f'[info] \t==>search_documents: question:{question}, answer:{answer}')
    
    return templates.TemplateResponse("chat01.html", {"request": request, "question":question, "answer": answer, "preanswer": prequery, "titles": titles_str})

#----------------------------------------------------------------------
# 유사한 쿼리 quickReplies 추가하기 위한 코드 
def similar_query(preanswer_docs:list, template:dict):
    for idx, pdocs in enumerate(preanswer_docs):
        if idx == 0:
            continue
            
        if preanswer_docs[idx]['answer'] and preanswer_docs[1]['score']:            
            preanswer_score = preanswer_docs[idx]['score']
            if preanswer_score > 1.60:  # 1.60 이상일때만 유사한 질문을 보여줌
                additional_structure = {
                    "messageText": preanswer_docs[idx]['answer'],
                    "action": "message",
                    "label": f"{preanswer_docs[idx]['answer']}({myutils.get_es_format_score(preanswer_score)}%)"
                }

                template["template"]["quickReplies"].append(additional_structure)

# 심플 text 템플릿 
def simpletext_template(text:str, usercallback:bool=False):
    template = {
            "version": "2.0",
            "useCallback": usercallback,
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": text
                        }
                    }
                ]
            }
        }
    
    return template
    
#=========================================================
# 카카오 쳇봇 연동 테스트 3
# - 콜백함수 정의 : 카카오톡은 응답시간이 5초로 제한되어 있어서, 5초이상 응답이 필요한 경우(LLM 응답은 10~20초) AI 챗봇 설정-콜백API 사용 신청하고 연동해야한다. 
#=========================================================
async def call_callback(settings:dict, user_id:str, user_mode:int, callbackurl:str, query:str, prompt:str, docs:list, s_best_contexts:list):
    async with httpx.AsyncClient() as client:
        
        await asyncio.sleep(1)
        
        error:str = ''
        errormsg:str = ''
        response:str = ''
        
        assert settings, f'Error:settings is empty'
        assert user_id, f'Error:user_id is empty'
        assert query, f'Error:query_prompt is empty'
        assert callbackurl, f'Error:callbackurl is empty'
    
        callbackurl1 = callbackurl
        
        start_time = time.time()
        prompt1 = prompt
        if len(prompt) > 100:
            prompt1 = prompt[0:99]
        myutils.log_message(f'\t[call_callback]==>call_callback: user_mode:{user_mode},query:{query}, prompt:{prompt1}({len(prompt)}), callbackurl:{callbackurl1}, user_id:{user_id}\n')
           
        gpt_model:str = settings['GPT_MODEL']
        system_prompt:str = settings['SYSTEM_PROMPT']
        f_min_score:float = settings['ES_SEARCH_MIN_SCORE']
        api_server_url:str = settings['API_SERVER_URL']
            
        if prompt:
            input_prompt = prompt
        else:
            input_prompt = query
            
        #myutils.log_message(f"\t[call_callback]==>input_prompt: {input_prompt}, system_prompt:{system_prompt}\n")
        #--------------------------------
        # GPT text 생성
        if gpt_model.startswith("gpt-"):
            response, status = generate_text_GPT2(gpt_model=gpt_model, prompt=input_prompt, system_prompt=system_prompt, 
                                                  stream=True, timeout=20) #timeout=20초면 2번 돌게 되므로 총 40초 대기함
        else:
            response, status = generate_text_davinci(gpt_model=gpt_model, prompt=input_prompt, stream=True, timeout=20)
         
        # GPT text 생성 성공이면=>질문과 답변을 저정해둠.
        preanswer_docs:list=[]
        if status == 0:
            if user_mode != 5:
                res, preanswer_docs, status1 = preanswer_embed.delete_insert_doc(doc={'answer':query, 'response':response},
                                                                           classification=preanswer_embed_classification[user_mode])
                 # 로그만 남기고 진행
                if status1 != 0:
                    myutils.log_message(f'[call_callback][error]==>insert_doc:{res}\n')
        else:
            if status == 1001: # time out일때
                query = "응답 시간 초과"
                response = "⚠️AI 응답이 없습니다. 잠시 후 다시 질문해 주세요.\n(" + response + ")"
            else:
                query = "응답 에러"
                response = "⚠️AI 에러가 발생하였습니다. 잠시 후 다시 질문해 주세요.\n(" + response + ")"
                    
            error = f'generate_text_xxx fail=>model:{gpt_model}'
            myutils.log_message(f'[call_callback][error]==>call_callback:{error}=>{response}\n')
            docs = []  # docs 초기화
             
        myutils.log_message(f"\t[call_callback]==>답변: {response}\n")
        
        # 소요된 시간을 계산합니다.
        end_time = time.time()
        formatted_elapsed_time = "{:.2f}".format(end_time - start_time)
        
        label_str:str = "다시 검색.."
        if user_mode == 5:
            label_str = "다시 요약.."
            
        template = {
            "version": "2.0",
            "template": {
                "outputs": [],
                "quickReplies": [
                        {
                            "messageText": '?'+query,
                            "action": "message",
                            "label": label_str
                        }
                      ]
                }
            }
        #--------------------------------
        # 검색된 내용 카카오톡 쳇봇 Text 구성     
        if user_mode == 0:  # 회사본문검색 
            # weburl = '10.10.4.10:9000/es/qaindex/docs?query='회사창립일은언제?'&search_size=3&qmethod=2&show=1
            webLinkUrl = api_server_url+'/es/qaindex/docs?query='+query+'&search_size=4&qmethod=2&show=1'
   
            template["template"]["outputs"].append({
                "textCard": {
                    "title": '📃' + query,
                    "description": '(time:' + str(formatted_elapsed_time) + ')\n' + response,
                    "buttons": [
                        {
                            "action": "webLink",
                            "label": "내용보기",
                            "webLinkUrl": webLinkUrl
                        }
                    ]
                }
            })
        elif user_mode == 1: # 웹문서검색 
            template["template"]["outputs"].append({
                "textCard": {
                    "title": '🌐' + query,
                    "description": '(time:' + str(formatted_elapsed_time) + ')\n' + response,
                    "buttons": [
                        {
                            "action": "webLink",
                            "label": f"{s_best_contexts[i]['title'][:12]}.." if len(s_best_contexts[i]['title']) > 12 else f"{s_best_contexts[i]['title']}",
                            "webLinkUrl": s_best_contexts[i]['link']
                        } for i in range(min(3, len(s_best_contexts)))
                    ]
                }
            })
        elif user_mode == 2:  # AI 검색
            template["template"]["outputs"].append({
                "textCard": {
                    "title": '🤖' + query,
                    "description": '(time:' + str(formatted_elapsed_time) + ')\n' + response
                }
            })
        elif user_mode == 5: # URL 요약
            template["template"]["outputs"].append({
                "textCard": {
                    "title": '💫' + query,
                    "description": '(time:' + str(formatted_elapsed_time) + ')\n' + response
                }
            })
            
        # 유사한 질문이 있으면 추가
        #myutils.log_message(f"\t[call_callback]preanswer_docs\n{preanswer_docs}\n")
        similar_query(preanswer_docs=preanswer_docs, template=template)
        
        #----------------------------------------
        for i in range(3):
            # 콜백 url로 anwer 값 전송
            callback_response = await client.post(
                callbackurl1,
                json=template
            )
                
            if callback_response.status_code == 200:
                myutils.log_message(f"\t[call_callback]call_callback 호출 성공\ncallbackurl:{callbackurl1}\n")
                break
            else:  # 실패면 1초 대기했다가 다시 전송해봄
                myutils.log_message(f"\t[call_callback][error] call_callback 호출 실패(count:{i}): {callback_response.status_code}\ncallbackurl:{callbackurl1}\n")
                await asyncio.sleep(1)
                continue
        #----------------------------------------
        # id_manager 에 id 제거
        # 응답 처리중에는 다른 질문할수 없도록 lock 기능을 위한 user_id 제거
        id_manager.remove_id_all(user_id) # id 제거
        #----------------------------------------
        
        myutils.log_message(f"\t[call_callback][end]==============\n")
 
        return callback_response
#=========================================================
# 카카오 쳇봇 연동 테스트
#=========================================================                     
@app.post("/chatbot3")
async def chabot3(content: Dict):

    #await asyncio.sleep(1)
    
    global settings
    settings = myutils.get_options()
    content1 = content["userRequest"]
    myutils.log_message(f'[start]==============\nt\[chabot3]==>content1:{content1}\n')
    
    query1:str = content["userRequest"]["utterance"]  # 질문
    callbackurl:str = content["userRequest"]["callbackUrl"] # callbackurl
    user_id:str = content["userRequest"]["user"]["id"]
    #myutils.log_message(f't\[chabot3]==>user_id:{user_id}\n')
    
    # 쿼리가 이미지인지 파악하기 위해 type을 얻어옴.'params': {'surface': 'Kakaotalk.plusfriend', 'media': {'type': 'image', 'url':'https://xxxx'}...}
    query_format:str = ""
    if 'media' in content["userRequest"]['params'] and 'type' in content["userRequest"]['params']['media']:
        query_format = content["userRequest"]['params']['media']['type']
      
    qmethod:int = settings['ES_Q_METHOD']
    system_prompt:str = settings['SYSTEM_PROMPT']
    gpt_model:str = settings['GPT_MODEL']
    
    assert query1, f'Error:query1 is empty'
    assert user_id, f'Error:user_id is empty'
    assert callbackurl, f'Error:callbackurl is empty'
    assert 0 <= qmethod <= 2, 'Error: qmethod should be in the range 0 to 2'
       
    search_size:int = 4      # 회사본문 검색 계수
    esindex:str = "qaindex"  # qaindex    
   
    bFind_docs:bool = True   # True이면 회사본문임베딩 찾은 경우
    content:dict = {}
    docs:list = []
    prompt:str = ''
    embed_context:str = ''

    #-----------------------------------------------------------
    # id_manager 에 id가 존재하면 '이전 질문 처리중'이므로, return 시킴
    # 응답 처리중에는 다른 질문할수 없도록 lock 기능을 위한 해당 user_id 가 있는지 검색
    if id_manager.check_id_exists(user_id):
        myutils.log_message(f't\[chabot3]==>이전 질문 처리중:{user_id}\n')
        return
    #-----------------------------------------------------------
    # 동영상이나 이미지 입력은 차단
    if query_format != "":
        template = simpletext_template(text = f'⚠️이미지나 동영상은 입력 할수 없습니다.')
        json_response = JSONResponse(content=template)
        return json_response
    #-----------------------------------------------------------
    
    # id_manager 에 id 추가.  응답 처리중에는 다른 질문할수 없도록 lock 기능을 위해 user_id 추가함.
    id_manager.add("0", user_id) # mode와 user_id 추가
    
    #-----------------------------------------------------------
    # prefix에 ? 붙여서 질문하면 이전 질문 검색 안함.
    preanswer_search = True   # True=이전질문 검색함.
    prefix_query1 = query1[0]
    if prefix_query1 == '?':
        query = query1[1:]
        preanswer_search = False
    else:
        query = query1     
    #-------------------------------------     
    # 쿼리 길이가 1보다 작으면 return 시킴.
    if len(query) < 1:
        myutils.log_message(f'\t[chatbot3]==>query is empty=>query1:{query}')
        # 응답 처리중에는 다른 질문할수 없도록 lock 기능을 위한 user_id 제거
        id_manager.remove_id_all(user_id) # id 제거
        return
    #-------------------------------------
    
    # 사용자 모드(0=회사본문검색, 1=웹문서검색, 2=AI응답모드, 5=URL 요약) 얻어옴.
    user_mode = userdb.select_user_mode(user_id)
    
    # 쿼리가 url 이면 사용자 모드는 5(URL 요약)로 설정
    if webscraping.is_url(query) == True and query_format == "":
        user_mode = 5        
        
    #------------------------------------
    # 설정 값 얻어옴
    setting = userdb.select_setting(user_id=user_id) # 해당 사용자의 site, preanswer 등을 얻어옴
    s_site:str = "naver" # 웹검색 사이트 기본은 네이버 
    e_preanswer:int = 1  # 예전 유사질문 검색 (기본은 허용)
    
    if setting != -1:
        s_site = setting.get('site', s_site)
        e_preanswer = setting.get('preanswer', e_preanswer)
        
    #myutils.log_message(f'\t[chatbot3]==>s_site:{s_site},  e_preanswer:{e_preanswer}')
    #-------------------------------------
    # 이전 질문 검색(회사본문검색=0, 웹문서검색=1) 일때만 
    if preanswer_search == True and user_mode < 5 and e_preanswer == 1: 
        preanswer_docs = preanswer_embed.embed_search(query=query, classification=preanswer_embed_classification[user_mode])
        
        if len(preanswer_docs) > 0:
            preanswer_score = preanswer_docs[0]['score']
            preanswer_response = preanswer_docs[0]['response']
            preanswer = preanswer_docs[0]['answer']
            preanswer_id = preanswer_docs[0]['_id']
            myutils.log_message(f'\t[chatbot3]==>이전질문:{preanswer}(score:{preanswer_score}, id:{preanswer_id})\n이전답변:{preanswer_response}')
                
            # 1.80 이상일때만 이전 답변 보여줌.
            if preanswer_score >= 1.80:  
                if user_mode == 0:
                    query1 = f'📃{query}'
                elif user_mode == 1:
                    query1 = f'🌐{query}'
                else:
                    query1 = f'🤖{query}'
                        
                # 정확도 스코어 구함
                formatted_preanswer_score = myutils.get_es_format_score(preanswer_score)
                     
                template = {
                    "version": "2.0",
                    "useCallback": False,
                    "template": {
                        "outputs": [
                        {
                            "textCard": {
                                "title": query1,
                                "description": f'💬예전 질문과 답변입니다. (유사도:{formatted_preanswer_score}%)\nQ:{preanswer}\n{preanswer_response}'
                            }
                        }
                      ],
                        "quickReplies": [
                        {
                            "messageText": '?'+query,
                            "action": "message",
                            "label": "다시 검색.."
                        }
                      ]
                    }
                }
                
                # 유사한 질문이 있으면 추가
                similar_query(preanswer_docs=preanswer_docs, template=template)
                  
                json_response = JSONResponse(content=template)

                # 응답 처리중에는 다른 질문할수 없도록 lock 기능을 위한 user_id 제거
                id_manager.remove_id_all(user_id) # id 제거

                return json_response       
 
    #------------------------------------
    # 설정 값 얻어옴 
    search_str:str = ""
    # 회사 문서(인덱싱 데이터) 검색
    if user_mode == 0:
        
        try:
            # es로 임베딩 쿼리 실행      
            error_str, docs = await async_es_embed_query(settings=settings, esindex=esindex, query=query, 
                                                         search_size=search_size, bi_encoder=BI_ENCODER1, qmethod=qmethod)
             # prompt 생성 => min_score 보다 작은 conext는 제거함.
            prompt, embed_context = make_prompt(settings=settings, docs=docs, query=query)
            
        except Exception as e:
            myutils.log_message(f'\t[chatbot3]==>async_es_embed_query fail=>{e}')
            # 응답 처리중에는 다른 질문할수 없도록 lock 기능을 위한 user_id 제거
            id_manager.remove_id_all(user_id) # id 제거
            return   

        # 컨텍스트가 없으면. 임베딩을 못찾은 것이므로, bFind_docs=False로 설정
        if len(embed_context) < 2: 
            bFind_docs = False
            
        search_str = "🔍회사본문검색 완료. 답변 대기중.."
    #-------------------------------------
    # 네이버 검색
    s_error:int = 0
    s_context:str = ''
    s_best_contexts:list = []
    
    if user_mode == 1:
        s_contexts:list = []   
        s_str:str = "네이버"
        try:
            if s_site == "naver":
                # 네이버 검색
                classification=['webkr', 'blog', 'news']
                # 랜덤하게 2개 선택
                #selected_items = random.sample(classification, 2)
                random.shuffle(classification)  #랜덤하게 3개 섞음
                s_contexts, s_best_contexts, s_error = naver_api.search_naver(query=query, classification=classification, start=random.randint(1, 2), display=8)
            else: # 구글 검색
                s_contexts, s_best_contexts, s_error = google_api.search_google(query=query, page=2) # page=2이면 20개 검색
                s_str = "구글"
                
        except Exception as e:
            myutils.log_message(f'\t[chatbot3]==>naver_api.search_naver fail=>{e}')
            # 응답 처리중에는 다른 질문할수 없도록 lock 기능을 위한 user_id 제거
            id_manager.remove_id_all(user_id) # id 제거
            s_error = 1001
       
        # prompt 구성
        if len(s_contexts) > 0 and s_error == 0:
            for idx, con in enumerate(s_contexts):
                if con['descript'] and con['link']:
                    s_context += con['descript']+'\n\n'
                               
            # text-davinci-003 모델에서, 프롬프트 길이가 총 1772 넘어가면 BadRequest('https://api.openai.com/v1/completions') 에러 남.
            # 따라서 context 길이가 1730 이상이면 1730까지만 처리함.
            if gpt_model.startswith("text-") and len(s_context) > 1730:
                s_context = s_context[0:1730]

            prompt = settings['PROMPT_CONTEXT'].format(context=s_context, query=query)
            search_str = f"🔍{s_str}검색 완료. 답변 대기중.."
        else:
            prompt = settings['PROMPT_NO_CONTEXT'].format(query=query)  
            search_str = f"🔍{s_str}검색 없음. 답변 대기중.."
            
    #----------------------------------------
    # AI 응답 모드
    if user_mode == 2:
        prompt = settings['PROMPT_NO_CONTEXT'].format(query=query)  
        search_str = "🤖AI 답변 대기중.."
    #----------------------------------------
    # URL 모드
    if user_mode == 5:
        srcfilepath = './tmp/'+str(user_id)+'.url' # 파일경로는 userid.url로 함.
        tarfilepath = './tmp/'+str(user_id)+'.mpower'
        
        # tmp 폴더가 없으면 생성합니다.
        if not os.path.exists('./tmp'):
            os.makedirs('./tmp')
        
        context, error = scraping_web(url=query, srcfilepath=srcfilepath, tarfilepath=tarfilepath)
        if len(context) > 300:
            if len(context) > 4000:
                context = context[0:3999]
            
            prompt = f'{context}\n\nQ:위 내용을 요약해줘. A:'
            search_str = "💫URL 내용 요약중.."
        else:
            if len(context) == 0:
                answer = f"⚠️URL 검출된 내용이 없습니다..URL을 다시 입력해주세요."
            elif len(context) < 301:
                answer = f"⚠️URL 검출된 내용이 너무 적어서 요약할 수 없습니다.. (길이:{len(context)})\n내용:\n{context}"
            else:
                answer = f"⚠️URL 내용 검출 실패..URL을 다시 입력해주세요.\n(error:{error})"
            
            template = simpletext_template(text = answer)
            
            # id_manager 에 id 제거
            # 응답 처리중에는 다른 질문할수 없도록 lock 기능을 위한 user_id 제거
            id_manager.remove_id_all(user_id) # id 제거
            
            json_response = JSONResponse(content=template)
            return json_response
    #----------------------------------------
    # 응답 메시지 출력 및 콜백 호출  
    # 회사본문검색(user_mode==0 )인데 검색에 맞는 내용을 못찾으면(bFind_docs == False), gpt 콜백 호출하지 않고, 답을 찾지 못했다는 메시지 출력함.       
    if user_mode==0 and bFind_docs == False:
        answer = "⚠️질문에 맞는 회사본문내용을🔍찾지 못했습니다. 질문을 다르게 해 보세요."
        template = simpletext_template(text = answer)
        
        # id_manager 에 id 제거
        # 응답 처리중에는 다른 질문할수 없도록 lock 기능을 위한 user_id 제거
        id_manager.remove_id_all(user_id) # id 제거
 
    # 검색이 아닌경우(user_mode==0 ), 혹은 회사본문검색(user_mode==0 )인데 맞는 내용을 찾은 경우(bFind_docs == True)에는 gpt 콜백 호출함.
    else:
             
        # 답변 설정
        text = f"{search_str}"
        template = {
            "version": "2.0",
            "useCallback": True,
            "data": {
                "text" : text
            }
        }
    #----------------------------------------
    call:bool = False
    for i in range(3):
        json_response = JSONResponse(content=template)
        if json_response.status_code == 200:
             # 비동기 작업을 스케줄링 콜백 호출
            task = asyncio.create_task(call_callback(settings=settings, user_id=user_id, user_mode=user_mode,callbackurl=callbackurl, 
                                                     query=query, prompt=prompt, docs=docs, s_best_contexts=s_best_contexts))
            
            myutils.log_message(f"\t[chabot3]==>성공: status_code:{json_response.status_code}\ncallbackurl: {callbackurl}\n")  
            call = True
            break
        else:
            myutils.log_message(f"\t[chabot3]==>실패(count:{i}): status_code:{json_response.status_code}\ncallbackurl: {callbackurl}\n")    
            continue
    
    if call == False:
        id_manager.remove_id_all(user_id) # id 제거
   
    return json_response
#----------------------------------------------------------------------

def set_userinfo(content, user_mode:int):
    myutils.log_message(f't\[searchdoc]==>content:{content}\n')
    user_id:str = content["user"]["id"]
    if user_id.strip()=="":
        return 1001
    
    # id_manager 에 id가 존재하면 '이전 질문 처리중'이므로, return 시킴
    # 응답 처리중에는 다른 질문할수 없도록 lock 기능을 위한 해당 user_id 가 있는지 검색
    if id_manager.check_id_exists(user_id):
        myutils.log_message(f't\[searchdoc]==>이전 질문 처리중:{user_id}\n')
        return 1002

    userdb.insert_user_mode(user_id, user_mode) # 해당 사용자의 user_id 모드를 0로 업데이트
    return 0
 
#-----------------------------------------------------------
@app.post("/searchdoc")
async def searchdoc(content: Dict):
    if set_userinfo(content=content["userRequest"], user_mode=0) != 0:
        return

    title = "📃회사본문검색\n질문을 하면 회사본문내용를🔍검색해서 모아이가 답을 합니다."
    descript = '''지금은 모코엠시스 2023년 '회사규정'과 '회사소개' 관련만🔍검색할 수 있습니다.(업데이트 예정..)\n\n[내용보기]를 누르면 검색한 💬회사본문내용을 볼 수 있습니다.
    '''
    template = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                "basicCard": {
                    "title": title,
                    "description": descript,
                    "thumbnail": {
                        "imageUrl": "http://k.kakaocdn.net/dn/eLnYje/btsA5fPdyHO/fOkPDdHMY6616CNYFiHNkK/2x1.jpg"
                    },
                    "buttons": [
                    {
                      "action":  "message",
                      "label": "출장시 숙박비는 얼마?",
                      "messageText": "출장시 숙박비는 얼마?"
                    },
                    {
                      "action":  "message",
                      "label": "야근 식대는 얼마?",
                      "messageText": "야근 식대는 얼마?"
                    }
                  ]
                 }
                }
              ]
           }
        }
    
    json_response = JSONResponse(content=template)
        
    return json_response
#----------------------------------------------------------------------
@app.post("/searchweb")
async def chabot3(content: Dict):
    if set_userinfo(content=content["userRequest"], user_mode=1) != 0:
        return
    
   # http://k.kakaocdn.net/dn/bUP0MS/btsA7RAx01M/sSR0gN6O0kzXN1l66pYvMk/2x1.jpg => 메인
   # http://k.kakaocdn.net/dn/nm41W/btsA9g0UbzW/Fvz12wrGK2duYyLCww2o21/2x1.jpg => URL 입력 요약
   # http://k.kakaocdn.net/dn/eLnYje/btsA5fPdyHO/fOkPDdHMY6616CNYFiHNkK/2x1.jpg => 회사본문검색
   # http://k.kakaocdn.net/dn/bqkjxi/btsA9V3gT5i/JRbnnpxeoxG6ok4H3rX9Tk/2x1.jpg => 웹검색
   # http://k.kakaocdn.net/dn/bbRJLT/btsBb5xrDyJ/cOKisJNsExLV77kHBTOTHk/2x1.jpg => AI응답모드
   # http://k.kakaocdn.net/dn/lGVgi/btsA5hTJGUL/tUo5HnahK3aMGO9XJ49t21/2x1.jpg => 설정
   # http://k.kakaocdn.net/dn/bRDZcJ/btsA9TqM29J/N79nlPR6shWiNuOycmsG1k/2x1.jpg=>피드벡
    title = "🌐웹검색\n질문을 하면 네이버,구글🔍검색해서 모아이가 답을 합니다."
    descript = "답변은 최대⏰30초 걸릴 수 있고,종종 엉뚱한 답변도 합니다.\n\n버튼을 클릭하면 검색한 🌐URL로 연결됩니다."
    template = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                "basicCard": {
                    "title": title,
                    "description": descript,
                    "thumbnail": {
                        "imageUrl": "http://k.kakaocdn.net/dn/bqkjxi/btsA9V3gT5i/JRbnnpxeoxG6ok4H3rX9Tk/2x1.jpg"
                    },
                    "buttons": [
                    {
                      "action":  "message",
                      "label": "제주도 봄 여행코스 추천",
                      "messageText": "제주도 봄 여행코스 추천"
                    },
                    {
                      "action":  "message",
                      "label": "2023년 한국야구 우승팀은?",
                      "messageText": "2023년 한국야구 우승팀은?"
                    }
                  ]
                 }
                }
              ]
           }
        }
    
    json_response = JSONResponse(content=template)
    
    return json_response

#----------------------------------------------------------------------
@app.post("/searchai")
async def searchai(content: Dict):
    if set_userinfo(content=content["userRequest"], user_mode=2) != 0:
        return
    
    title = "🤖AI 응답 모드\n질문을 하면 모아이가 알아서 답변을 해줍니다."
    descript = '''답변은 최대⏰30초 걸릴 수 있으며,종종 엉뚱한 답변도 합니다.
    '''
    template = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                "basicCard": {
                    "title": title,
                    "description": descript,
                    "thumbnail": {
                        "imageUrl": "http://k.kakaocdn.net/dn/bbRJLT/btsBb5xrDyJ/cOKisJNsExLV77kHBTOTHk/2x1.jpg"
                    },
                    "buttons": [
                    {
                      "action":  "message",
                      "label": "봄을 주제로 노래가사 써줘",
                      "messageText": "봄을 주제로 노래가사 써줘"
                    },
                    {
                      "action":  "message",
                      "label": "AI 강의 목차 만들어줘",
                      "messageText": "AI 강의 목차 만들어줘"
                    }
                  ]
                 }
                }
              ]
           }
        }
        
    json_response = JSONResponse(content=template)    
    return json_response
#----------------------------------------------------------------------
# setting 관련
@app.post("/setting/save")
async def setting_save(request: Request): 
    
    form = await request.form()
    user_id = form.get("user_id")
    search_site = form.get("search_engine")
    pre_answer = form.get("preanswer")
    
    #myutils.log_message(f"\t[setting]==>setting_save=>pre_answer:{pre_answer}/{type(pre_answer)}\n")
    
    # 변경값으로 셋팅.
    error = userdb.insert_setting(user_id=user_id, site=search_site, preanswer=int(pre_answer)) # 해당 사용자의 user_id site를 업데이트
    setting_success:bool = False
    if error == 0:
        setting_success = True
    else:
        myutils.log_message(f"\t[setting]==>setting_save fail!\n")
        
    return templates.TemplateResponse("setting.html", {"request": request, "user_id":user_id, "search_site": search_site, 
                                                       "pre_answer": int(pre_answer), "setting_success": setting_success })
    
# setting.html 로딩    
@app.get("/setting/form")
async def setting_form(request:Request, user_id:str):
    
    assert user_id, f'user_id is empty'
    setting = userdb.select_setting(user_id=user_id) # 해당 사용자의 site를 얻어옴
    
    search_site:str = "naver" # 웹검색 사이트 (기본은 naver)
    pre_answer=1   # 예전 유사 질문 검색(기본=1(검색함))
    if setting != -1 and setting['site']:
        search_site = setting['site']
        pre_answer = setting['preanswer']
        
    #myutils.log_message(f"\t[setting]==>setting_form=>user_id:{user_id}, search_site:{search_site}, preanswer:{pre_answer}\n")
    
    return templates.TemplateResponse("setting.html", {"request": request, "user_id":user_id, 
                                                       "search_site": search_site, "pre_answer":pre_answer})

@app.post("/setting")
async def setting(content: Dict):
    user_id:str = content["userRequest"]["user"]["id"]
    assert user_id, f'user_id is empty'
    
    api_server_url:str = settings['API_SERVER_URL']
    
    search_site:str = "naver" # 웹검색 사이트 (기본은 naver)
    pre_answer=1   # 예전 유사 질문 검색(기본=1(검색함))
    pre_answer_str:str = '검색함'
    user_mode_list:list = ['회사본문검색(1)','웹검색(2)','AI응답모드(3)']   
    user_mode_str:str = "없음"
    
    setting = userdb.select_setting(user_id=user_id) # 해당 사용자의 site를 얻어옴
    #myutils.log_message(f"\t[setting]==>setting:{setting}\n")
    
    user_mode=userdb.select_user_mode(user_id=user_id)
    if user_mode >= -1:
        user_moe_str = user_mode_list[user_mode]
        
    
    if setting != -1 and setting['site']:
        search_site = setting['site']
        pre_answer = setting['preanswer']
     
    if pre_answer != 1:
        pre_answer_str:str = '검색안함'
        
    linkurl = f'{api_server_url}/setting/form?user_id={user_id}'
    descript = f'🧒 사용자ID: {user_id}\n\n🕹 현재 동작모드: {user_moe_str}\n💬 에전유사 질문검색: {pre_answer_str}\n🌐 웹검색 사이트: {search_site}\n\n예전유사 질문검색, 웹검색 사이트 변경을 원하시면 설정하기를 눌러 변경해 주세요.'
    
    template = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                "basicCard": {
                    "title": "사용자정보 & 설정",
                    "description": descript,
                    "thumbnail": {
                        "imageUrl": "http://k.kakaocdn.net/dn/lGVgi/btsA5hTJGUL/tUo5HnahK3aMGO9XJ49t21/2x1.jpg"
                    },
                    "buttons": [
                    {
                        "action": "webLink",
                        "label": "⚙️설정하기",
                        "webLinkUrl": linkurl
                    }
                  ]
                 }
                }
              ]
           }
        }
        
    json_response = JSONResponse(content=template)
    return json_response
#----------------------------------------------------------------------