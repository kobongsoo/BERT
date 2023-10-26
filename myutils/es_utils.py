import os
import random
import numpy as np
from typing import Dict, List, Optional
from tqdm.notebook import tqdm

# ES 관련
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch import helpers

#---------------------------------------------------------------------------
# 인덱스내 데이터 조회 => query 이용
#---------------------------------------------------------------------------
def es_search(es, index_name, data=None):
    assert es is not None, f'error!!=>es is None'
    assert index_name is not None, f'error!!=>index_name is None'
    
    if data is None: #모든 데이터 조회
        data = {"match_all":{}}
    else:
        data = {"match": data}
        
    body = {"query": data}
    res = es.search(index=index_name, body=body)
    return res

#---------------------------------------------------------------------------
## 인덱스 내의 데이터 삭제 => query 이용
#---------------------------------------------------------------------------
def es_delete(es, index_name:str, data):
    assert es is not None, f'error!!=>es is None'
    assert index_name is not None, f'error!!=>index_name is None'
    
    if data is None:  # data가 없으면 모두 삭제
        data = {"match_all":{}}
    else:
        data = {"match": data}
        
    body = {"query": data}
    return es.delete_by_query(index=index_name, body=body)

#---------------------------------------------------------------------------
## 인덱스 내의 데이터 삭제 => id 이용
#---------------------------------------------------------------------------
def es_delete_by_id(es, index_name:str, id):
    assert es is not None, f'error!!=>es is None'
    assert index_name is not None, f'error!!=>index_name is None'
    
    return es.delete(index=index_name, id=id)

#---------------------------------------------------------------------------
## 인덱스 내의 데이터 업데이트=>_id 에 데이터 업데이트
#---------------------------------------------------------------------------
def es_update(es, index_name, id, doc, doc_type):
    assert es is not None, f'error!!=>es is None'
    assert index_name is not None, f'error!!=>index_name is None'
    
    body = {
        'doc': doc
    }
    
    res=es.update(index=index_name, id=id, body=body, doc_type=doc_type)
    return res

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

# main    
if __name__ == '__main__':
    main()