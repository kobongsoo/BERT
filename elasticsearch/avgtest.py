
import torch
from sentence_transformers import SentenceTransformer, util
from sentence_transformers.cross_encoder import CrossEncoder

import kss
import numpy as np
import json
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from tqdm import tqdm

from elasticsearch import Elasticsearch
from elasticsearch import helpers


# FutureWarning 제거
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) 

import sys
sys.path.append('..')
from myutils import seed_everything, GPU_info, getListOfFiles, embed_text, embed_text_avg
device = GPU_info()
#device = torch.device('cpu')

seed_everything(111)

#-------------------------------------------------------------------------------------
# 1.임베딩 모델 설정
sbert_model_path = 'bongsoo/klue-sbert-v1'
# - cpu 모델로 실행할때는 device=cpu, 기본은 GPU임
embedder = SentenceTransformer(sbert_model_path, device=device)

text = '나는 오늘 밥을 먹는다.'
vectors = embedder.encode(text, convert_to_tensor=True)
print(f'vector_len:{len(vectors)}')
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# 1. elasticsearch 접속

# ElasticSearch(이하:ES) 데이터 인텍싱
# - ElasticSearch(이하:ES)에 KorQuAD_v1.0_train_convert.json 파일에 vector값을 구하여 index 함
#
# => index 명 : korquad
# => index 구조 : index_1.json 파일 참조
# => BATCH_SIZE : 100 => 100개의 vector값을 구하여, 한꺼번에 ES에 인텍스 데이터를 추가함.

INDEX_NAME = 'aihub-bwsg-klue-sbert-v1-mpower10u-enable-true-768d'  # ES 인덱스 명 (*소문자로만 지정해야 함)
INDEX_FILE = './data/mpower10u-enable-true.json'                 # 인덱스 구조 파일
DATA_FOLDER = '../../../data11/ai_hub/ts1/사회일반/'        # 인덱스할 파일들이 있는 폴더경로 
BATCH_SIZE = 100

PARAGRAPH_AVG = True         # True이면 문단벡터 구할때 모든 문장의 평균치 벡터를 구함, False이면 문단 전체 벡터를 구함

es = Elasticsearch("http://192.168.0.27:9200/")
print(es.info())
#-------------------------------------------------------------------------------------

# 인덱싱 함수 
def index_data(createindex:bool=True):
    
    es.indices.delete(index=INDEX_NAME, ignore=[404])
    
    count = 0
       
    # 인덱스 생성
    if createindex == True:
        with open(INDEX_FILE) as index_file:
            source = index_file.read().strip()

            count += 1
            print(f'{count}:{source}')

            es.indices.create(index=INDEX_NAME, body=source)
        
  
    # json 파일들이 있는 폴더에 .json 파일 이름들을 얻기
    # =>DATA_FOLDER: .JSON파일들이 있는 폴더
    files = getListOfFiles(DATA_FOLDER)
    assert len(files) > 0 # files가 0이면 assert 발생
    
    print('*file_count: {}, file_list:{}\n'.format(len(files), files[0:5]))
 
    for idx, file in enumerate(tqdm(files)):
        if ".json" not in file:  #.json 파일이 아니면 합치지 않음
            continue
            
        count = 0
        docs = []
    
        # json 파일 로딩 => [SJML][text] entry만 불러옴
        json_data = json.load(open(file, "r", encoding="utf-8"))['SJML']['text']
        for data in tqdm(json_data):
        #for data in json_data:
            count += 1
            doc = {} #dict 선언
            
            paragraph = data['content']

            doc['title'] = data['title']            # 제목 설정
            doc['paragraph'] = data['content']    # 문장 담음.
                
            docs.append(doc)
            #print(f'count:{count}')
            #print(doc['title'])
            
            if count % BATCH_SIZE == 0:
                index_batch(docs)
                docs = []
                print("Indexed {} documents.".format(count))
                  
        if docs:
            index_batch(docs)
            print("Indexed {} documents.".format(count))   
            
        es.indices.refresh(index=INDEX_NAME)
            
    es.indices.refresh(index=INDEX_NAME)
    #print("=== End Done indexing===")
                   
    
def index_batch(docs):
   
    start = time.time()
    print(f'*임베딩 시작==>')
        
    # 제목 벡터를 구함
    titles = [doc["title"] for doc in docs]  
    #title_vectors = embed_text(model=embedder, paragraphs=titles)      
    
    # 문단 벡터를 구함
    if PARAGRAPH_AVG == True:
        # * cpu로 문장별 평균을 구하는 경우에는 임베딩하는데 너무 오래 걸림.
        paragraph_vectors = [embed_text_avg(model=embedder, paragraph=doc["paragraph"]) for doc in docs]
    else:
        # 원본문장 벡터를 구함 => 전체벡터를 구함
        paragraphs = [doc["paragraph"] for doc in docs]   
        paragraph_vectors = embed_text(paragraphs)
   
    requests = []
    
    print(f'*임베딩 완료(시간) : {time.time()-start:.4f}')
    start = time.time()
    
    # ES request 할 리스트 정의
    #for i, doc in enumerate(tqdm(docs)):
    for i, doc in enumerate(docs):
        request = {}  #dict 정의
      
        # mpower10u.json 인덱스일때...
        request["rfile_name"] = doc["title"]       # 제목               
        request["rfile_text"] = doc["paragraph"]   # 문장
        
        if i==0:
            print(doc["title"])
            print(paragraph_vectors[i][0:10])
            print()
        
        request["_op_type"] = "index"        
        request["_index"] = INDEX_NAME
        
        request["vector1"] = paragraph_vectors[i]  # 문장 벡터
        #request["vector1"] = np.zeros((768))      # zero 벡터
        requests.append(request)
        
    # batch 단위로 한꺼번에 es에 데이터 insert 시킴     
    bulk(es, requests)

    print(f'*인덱싱 완료(시간) : {time.time()-start:.4f}')
    
def main():
  
    # 2. index 처리
    start = time.time()
    
    index_data(True)
    
    print(f'*인덱싱 총 시간 : {time.time()-start:.4f}')
    
if __name__ == '__main__':
    main()