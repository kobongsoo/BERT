import torch
from sentence_transformers import SentenceTransformer, util
from sentence_transformers.cross_encoder import CrossEncoder

import kss
import numpy as np
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from tqdm.notebook import tqdm

from elasticsearch import Elasticsearch
from elasticsearch import helpers

# 추출 요약
from summarizer.sbert import SBertSummarizer

# FutureWarning 제거
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) 

import sys
sys.path.append('..')
from myutils import seed_everything, GPU_info, getListOfFiles
device = GPU_info()
#device = torch.device('cpu')

seed_everything(111)

# elastic 서버 접속 테스트
#es = Elasticsearch("https://192.168.0.91:9200/", verify_certs=False)
#es = Elasticsearch("http://192.168.0.130:9200/")
#es.info()

def load_model():
    #=====================================================================
    # 임베딩 모델 설정
    sbert_model_path = 'bongsoo/kpf-sbert-v1.1'
    # - cpu 모델로 실행할때는 device=cpu, 기본은 GPU임
    embedder = SentenceTransformer(sbert_model_path, device=device)

    text = '나는 오늘 밥을 먹는다.'
    vectors = embedder.encode(text, convert_to_tensor=True)
    print(f'vector_len:{len(vectors)}')
    #=====================================================================
    # 추출요약 모델 설정
    summarizer_sbert_model_path = 'bongsoo/albert-small-kor-sbert-v1.1'
    summarizer_model = SBertSummarizer(summarizer_sbert_model_path)
    print(summarizer_model)
    #=====================================================================
    # crossencoder 모델 설정
    crossencoder_model_path = 'bongsoo/kpf-cross-encoder-v1'
    crossencoder = CrossEncoder(crossencoder_model_path, device=device)
    print(crossencoder)
    #=====================================================================

# 인덱싱 함수 
def index_data():
    
    es.indices.delete(index=INDEX_NAME, ignore=[404])
    
    count = 0
       
    # 인덱스 생성
    with open(INDEX_FILE) as index_file:
        source = index_file.read().strip()
      
        count += 1
        print(f'{count}:{source}')
      
        es.indices.create(index=INDEX_NAME, body=source)
        
  
    # json 파일들이 있는 폴더에 .json 파일 이름들을 얻기
    # =>DATA_FOLDER: .JSON파일들이 있는 폴더
    files = getListOfFiles(DATA_FOLDER)
    assert len(files) > 0 # files가 0이면 assert 발생
    
    print('*file_count: {}, file_list:{}'.format(len(files), files[0:5]))
 
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
            
            #================================================================
            # 추출요약 적용된 경우에는 입력문장에 대한 요약문장 추출함.
            if SUMMARIZER == True:
                paragraph_summarize = summarizer_model(paragraph, 
                                                       min_length=SUMMARIZER_MIN_LENGTH, 
                                                       num_sentences=SUMMARIZER_NUM_SENTENCE)
                # 요약문이 있으면 제목. + 요약문  담고, 없으면 제목. + 원본문장 담음.
                if paragraph_summarize:
                    doc['summarize'] = paragraph_summarize
                else:
                    doc['summarize'] = paragraph
            #================================================================
            
            doc['title'] = data['title']            # 제목 설정
            doc['paragraph'] = data['content']    # 문장 담음.
                
            docs.append(doc)
            #print(f'count:{count}')
            #print(doc['title'])
            
            if count % BATCH_SIZE == 0:
                index_batch(docs)
                docs = []
                print("Indexed {} documents.".format(count))
                  
            # ** 10 개만 보냄
            #if count >= 10:
            #   break
            
        if docs:
            index_batch(docs)
            print("Indexed {} documents.".format(count))   
            
        es.indices.refresh(index=INDEX_NAME)
            
    es.indices.refresh(index=INDEX_NAME)
    #print("=== End Done indexing===")
                   
    
# 문단(paragraph)들 분리
# 문장으로 나누고, 해당 vector들의 평균을 구함.
# =>굳이 elasticsearch에 문단 벡터는 추가하지 않고, title 벡터만 이용해도 되므로 주석처리함

def paragraph_index(paragraph):
    avg_paragraph_vec = np.zeros((1,768))
    sent_count = 0
    
    # ** kss로 분할할때 히브리어: מר, 기타 이상한 특수문자 있으면 에러남. 
    # 따라서 여기서는 그냥 . 기준으로 문장을 나누고 평균을 구함
    # 하나의 문장을 읽어와서 .기준으로 나눈다.
    sentences = [sentence for sentence in paragraph.split('. ') if sentence != '' and len(sentence) > 20]
    for sent in sentences:
        # 문장으로 나누고, 해당 vector들의 평균을 구함.
        avg_paragraph_vec += embed_text([sent])
        sent_count += 1
  
        # 최대 10개 문장만 처리함 
        if sent_count >= 10:
            break
    '''
    # kss로 분할할때 줄바꿈 있으면, 파싱하는데 에러남.따라서 "\n"는 제거함
    paragraph = paragraph.replace("\n","")
    
    print("==Start paragraph_index==")
    print(paragraph)
    for sent in kss.split_sentences(paragraph):
        # 문장으로 나누고, 해당 vector들의 평균을 구함.
        avg_paragraph_vec += embed_text([sent])
        sent_count += 1
        
        # 최대 10개 문장만 처리함 
        if sent_count >= 10:
            break
    '''
    # 0으로 나누면 배열이 nan(not a number)가 되어 버리므로, 반드시 0>큰지 확인해야 함
    if sent_count > 0:
        avg_paragraph_vec /= sent_count
    return avg_paragraph_vec.ravel(order='C') # 1차원 배열로 변경


def index_batch(docs):
   
    # 제목 벡터를 구함
    titles = [doc["title"] for doc in docs]  
    title_vectors = embed_text(titles)      
    
    # 문단 벡터를 구함
    if PARAGRAPH_AVG == True:
        # * cpu로 문장별 평균을 구하는 경우에는 임베딩하는데 너무 오래 걸림.
        paragraph_vectors = [paragraph_index(doc["paragraph"]) for doc in docs]
    else:
        # 원본문장 벡터를 구함 => 전체벡터를 구함
        paragraphs = [doc["paragraph"] for doc in docs]   
        paragraph_vectors = embed_text(paragraphs)
      
    #=========================================================================
    # 요약문 각 문장별 벡터를 구하고 평균을 냄
    if SUMMARIZE_AVG_INDEX == True:
        summarize_vectors = [paragraph_index(doc["summarize"]) for doc in docs]
    # 요약문 전체 벡터를 구함    
    else:
        paragraph_summarizes = [doc["summarize"] for doc in docs]
        summarize_vectors = embed_text(paragraph_summarizes)
     #=========================================================================    
   
    requests = []
    
    # ES request 할 리스트 정의
    #for i, doc in enumerate(tqdm(docs)):
    for i, doc in enumerate(docs):
        request = {}  #dict 정의
        
        # 요약벡터 = 타이틀벡터 + 요약벡터 의 평균으로 함
        summarize_vector = (title_vectors[i] + summarize_vectors[i]) / 2
        '''
        request["title"] = doc["title"]            # 제목               
        request["paragraph"] = doc["paragraph"]    # 문장
        request["summarize"] = doc["summarize"]    # 요약문
        
        request["_op_type"] = "index"        
        request["_index"] = INDEX_NAME
        
        request["title_vector"] = title_vectors[i]          # 제목 벡터
        request["paragraph_vector"] = paragraph_vectors[i]  # 문장 벡터
        request["summarize_vector"] = summarize_vector #summarize_vectors[i]  # 요약문 벡터
        '''
        # mpower10u.json 인덱스일때...
        request["rfile_name"] = doc["title"]       # 제목               
        request["rfile_text"] = doc["paragraph"]   # 문장
        request["rfile_sum"] = doc["summarize"]    # 요약문
        
        request["_op_type"] = "index"        
        request["_index"] = INDEX_NAME
        
        request["name_vector"] = title_vectors[i]          # 제목 벡터
        request["text_vector"] = paragraph_vectors[i]  # 문장 벡터
        request["sum_vector"] = summarize_vector #summarize_vectors[i]  # 요약문 벡터
        
        requests.append(request)
        
    # batch 단위로 한꺼번에 es에 데이터 insert 시킴     
    bulk(es, requests)
    
# embedding 모델에서 vector를 구함    
def embed_text(input):
    vectors =  embedder.encode(input, convert_to_tensor=True)
    return [vector.cpu().numpy().tolist() for vector in vectors]

#======================================================================================
# ElasticSearch(이하:ES) 데이터 인텍싱
# - ElasticSearch(이하:ES)에 KorQuAD_v1.0_train_convert.json 파일에 vector값을 구하여 index 함
#
# => index 명 : korquad
# => index 구조 : index_1.json 파일 참조
# => BATCH_SIZE : 100 => 100개의 vector값을 구하여, 한꺼번에 ES에 인텍스 데이터를 추가함.
#======================================================================================
def main():
    INDEX_NAME = 'aihub-ts1-bwsg-kpf-sbert-v1.1-mpower10u-enable-1'  # ES 인덱스 명 (*소문자로만 지정해야 함)
    INDEX_FILE = './data/mpower10u.json'                 # 인덱스 구조 파일
    DATA_FOLDER = '../../../data11/ai_hub/ts1/사회일반/'        # 인덱스할 파일들이 있는 폴더경로 
    BATCH_SIZE = 100

    SUMMARIZER = True            # TRUE면 추출요약을 한다.
    SUMMARIZER_NUM_SENTENCE = 2  # 추출요약할때 몇문장으로 요약할지
    SUMMARIZE_AVG_INDEX = True   # True면 요약문장들에 대해 각 문장의 embedding을 구하고, 평균을 낸다.
    SUMMARIZER_MIN_LENGTH = 20              # 추출요약할때 해당 길이보다 작은 문장은 제외함.

    PARAGRAPH_AVG = True         # True이면 문단벡터 구할때 모든 문장의 평균치 벡터를 구함, False이면 문단 전체 벡터를 구함

    # 1. elasticsearch 접속
    es = Elasticsearch("http://192.168.0.27:9200/")
    print(es.info())

    # 2. index 처리
    index_data()
    
if __name__ == '__main__':
    load_model()
    main()
    