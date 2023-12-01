import torch
import time
import os
import numpy as np
from tqdm.notebook import tqdm

import asyncio
from elasticsearch import Elasticsearch

from .es_embed import embedding

#---------------------------------------------------------------------------
# ES 평균 쿼리 스크립트 구성
# => 1문서당 10개의 벡터가 있는 경우 10개의 벡터 유사도 평균 구하는 스크립트
# => 아래 make_max_query_script 보다 엄청 정확도 떨어짐. (max=83%, avg=50%)
# -in: query_vector = 1차원 임베딩 벡터 (예: [10,10,1,1, ....]
# -in: vectornum : ES 인덱스 벡터 수
#---------------------------------------------------------------------------
def make_avg_query_script(query_vector, vectornum:int=10, vectormag:float=0.8, uid_list:list=None)->str:
    # 문단별 10개의 벡터와 쿼리벡터를 서로 비교하여 유사도를 구하고, 10개를 구한 유사도의 평균을 최종 유사도로 지정하여 가장 유사한 문서 출력
    # => return 스코어는 음수(-0.212345)가 될수 없으므로, 음수가 나오면 0으로 리턴.
    # => script """ 안에 코드는 java 임.
    # => "queryVectorMag": 0.1905 일때 100% 일치하는 값은 9.98임(즉 10점 만점임)
    
    # uid_list가 있는 경우에는 해당하는 목록만 검색함
    if uid_list:
        query = { "bool" :{ "must": [ { "terms": { "rfile_name": uid_list } } ] } }
    else: # uid_list가 있는 경우에는 해당하는 목록만 검색함
        query = { "match_all" : {} }
        
    script_query = {
        "script_score":{
            "query":query,
                "script":{
                    "source": """
                      float avg_score = 0;
                      float total_score = 0;
                      for(int i = 1; i <= params.VectorNum; i++) 
                      {
                          float[] v = doc['vector'+i].vectorValue; 
                          float vm = doc['vector'+i].magnitude;  
                          
                          if (v[0] != 0)
                          {
                              float dotProduct = 0;

                              for(int j = 0; j < v.length; j++) 
                              {
                                  dotProduct += v[j] * params.queryVector[j];
                              }

                              float score = dotProduct / (vm * (float) params.queryVectorMag);
                              
                              if (score < 0) 
                              {
                                  score = 0
                              }
                              total_score += score;
                          }
                      }
                      avg_score = total_score / params.VectorNum;
                      if (avg_score < 0) {
                        avg_score = 0;
                      }
                      return avg_score
                    """,
                "params": 
                {
                  "queryVector": query_vector,  # 벡터임베딩값 설정
                  "queryVectorMag": vectormag,  # 벡터 크기
                  "VectorNum": vectornum        # 벡터 수 설정
                }
            }
        }
    }
    
    return script_query
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# ES MAX 쿼리 스크립트 구성
# => 1문서당 10개의 벡터 중에서 가장 유사도가 큰 1개의 벡터 유사도 측정하는 쿼리
# -in: query_vector = 1차원 임베딩 벡터 (예: [10,10,1,1, ....]
# -in: vectornum : ES 인덱스 벡터 수
#---------------------------------------------------------------------------
def make_max_query_script(query_vector, vectornum:int=10, vectormag:float=0.8, uid_list:list=None)->str:
    # 문단별 10개의 벡터와 쿼리벡터를 서로 비교하여 최대값 갖는 문단들중 가장 유사한  문단 출력
    # => script """ 안에 코드는 java 임.
    # => "queryVectorMag": 0.1905 일때 100% 일치하는 값은 9.98임(즉 10점 만점임)
                        
    # uid_list가 있는 경우에는 해당하는 목록만 검색함
    if uid_list:
        query = { "bool" :{ "must": [ { "terms": { "rfile_name": uid_list } } ] } }
    else: # uid_list가 있는 경우에는 해당하는 목록만 검색함
        query = { "match_all" : {} }
    
    script_query = {
        "script_score":{
             "query":query,
                "script":{
                    "source": """
                      float max_score = 0;
                      for(int i = 1; i <= params.VectorNum; i++) 
                      {
                          float[] v = doc['vector'+i].vectorValue; 
                          float vm = doc['vector'+i].magnitude;  
                          
                          if (v[0] != 0)
                          {
                              float dotProduct = 0;

                              for(int j = 0; j < v.length; j++) 
                              {
                                  dotProduct += v[j] * params.queryVector[j];
                              }

                              float score = dotProduct / (vm * (float) params.queryVectorMag);

                              if(score > max_score) 
                              {
                                  max_score = score;
                              }
                            }
                      }
                      return max_score
                    """,
                "params": 
                {
                  "queryVector": query_vector,  # 벡터임베딩값 설정
                  "queryVectorMag": vectormag,  # 벡터 크기
                  "VectorNum": vectornum        # 벡터 수 설정
                }
            }
        }
    }
    
    return script_query
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# ES 기본 vector 쿼리 구성
#---------------------------------------------------------------------------
def make_query_script(query_vector, uid_list:list=None)->str:
    # 문단별 10개의 벡터와 쿼리벡터를 서로 비교하여 최대값 갖는 문단들중 가장 유사한  문단 출력
    # => script """ 안에 코드는 java 임.
    # => "queryVectorMag": 0.1905 일때 100% 일치하는 값은 9.98임(즉 10점 만점임)
                        
    # uid_list가 있는 경우에는 해당하는 목록만 검색함
    if uid_list:
        query = { "bool" :{ "must": [ { "terms": { "rfile_name": uid_list } } ] } }
    else: # uid_list가 있는 경우에는 해당하는 목록만 검색함
        query = { "match_all" : {} }
    
    script_query = {
        "script_score":{
            "query":query,
            "script":{
                "source": "cosineSimilarity(params.queryVector, doc['vector1']) + 1.0",  # 뒤에 1.0 은 코사인유사도 측정된 값 + 1.0을 더해준 출력이 나옴
                "params": {"queryVector": query_vector}
            }
        }
    }
    
    return script_query

#---------------------------------------------------------------------------
#쿼리에 대해 일반검색해서 임베딩 검색할 후보군 10개 목록 uids를 얻는 함수
#---------------------------------------------------------------------------
def es_search_uids(es, esindex:str, uid_min_score:int, size:int=10, data=None):
    if data is None: #모든 데이터 조회
        data = {"match_all":{}}
    else:
        data = {"match": data}
        
    body = {
        "size": size,
        "query": data,
        "_source":{"includes": ["rfile_name","rfile_text"]}
    }
    
    response = None
    response = es.search(index=esindex, body=body)
    
    print(f'=>후보군uid_min_score:{uid_min_score}')
    print(f'=>후보군 list:{response}\n')
    
    rfilename = []
    count = 0
    docs = []
    
    for hit in response["hits"]["hits"]: 
        tmp = hit["_source"]["rfile_name"]

        # 중복 제거
        if tmp and tmp not in rfilename:
            rfilename.append(tmp)
            doc = {}  #dict 선언
            
            score = hit["_score"]
            if score > uid_min_score:  # 6 이상일때만 스코어 계산
                doc['rfile_name'] = hit["_source"]["rfile_name"]      # contextid 담음
                doc['rfile_text'] = hit["_source"]["rfile_text"]      # text 담음.
                doc['score'] = score
                docs.append(doc)
                count += 1
    
    uids = []
    for doc in docs:
        uids.append(doc['rfile_name'])

    return uids, docs
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# ES 임베딩 벡터 쿼리 실행 함수
# - in : esindex=인덱스명, query=쿼리 , search_size=검색출력계수
# - option: qmethod=0 혹은 1 혹은 2(0=max벡터 구하기, 1=평균벡터 구하기, 2=임베딩벡터가 1개인 경우 (default=0)), uid_list=검색할 uid 리스트(*엠파워에서는 검색할 문서id를 지정해서 검색해야 검색속도가 느리지 않음)
#---------------------------------------------------------------------------
def es_embed_query(settings:dict, esindex:str, query:str, 
                   search_size:int, bi_encoder, qmethod:int=0, 
                   uids:list=None):
    
    error: str = 'success'
    
    query = query.strip()
    
    #print(f'search_size: {search_size}')
    es_url = settings['ES_URL']
    uid_min_score = settings['ES_UID_MIN_SCORE']
    vector_mgr = settings['ES_SEARCH_VECTOR_MAG']
    float_type = settings['E_FLOAT_TYPE']
    vector_num = settings['NUM_CLUSTERS']
      
    # 1.elasticsearch 접속
    es = Elasticsearch(es_url)   
    
    if not query:
        error = 'query is empty'
    elif search_size < 1:
        error = 'search_size < 1'
    elif not es.indices.exists(esindex):
        error = 'esindex is not exist'
    elif qmethod < 0 or qmethod > 2:
        error = 'qmenthod is not variable'
    elif vector_num < 1:
        error = 'vector_num is not variable'
        
    if error != 'success':
        return error, None
   
    #print(f'vector_num: {type(vector_num)}/{vector_num}')

    # 후보군 목록이 없으면, es 일반검색 해서 후보군 리스트 뽑아냄.
    docs = []
    if uids == None:
        #* es로 쿼리해서 후보군 추출.
        data = {'rfile_text': query}
        uids, docs = es_search_uids(es=es, esindex=esindex, uid_min_score=uid_min_score, size=10, data=data)
        
    #print(f'\t==>es_embed_query:uids:{uids}, qmethod: {qmethod}')
    
    if len(uids) < 1:
        return error, docs # 쿼리,  rfilename, rfiletext, 스코어 리턴 
    
    # 2. 검색 문장 embedding 후 벡터값 
    # 쿼리들에 대해 임베딩 값 구함
    start_embedding_time = time.time()
    embed_query = embedding([query], bi_encoder, float_type)
    end_embedding_time = time.time() - start_embedding_time
    #print("*embedding time: {:.2f} ms".format(end_embedding_time * 1000)) 
    #print(f'*embed_querys.shape:{embed_query.shape}\n')
        
    # 3. 쿼리 만듬
    # - 쿼리 1개만 하므로, embed_query[0]으로 입력함.
    if qmethod == 0:
        script_query = make_max_query_script(query_vector=embed_query[0], vectormag=vector_mgr, vectornum=int(vector_num), uid_list=uids) # max 쿼리를 만듬.
    elif qmethod == 1:
        script_query = make_avg_query_script(query_vector=embed_query[0], vectormag=vector_mgr, vectornum=int(vector_num), uid_list=uids) # 평균 쿼리를 만듬.
    else:
        script_query = make_query_script(query_vector=embed_query[0], uid_list=uids) # 임베딩 벡터가 1개인경우=>기본 쿼리 만듬.
        
    #print(f'script_query:{script_query}')
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

    # 5. 결과 리턴
    # - 쿼리 응답 결과값에서 _id, _score, _source 등을 뽑아내고 내림차순 정렬후 결과값 리턴
    print(f'=>본문검색결과\n{response}\n')
    
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

    return error, docs # 쿼리,  rfilename, rfiletext, 스코어 리턴 

#---------------------------------------------------------------------------
# 비동기 ES 임베딩 벡터 쿼리 실행 함수
#---------------------------------------------------------------------------
async def async_es_embed_query(settings:dict, esindex:str, query:str, search_size:int, bi_encoder, qmethod:int, uids:list=None):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, es_embed_query, settings, esindex, query, search_size, bi_encoder, qmethod, uids)
#---------------------------------------------------------------------------


# main    
if __name__ == '__main__':
    main()