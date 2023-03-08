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

import time

# FutureWarning 제거
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) 

import sys
sys.path.append('..')
from myutils import seed_everything, GPU_info, getListOfFiles
device = GPU_info()
#device = torch.device('cpu')

#------------------------------------------------------------------------------------
# 0. param 설정
#------------------------------------------------------------------------------------
seed = 111
query_num = 500             # 쿼리 최대 갯수: KorQuAD_v1.0_dev.json 최대값은 5533개임, 0이면 모든 5533개 쿼리함.
search_k = 5                # FAISS 검색시, 검색 계수(5=쿼리와 가장 근접한 5개 결과값을 반환함)
avg_num = 1                 # 쿼리에 대해 sub 문장들중 최대 scorce를 갖는 문장을 몇개 찾고 평균낼지.(3=쿼리에 가장 유사한 sub문장 3개를 찾고 평균을 냄)
faiss_index_method = 0      # 0= Cosine Similarity 적용(IndexFlatIP 사용), 1= Euclidean Distance 적용(IndexFlatL2 사용)

# 토큰 임베딩 관련 param
IS_EMBED_DIVIDE = True      #여기서는 토큰 임베딩은 True고정, True=문단의 여러 문장을, 토큰 단위로 분리후 벡터 구해서 인덱스 만듬/False=문단의 여러문장을 하나의 벡터를 구해서 인덱스 만듬.
EMBED_DIVIDE_LEN = [5,7,9]  #5 # 문장을 몇개(토큰)으로 분리할지 (7,8,10) 일때 성능 좋음=>50.8%, (5,7,9) 일때 차원축소 128=>41.80%(81.8%) 성능 좋음
MAX_TOKEN_LEN = 40          # 최대 몇개 token까지만 임베딩 할지

# 차원 축소 관련 param
# 차원 축소 할지, 768 값을 앞에 384 만큼만 배열 resize 시킴.  
# - 384로 줄일대 -2% 성능 저하 발생(512: -1.2%, 256: -6%)
DIM_RESIZE_METHOD = 2  # 0=차원축소 안함/1=resize 로 차원축소/2=Dense 모델 이용 차원축소
DIM_RESIZE_LEN = 128

# ONNX 모델 사용
IS_ONNX_MODEL = True        # True=onnx 모델 사용

#------------------------------------------------------------------------------------
INDEX_NAME = 'aihub-ts1-acsampe-klue-sbert-v1-mpower10u-128d-onnx-1'  # ES 인덱스 명 (*소문자로만 지정해야 함)
INDEX_FILE = './data/mpower10u_128d.json'                 # 인덱스 구조 파일
DATA_FOLDER = '../../../data11/ai_hub/ts1/sample4/'     # 인덱스할 파일들이 있는 폴더경로 
BATCH_SIZE = 100

#------------------------------------------------------------------------------------

seed_everything(seed)

#-------------------------------------------------------------------------------------
# 1. 검색모델 로딩
# => bi_encoder 모델 로딩, polling_mode 설정
#-------------------------------------------------------------------------------------
from myutils import bi_encoder, dense_model, onnx_model

# bi_encoder 모델 로딩
bi_encoder_path = "bongsoo/klue-sbert-v1"
pooling_mode = 'mean' # bert면=mean, albert면 = cls
 # 출력 임베딩 크기 지정 : 0=기본 모델 임베딩크기(768), 예:128=128 츨력임베딩 크기 
out_dimension = 128 if DIM_RESIZE_METHOD == 2 else 0 if DIM_RESIZE_METHOD != 2 else None
    
word_embedding_model1, bi_encoder1 = bi_encoder(model_path=bi_encoder_path, max_seq_len=512, do_lower_case=True, 
                                              pooling_mode=pooling_mode, out_dimension=out_dimension, device=device)
print(f'---bi_encoder---------------------------')   
print(bi_encoder1)
print(word_embedding_model1)

print(f'---dense param---------------------------')   
# 출력 값 차원 축소 지정인 경우, token_embeddings 일때는 sentencebert 라이브러리를 이용하여 dense_model 모델 추가할수 없으므로,
# 사용자정의 dense_model을 정의해서, 가중치와 bias를 bi_encoder모델에 것을 얻어와서 적용해서 차원 죽소함.
# => resize 방식 보다 성능 떨어지지만, 128일때는 더 성능이 좋음
if DIM_RESIZE_METHOD == 2:
    #-------------------------------------------------------------------------
    # 처음에는 아래 코드를 활용하여 해당 모델의 128 weight와 bias를 저장해 두어야 함.
    #state_dict = bi_encoder1.state_dict()  # bi_encoder모델이 state_dict 얻어옴
    #print(state_dict.keys())
    #dense_weight = state_dict['2.linear.weight'] # denser 모델에 bi_encoder모델이 linear.weight 적용
    #dense_bias = state_dict['2.linear.bias']     # denser 모델에 bi_encoder모델이 linear.bias 적용
    
    # 처음에  weigth, bias 파일을 저장해 둠.
    #torch.save(dense_weight, 'klue-sbert-v1-weigth.pt')
    #torch.save(dense_bias, 'klue-sbert-v1-bias.pt')
    #-------------------------------------------------------------------------
    # weigth, bias 저장해둔 파일 로딩
    dense_weight = torch.load('../embedding_sample/faiss/data/dense_weight/klue-sbert-v1-weight-128.pt')
    dense_bias = torch.load('../embedding_sample/faiss/data/dense_weight/klue-sbert-v1-bias-128.pt')

    print('*dense_weight:{}'.format(dense_weight.size()))
    print(f'*dense_bias:{dense_bias.size()}')
 
# onnx 모델 로딩
if IS_ONNX_MODEL == True:
    onnx_model_path = "bongsoo/klue-sbert-v1-onnx"#"bongsoo/klue-sbert-v1-onnx"
    onnx_tokenizer, onnx_model = onnx_model(onnx_model_path)
    print(f'---onnx_model---------------------------')
    print(onnx_model)

#-------------------------------------------------------------------------------------
# 1. elasticsearch 접속
es = Elasticsearch("http://192.168.0.27:9200/")
print(es.info())
#-------------------------------------------------------------------------------------
    
#-------------------------------------------------------------------------------------
# 안덱싱 및 검색 조건에 맞게 임베딩 처리 하는 함수 
#-------------------------------------------------------------------------------------
from myutils import embed_text, onnx_embed_text

def embedding(paragrphs:list):
    if IS_ONNX_MODEL == True:
        if IS_EMBED_DIVIDE == True: # 한 문단에 대한 40개 문장들을 토큰단위로 쪼개서 임베딩 처리함  
            #----------------------------------------------------
            # 한 문단에 대한 문장들의 토큰을 ?개씩 나누고 비교.
            # - 한 문단에 대한 문장들에 대해 [tensor(250,768), tensor(243,768), tensor(111,768),..] tensor 리스트 타입으로 벡터 생성됨.
            #----------------------------------------------------
            embeddings = onnx_embed_text(model=onnx_model, tokenizer=onnx_tokenizer, paragraphs=paragrphs) 
        else: # 한 문단에 대한 40개 문장 배열들을 한꺼번에 임베딩 처리함
            embeddings = onnx_embed_text(model=onnx_model, tokenizer=onnx_tokenizer, paragraphs=paragrphs, token_embeddings=False)
    else:
        if IS_EMBED_DIVIDE == True: # 한 문단에 대한 40개 문장들을 토큰단위로 쪼개서 임베딩 처리함  
            #----------------------------------------------------
            # 한 문단에 대한 문장들의 토큰을 ?개씩 나누고 비교.
            # - 한 문단에 대한 문장들에 대해 [tensor(250,768), tensor(243,768), tensor(111,768),..] tensor 리스트 타입으로 벡터 생성됨.
            #----------------------------------------------------
            embeddings = embed_text(model=bi_encoder1, paragraphs=paragrphs, token_embeddings=True, return_tensor=False)
        else: # 한 문단에 대한 40개 문장 배열들을 한꺼번에 임베딩 처리함
            embeddings = embed_text(model=bi_encoder1, paragraphs=paragrphs, return_tensor=False)  
            
    return embeddings

#-------------------------------------------------------------------------------------
# 안덱싱 처리
#-------------------------------------------------------------------------------------
from tqdm import tqdm
import kss
from myutils import embed_text, divide_arr_avg_exten, clean_text

# 인덱싱 함수 
def index_data(createindex:bool = True):
    
    if createindex == True:
        es.indices.delete(index=INDEX_NAME, ignore=[404])
        count = 0
        # 인덱스 생성
        with open(INDEX_FILE) as index_file:
            source = index_file.read().strip()
            count += 1
            #print(f'{count}:{source}') # 인덱스 구조 출력
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
        for data in json_data:
        #for data in json_data:
            count += 1
            doc = {} #dict 선언
            
            doc['title'] = data['title']            # 제목 설정
            doc['paragraph'] = data['content']      # 문장 담음.
                
            docs.append(doc)
            #print(f'count:{count}')
            #print(doc['title'])
            
            if count % BATCH_SIZE == 0:
                start = time.time()
                    
                index_batch(docs)
                docs = []
                print(f'*Indexed {count} documents./time:{time.time()-start:.4f}')
                
                  
            # ** 10 개만 보냄
            #if count >= 10:
            #   break
            
        if docs:
            index_batch(docs)
            print("Indexed {} documents.".format(count))   
            
        es.indices.refresh(index=INDEX_NAME)
            
    es.indices.refresh(index=INDEX_NAME)
    #print("=== End Done indexing===")
                   

def index_batch(docs):
        
    requests = []
    
    for i, doc in enumerate(tqdm(docs)):
        title = doc['title']
        paragraph = doc['paragraph']

        sub_contexts = []
        #------------------------------------------------------------------------------------------------------------------------
        paragraph = clean_text(paragraph)  # 전처리 : (한글, 숫자, 영문, (), {}, [], %, ,,.,",')  등을 제외한 특수문자 제거
        
        # 입력 문단 길이가 999개 크면, 속도가 느려지므로 최대 999개 까지만 문자 입력 받음.
        if len(paragraph) > 999:
            #print(f'paragraph_len:{len(paragraph)}')
            paragraph = paragraph[0:999]
            
        # 입력 문단을 여러 문장들로 나눔.
        #sentences = [sentence for sentence in paragraph.split('.') if sentence != '' and len(sentence) > 10]  # '.'(마침표) 로 구분해서 sub 문장을 만듬.
        #sentences = [sentence for sentence in kss.split_sentences(paragraph) if sentence != '' and len(sentence) > 10] # kss 이용해서 sub 문장을 만듬
        
        # 최대 10개 문장만 추출함.
        sentences = []
        count = 0
        for sentence in kss.split_sentences(paragraph):
            if sentence != '' and len(sentence) > 10:
                sentences.append(sentence)
                if count > 10:
                    break
                    
        # 만약 sentences(sub 문장) 가 하나도 없으면 원본문장을 담고, 10이상이면  10개만 담음.
        sub_contexts.append([paragraph] if len(sentences) < 1 else sentences[0:10] if len(sentences) > 10 else sentences)
       
        if i < 1:
            print(sub_contexts[0])
        
        #------------------------------------------------------------------------------------------------------------------------
        # 토큰 분할 임베딩 처리
        # => sub_contexts은  1차원 리스트 임 (예:['오늘 비가 온다','오늘 눈이 온다','날씨가 좋다'])
        token_embeds = embedding(sub_contexts[0])
        #------------------------------------------------------------------------------------------------------------------------ 
        # 토큰 분할인 경우 처리 start=>           
        token_embed_arr_list = []
        tcount = 0
        # tensor(250,768) 한문장 토큰 임베딩 얻어와서, 각 ?개 토큰씩 평균을 구함.
        for token_embed in token_embeds:
            token_embed = token_embed[1:-1] # 맨앞에 [CLS]와 맨뒤에 [SEP] 토큰은 뺌
            if tcount >= MAX_TOKEN_LEN: 
                break
             
            #print(f'token_embed.shape:{token_embed.shape}')
            
            token_embed_arrs = token_embed.cpu().numpy().astype('float32')
            #print(f'token_embed_arrs:{token_embed_arrs.shape}')
            # 5,7,10 씩 자르면서 문장 토큰 평균을 구함
            token_embed_divide_arrs = divide_arr_avg_exten(embed_arr=token_embed_arrs, divide_arrs=EMBED_DIVIDE_LEN) 

             # Dense 방식으로 차원 축소 => 평균 구한후 차원 축소하는 방식이 0.6% 정도 성능 좋음
            if DIM_RESIZE_METHOD == 2:
                tmp1 = torch.Tensor(token_embed_divide_arrs)
                #tmp1 = torch.from_numpy(token_embed_divide_arrs)
                debug1 = False
                tmp2 = dense_model(embed_tensor=tmp1, out_f=DIM_RESIZE_LEN, weight=dense_weight, bias=dense_bias, debug=debug1)
                arrs = tmp2.detach().numpy().astype('float32')
            else:  
                arrs = token_embed_divide_arrs
                
            # 평균 구한 토큰들을 token_embed_arr_list 리스트에 담아둠.(50보다 크면 50개만 담음)           
            for idx, arr in enumerate(arrs):
                
                 # Resize 방식으로 차원 축소(384로 줄일대 -2% 성능 저하 발생)
                if DIM_RESIZE_METHOD == 1:
                    darr = np.resize(arr, (DIM_RESIZE_LEN,))
                else:
                    darr = arr
                    
                token_embed_arr_list.append(darr)
                tcount +=1
                if tcount >=MAX_TOKEN_LEN:
                    break

        #embeddings = np.array(token_embed_arr_list)
        #------------------------------------------------------------------------------------------------------------------------
        # ES에 문단 인덱싱 처리
        request = {}  #dict 정의
        request["rfile_name"] = title       # 제목               
        request["rfile_text"] = paragraph   # 문장
        
        request["_op_type"] = "index"        
        request["_index"] = INDEX_NAME
        
        # for문 돌면서 벡터 처리
        #print(type(token_embed_arr_list))
        #print(len(token_embed_arr_list))
        
        # vector 1~40 까지 값을 0으로 초기화 해줌.
        for i in range(MAX_TOKEN_LEN):
            if DIM_RESIZE_METHOD > 0:
                request["vector"+str(i+1)] = np.zeros((DIM_RESIZE_LEN))
            else:
                request["vector"+str(i+1)] = np.zeros((768))
            
        # vector 값들을 담음.
        for i, token_embed_arr in enumerate(token_embed_arr_list):
            request["vector"+str(i+1)] = token_embed_arr
            
        requests.append(request)
        #------------------------------------------------------------------------------------------------------------------------
                
    # batch 단위로 한꺼번에 es에 데이터 insert 시킴     
    bulk(es, requests)
    
#======================================================================================
# ElasticSearch(이하:ES) 데이터 인텍싱
# - ElasticSearch(이하:ES)에 KorQuAD_v1.0_train_convert.json 파일에 vector값을 구하여 index 함
#
# => index 명 : korquad
# => index 구조 : index_1.json 파일 참조
# => BATCH_SIZE : 100 => 100개의 vector값을 구하여, 한꺼번에 ES에 인텍스 데이터를 추가함.
#======================================================================================
def main():
    #======================================================================================
    # ElasticSearch(이하:ES) 데이터 인텍싱
    # - ElasticSearch(이하:ES)에 KorQuAD_v1.0_train_convert.json 파일에 vector값을 구하여 index 함
    #
    # => index 명 : korquad
    # => index 구조 : index_1.json 파일 참조
    # => BATCH_SIZE : 100 => 100개의 vector값을 구하여, 한꺼번에 ES에 인텍스 데이터를 추가함.
    #======================================================================================
  
    # 2. index 처리
    start = time.time()
    
    index_data(False)
    
    print(f'*인덱싱 총 시간 : {time.time()-start:.4f}')
    
if __name__ == '__main__':
    main()
    