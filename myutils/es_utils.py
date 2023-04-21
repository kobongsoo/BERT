import os
import random
import numpy as np
from typing import Dict, List, Optional

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