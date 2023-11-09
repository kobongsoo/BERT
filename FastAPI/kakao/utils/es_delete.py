import torch
import time
import os
import numpy as np
from tqdm.notebook import tqdm

import asyncio
from elasticsearch import Elasticsearch

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
## 인덱스 내의 데이터 삭제 => id 이용
#---------------------------------------------------------------------------
def es_delete_by_id(es, index_name:str, id):
    assert es is not None, f'error!!=>es is None'
    assert index_name is not None, f'error!!=>index_name is None'
    
    return es.delete(index=index_name, id=id)

#---------------------------------------------------------------------------
# ES 임베딩 도큐먼트 삭제 함수
# -> 삭제할 _id를 얻어와서 삭제함.
# - in : esindex=인덱스명, rfile_name=파일 유니크한 값(sfileid, contxtsid) 
#---------------------------------------------------------------------------
def es_embed_delete(esindex:str, uids:str, es_url:str):
    
    error: int = 0
    
    # 1.elasticsearch 접속
    es = Elasticsearch(es_url)      
    #print(f'==>es_url:{es_url}')
    
    data = {'rfile_name': uids} # **인덱스 형식에 따라 변경해줘야함.
    #print(f'==>data:{data}')
    
    # 2. 쿼리 검색후 _id 얻어옴.
    id_list = []
    res=es_search(es, index_name=esindex, data=data)
    #print(f'==>res:{res}')
    
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
async def async_es_embed_delete(esindex:str, uids:str, es_url:str):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, es_embed_delete, esindex, uids, es_url)
#---------------------------------------------------------------------------

# main    
if __name__ == '__main__':
    main()