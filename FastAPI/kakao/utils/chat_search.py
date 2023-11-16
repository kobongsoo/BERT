import torch
import time
import os
import numpy as np
from tqdm.notebook import tqdm

import asyncio
from elasticsearch import Elasticsearch
from fastapi import HTTPException

from .es_search import es_embed_query, make_query_script
from .llm_generate import generate_text_GPT2

#------------------------------------------------------------------------
# PROMPT 생성
#------------------------------------------------------------------------
def make_prompt(settings:dict, docs:list, query:str):
       
    min_score = settings['ES_SEARCH_MIN_SCORE']
    prompt_context = settings['PROMPT_CONTEXT']
    prompt_no_context = settings['PROMPT_NO_CONTEXT']
    
    assert query, f'query is empty'
    assert prompt_context, f'prompt_context is empty'
    assert prompt_context, f'prompt_no_context is empty'
 
    # prompt 구성
    context:str = ''

    for doc in docs:
        score = doc['score']
        if score > min_score:
            rfile_text = doc['rfile_text']
            if rfile_text:
                context += rfile_text + '\n\n'
                
    if context:
        prompt = prompt_context.format(query=query, context=context)
    else:
        prompt = prompt_no_context.format(query=query)
        
        '''
        if LLM_MODEL == 0:  #SLLM 모델일때 
            prompt = PROMPT_NO_CONTEXT.format(query=query)
        else:   # GPT 혹은 BARD인 경우, context가 없으면  프롬프트는 쿼리만 생성함.
            prompt = query
        '''  
    return prompt, context
#------------------------------------------------------------------------

#------------------------------------------------------------------
# BERT로 문단 검색 후 sLLM 로 Text 생성.
#------------------------------------------------------------------
def chat_search(settings:dict, esindex:str, query:str, 
                search_size:int, bi_encoder, checkdocs:bool=True):
    
    error:str = 'success'
        
    query = query.strip()
    esindex = esindex.strip()
    es_url = settings['ES_URL'].strip()
    gpt_model = settings['GPT_MODEL'].strip()
    qmethod = settings['ES_Q_METHOD']
    system_prompt = settings['SYSTEM_PROMPT']
    min_score = settings['ES_SEARCH_MIN_SCORE']
    
    assert query, f'query is empty'
    assert esindex, f'esindex is empty'
    assert es_url, f'es_url is empty'
    assert gpt_model, f'gpt_model is empty'

    print(f'\t==>chat_search:{esindex}, query:{query}, search_size:{search_size}, es_url:{es_url}, gpt_model:{gpt_model}')
    
    docs = []
    response:str = '회사 자료에서는 질문에 답을 찾지 못했습니다.\n질문을 다르게 해보세요.'
    embed_context:str = ''
    bFind_docs = True # True이면 회사문서임베딩 찾은 경우
    
    if checkdocs == False: # 회사문서검색 체크하지 않으면 그냥 쿼리 그대로 prompt 설정함.
        query1=query
        prompt, embed_context = make_prompt(settings=settings, docs='', query=query1)   
    else:
        query1 = query
        
        # es로 임베딩 쿼리 실행
        try:
            error, docs = es_embed_query(settings=settings, esindex=esindex, query=query1, 
                                         search_size=search_size, bi_encoder=bi_encoder, qmethod=qmethod)
        except Exception as e:
            error = f'es_embed_query fail'
            msg = f'{error}=>{e}'
            print(f'\t==>chat_search: {msg}\n')
            raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
         
        # 검색된 문단들 출력
        #print(docs)
        #print()
        
        # prompt 생성    
        prompt, embed_context = make_prompt(settings=settings, docs=docs, query=query1)
        
        if len(embed_context) < 2:
            bFind_docs = False
            
    print(f'\t==>chat_search:prompt:{prompt}, bFind_docs:{bFind_docs}')
  
    # bFind_docs == True일때만 쿼리함.
    if bFind_docs == True or checkdocs == False:

        # GPT text 생성
        if gpt_model.startswith("text-davinci"):
            response, status = generate_text_davinci(gpt_model=gpt_model, prompt=input_prompt)
        else:
            response, status = generate_text_GPT2(gpt_model=gpt_model, prompt=input_prompt, system_prompt=system_prompt, timeout=30) #timeout=30초로 설정
 
        if status != 0:
            error = f'generate_text_xxx fail=>model:{gpt_model}'
            msg = f'{error}=>{e}'
            print(f'[search_docs]: {msg}\n')
            raise HTTPException(status_code=404, detail=msg, headers={"X-Error": error},)
    
    # 리턴 구문 작성
    query = query1
    context:str = ''
        
    if checkdocs == True:
        if len(docs) > 0:
            for doc in docs:
                score = doc['score']
                    
                if score > min_score:
                    rfile_text = doc['rfile_text']
                    if rfile_text:
                        #score -=1
                        formatted_score = "{:.2f}".format(score)
                        context += '\n'+rfile_text+'\n[score:'+str(formatted_score)+']' + '\n'  # 내용과 socore 출력
        
    # 내용검색체크되고, 실제 db에서 내용을 찾은 경우에만 '검색내요' 항목 추가해줌.
    if checkdocs == True and bFind_docs == True:
        answer = '답변:\n' + response + '\n\n검색내용:' + context
    else:
        answer = response
        
    print(f'\t==>chat_search:answer:{answer}\n')
    return query, answer, embed_context
    
    
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# 비동기 BERT로 문단 검색 후 LLM모델 로 Text 생성.
#---------------------------------------------------------------------------
async def async_chat_search(settings:dict, esindex:str, query:str, 
                            search_size:int, bi_encoder, checkdocs:bool=True):
    
    loop = asyncio.get_running_loop()
    #print(f'[async_search_docs] esindex :{esindex}')
    ##print(f'[async_search_docs] query :{query}')
    #print(f'[async_search_docs] gpt_model :{gpt_model}')
    
    return await loop.run_in_executor(None, chat_search, 
                                      settings, esindex, query, 
                                      search_size, bi_encoder, checkdocs)


# main    
if __name__ == '__main__':
    main()