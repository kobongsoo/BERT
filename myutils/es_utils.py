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
# ES 쿼리 스크립트 구성
# -in: query_vector = 1차원 임베딩 벡터 (예: [10,10,1,1, ....]
# -in: vectornum : ES 인덱스 벡터 수
#---------------------------------------------------------------------------
def make_query_script(query_vector, vectornum:int=10, vectormag:float=0.8)->str:
    # 문단별 40개의 벡터와 쿼리벡터를 서로 비교하여 최대값 갖는 문단들중 가장 유사한  문단 출력
    # => script """ 안에 코드는 java 임.
    # => "queryVectorMag": 0.1905 일때 100% 일치하는 값은 9.98임(즉 10점 만점임)
    script_query = {
        "script_score":{
            "query":{
                "match_all": {}
            },
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

# main    
if __name__ == '__main__':
    main()