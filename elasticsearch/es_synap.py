
import os
import platform

# os가 윈도우면 from eunjeon import Mecab 
if platform.system() == 'Windows':
    os.environ["OMP_NUM_THREADS"] = '1' # 윈도우 환경에서는 쓰레드 1개로 지정함

import torch
import pandas as pd
import time
import kss
import numpy as np
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from tqdm.notebook import tqdm

from sentence_transformers import SentenceTransformer, util
from sentence_transformers.cross_encoder import CrossEncoder

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from sklearn.cluster import KMeans

# FutureWarning 제거
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) 

import sys
sys.path.append('..')
from myutils import seed_everything, GPU_info, mlogging, getListOfFiles
from myutils import remove_reverse, getListOfFiles, clean_text
from myutils import embed_text, onnx_embed_text, fassi_index, clustering_embedding, kmedoids_clustering_embedding
from myutils import sliding_window_tokenizer, split_sentences, split_sentences1, get_text_chunks


logger = mlogging(loggername="synap", logfilename="../../log/synap")
device = GPU_info()
#device = torch.device('cpu')

#------------------------------------------------------------------------------------
# 0. param 설정
#------------------------------------------------------------------------------------
seed = 111
query_num = 0               # 쿼리 최대 갯수: KorQuAD_v1.0_dev.json 최대값은 5533개임, 0이면 모든 5533개 쿼리함.
search_k = 5                # FAISS 검색시, 검색 계수(5=쿼리와 가장 근접한 5개 결과값을 반환함)
avg_num = 1                 # 쿼리에 대해 sub 문장들중 최대 scorce를 갖는 문장을 몇개 찾고 평균낼지.(3=쿼리에 가장 유사한 sub문장 3개를 찾고 평균을 냄)
faiss_index_method = 1      # 0= Cosine Similarity 적용(IndexFlatIP 사용), 1= Euclidean Distance 적용(IndexFlatL2 사용)

# 임베딩 방식 (0=문장클러스터링, 1=문장평균임베딩, 2=문장임베딩)
EMBEDDING_METHOD = 0    
FLOAT_TYPE = 'float16'     # 'float32' 혹은 'float16' => 모델임베딩후 출력되는 벡터 float 타입을 지정.=>단 FAISS에 인덱스할때는 'float32'만 지원하므로, .astype('float32')로 형변환 해줘야 함.

# 청크 분할 혹은 슬라이딩 윈도우param
IS_SLIDING_WINDOW = False
WINDOW_SIZE=256             # 문단을 몇 token으로 나눌지          (128,0)=>78.40%, (256, 64)=>75.20%
SLIDING_SIZE=0              # 중첩되는 token 

# 클러스트링 param
CLUSTRING_MODE = "kmeans"  # "kmeans" = k-평균 군집 분석, kmedoids =  k-대표값 군집 분석
num_clusters = 10           # 클러스터링 계수 
outmode = "mean"           # 클러스터링후 출력벡터 정의(kmeans 일때 => mean=평균벡터 출력, max=최대값벡터출력 / kmedoids 일때=>mean=평균벡터, medoid=대표값벡터)

# ONNX 모델 사용 유.무
IS_ONNX_MODEL = False

# 차원 축소
out_dimension = 128  # 768은 0으로 입력, 128=128 입력
if out_dimension == 0:
    dimension=768
    
# 문장 전처리
remove_sentence_len = 8    # 문장 길이가 10이하면 제거 
remove_duplication = False  # 중복된 문장 제거(*중복된 문장 제거 안할때 1%정도 정확도 좋음)

# ES 관련 Param
INDEX_NAME = 'mpower_128d_10_float16'  # ES 인덱스 명 (*소문자로만 지정해야 함)
INDEX_FILE = './data/mpower10u_128d_10.json'                 # 인덱스 구조 파일
BATCH_SIZE = 20  # 배치 사이즈 = 20이면 20개씩 ES에 인덱싱함.
#------------------------------------------------------------------------------------

assert FLOAT_TYPE == 'float16' or FLOAT_TYPE == 'float32', f'FLOAT_TYPE은 float16, float32 만 입력가능합니다. 현재 입력 FLOAT_TYPE={FLOAT_TYPE}'
assert CLUSTRING_MODE == 'kmeans' or CLUSTRING_MODE == 'kmedoids', f'CLUSTRING_MODE는 kmeans, kmedoids 만 입력가능합니다. 현재 입력 CLUSTRING_MODE={CLUSTRING_MODE}'
assert EMBEDDING_METHOD == 0 or EMBEDDING_METHOD == 1 or EMBEDDING_METHOD == 2, f'EMBEDDING_METHOD는  0,1,2 만 입력가능합니다. 현재 입력 EMBEDDING_METHOD={EMBEDDING_METHOD}'
assert out_dimension == 0 or out_dimension == 128, f'out_dimension는  0,128 만 입력가능합니다. 현재 입력 out_dimension={out_dimension}'

seed_everything(seed)

#-------------------------------------------------------------------------------------
# 1. 검색모델 로딩
# => bi_encoder 모델 로딩, polling_mode 설정
# => bi_encoder1 = SentenceTransformer(bi_encoder_path) # 오히려 성능 떨어짐. 이유는 do_lower_case나, max_seq_len등 세부 설정이 안되므로.
#-------------------------------------------------------------------------------------
import torch
from myutils import bi_encoder, dense_model, onnx_model, onnx_embed_text
from sentence_transformers import SentenceTransformer

#bi_encoder_path = "../../data11/model/bert/moco-sentencebertV2.0-nli_128d-sts" 
bi_encoder_path = "bongsoo/kpf-sbert-128d-v1" #"bongsoo/kpf-sbert-v1.1" # kpf-sbert-v1.1 # klue-sbert-v1 # albert-small-kor-sbert-v1.1
pooling_mode = 'mean' # bert면=mean, albert면 = cls


word_embedding_model1, bi_encoder1 = bi_encoder(model_path=bi_encoder_path, max_seq_len=512, do_lower_case=True, 
                                                pooling_mode=pooling_mode, out_dimension=out_dimension, device=device)
  
print(f'\n---bi_encoder---------------------------')
print(bi_encoder1)
print(word_embedding_model1)
print()
#------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------
# text 추출된 문서파일들을 불러와서 datafframe 형태로 만듬
#-------------------------------------------------------------------------------------------------------
def load_docs():
    # 문서 추출된 TEXT들을 dataframe 형태로 만듬.
    OUT_FOLDER = '../../../data11/mpower_doc/out/' # 추출된 TEXT 파일들이 있는 루트폴더

    # OUT_FOLDER에 모든 파일 경로를 얻어옴.
    file_paths = getListOfFiles(OUT_FOLDER)
    assert len(file_paths) > 0 # files가 0이면 assert 발생

    print('*file_count: {}, file_list:{}'.format(len(file_paths), file_paths[0:5]))
    print()
    
    contexts = []
    titles = []
    contextids = []

    # TEXT 추출된 파일들을 읽어오면서 제목(title), 내용(contexts) 등을 저장해 둠.
    contextid = 1000
    for idx, file_path in enumerate(tqdm(file_paths)):
        if '.ipynb_checkpoints' not in file_path:
            sentences = []
            with open(file_path, 'r', encoding='utf-8') as f:
                data = f.read()

                #.PAGE:1 패턴을 가지는 문장은 제거함.
                pattern = r"\.\.PAGE:\d+\s?"
                data = clean_text(text=data, pattern=pattern)

                file_name = os.path.basename(file_path)  # 파일명만 뽑아냄

                #  filename = 5.보안사업부 사업계획.hwp.txt 이면 뒤에 hwp.txt는 제거하고 '5.보안사업부 사업계획' 문자열만 title로 저장함.
                file_name = remove_reverse(file_name, '.')# 5.보안사업부 사업계획.hwp 출력됨
                file_name = remove_reverse(file_name, '.')# 5.보안사업부 사업계획 출력됨

                contextid += 1
                contexts.append(data)     # 파일 내용 저장 
                titles.append(file_name)  # 파일명을 제목으로 저장(추후 쿼리할 문장이 됨)
                contextids.append(contextid) # contextid 저장 

    # 데이터 프레임으로 만듬.
    df_contexts = pd.DataFrame((zip(contexts, contextids)), columns = ['context','contextid'])
    df_questions = pd.DataFrame((zip(titles, contextids)), columns = ['question','contextid'])

    print(f'*len(contexts): {len(contexts)}')
    print()
    
    return df_contexts, df_questions

#-------------------------------------------------------------------------------------------------------
# 3. 슬라이딩 윈도우 혹은 문장 분리  
# 1) 슬라이딩 윈도우 : 문장(문서)들을 chunk(청크: 큰 덩어리)로 분리, 다시 분리된 chunks를 kss로 문장 분리해서 sentences 만듬, 이후 chunks와 sentences를 doc_sentences에 담음
#    최대 512 단위로 서로 겹치게 청크 단위로 분리함.
# 2) 문장 분리 : kss와 \n(줄바꿈)으로 문장을 분리함.
#-------------------------------------------------------------------------------------------------------
def get_sentences(df_contexts, df_questions):

    contexts = df_contexts['context'].values.tolist()
    start = time.time()


    doc_sentences = []
    tokenizer = word_embedding_model1.tokenizer

    # 슬라이딩 윈도우 처리 후 chunks 리스트 만들고, 다시 chunks를 kss로 문장 분리해서, 최종 chunks와 sentences를 doc_sentences에 담음
    if IS_SLIDING_WINDOW == True:
        for idx, context in enumerate(tqdm(contexts)):

            clean_context = clean_text(context)  # 전처리 : (한글, 숫자, 영문, (), {}, [], %, ,,.,",')  등을 제외한 특수문자 제거

            pattern = r'^\d+(\.\d+)*'  # 문장 맨앞에 '4.1.2.3' 패턴 제거,  r'^\d+(\.\d+)*\s+' # 문장 맨앞에 '4.1.2.3띄어쓰기' 있는 패턴 제거
            clean_context = clean_text(text=clean_context, pattern=pattern)

            pattern = r'^\d+\.'  # 문장 맨 앞에 '4.' 패턴 제거
            clean_context = clean_text(text=clean_context, pattern=pattern)

            pattern = r'^\d+\)'  # 문장 맨 앞에 '4)' 패턴 제거
            clean_context = clean_text(text=clean_context, pattern=pattern)


            #chunks = sliding_window_tokenizer(tokenizer = tokenizer, paragraph=clean_context, window_size=WINDOW_SIZE, sliding_size=SLIDING_SIZE)

            # 청크 클러스터링만 수행함
            chunks = get_text_chunks(tokenizer = tokenizer, paragraph=clean_context, chunk_token_size=WINDOW_SIZE)
            doc_sentences.append(chunks)

            #sentences = split_sentences1(paragraphs=chunks, remove_line=False, remove_sentence_len=remove_sentence_len, sentences_split_num=10000, paragraphs_num=10000000, debug=False)

            # chunks 1차원 리스트[A,B,C]와 sentences 2차원 리스트[[a,b],[b,c],[d,e]] 를 합쳐서, doc_sentencs[A,a,b,B,b,c,C,d,e] 에 담음.
            #arr = []
            #[arr.extend([chunks[i], *sentences[i]]) for i in range(len(chunks))]

            # doc_sentences 리스트에 추가 
            #doc_sentences.append(arr)

    # 문장 분리해서 doc_sentences에 담음.
    else:
        doc_sentences = split_sentences1(paragraphs=contexts, 
                                        remove_line=False, 
                                        remove_sentence_len=remove_sentence_len, 
                                        remove_duplication=remove_duplication, 
                                        check_en_ko=False, # 한국어 혹은 영어문장이외 제거하면, 즉 true 지정하면 1% 성능 저하됨
                                        sentences_split_num=10000, paragraphs_num=10000000, showprogressbar=True, debug=False)

    logger.info(f'*문장처리=>len:{len(doc_sentences[0])}, time:{time.time()-start:.4f}')
    
    len_list = []
    for i, doc_sentence in enumerate(doc_sentences):
        doc_sentence_len = len(doc_sentence)
        if i < 301:
            print(f'[{i}] {doc_sentence_len}/{df_questions["question"][i]}')
        len_list.append(doc_sentence_len)

    logger.info(f'*문장 길이=>평균:{sum(len_list) / len(len_list)} / MAX: {max(len_list)} / MIN: {min(len_list)}\r\n')
    
    return doc_sentences


#---------------------------------------------------------------------------
# 임베딩 처리 함수 
# -in : paragrphs 문단 리스트
#---------------------------------------------------------------------------
# 조건에 맞게 임베딩 처리하는 함수 
def embedding(paragrphs:list):
    if IS_ONNX_MODEL == True:
        embeddings = onnx_embed_text(model=onnx_model, tokenizer=onnx_tokenizer, paragraphs=paragrphs, token_embeddings=False).astype(FLOAT_TYPE)  
    else:
        # 한 문단에 대한 40개 문장 배열들을 한꺼번에 임베딩 처리함
        embeddings = embed_text(model=bi_encoder1, paragraphs=paragrphs, return_tensor=False).astype(FLOAT_TYPE)  
    
    return embeddings

#---------------------------------------------------------------------------
# ES 인덱스 생성
# -in : es : ElasticSearch 객체.
# -in : create : 기존에 동일한 인덱스는 삭제하고 다시 생성.
#---------------------------------------------------------------------------
def create_index(es, create:bool = True):
    
    if create == True:
        es.indices.delete(index=INDEX_NAME, ignore=[404])
        count = 0
        
        # 인덱스 생성
        with open(INDEX_FILE) as index_file:
            source = index_file.read().strip()
            count += 1
            print(f'{count}:{source}') # 인덱스 구조 출력
            es.indices.create(index=INDEX_NAME, body=source)
            
#---------------------------------------------------------------------------
# 인덱스 batch 처리
# - in: ES 객체
# - in: docs=인덱스 처리할 data
# - in: vector_len=한문서에 인덱싱할 벡터수=클러스터링수와 동일(기본=10개)
# - in: dim_size=벡터 차원(기본=128)
#---------------------------------------------------------------------------
def index_batch(es, docs, vector_len:int=10, dim_size:int=128):
        
    requests = []
    
    for i, doc in enumerate(tqdm(docs)):
        rfile_name = doc['rfile_name']
        rfile_text = doc['rfile_text']
        dense_vectors = doc['dense_vectors']
        
        #--------------------------------------------------------------------
        # ES에 문단 인덱싱 처리
        request = {}  #dict 정의
        request["rfile_name"] = rfile_name       # 제목               
        request["rfile_text"] = rfile_text   # 문장
        
        request["_op_type"] = "index"        
        request["_index"] = INDEX_NAME
        
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
    
#-------------------------------------------------------------------------------------------------------
#문단에 문장들의 임베딩을 구하여 각각 클러스터링 처리함.
#-------------------------------------------------------------------------------------------------------
def index_data(es, df_contexts, df_questions, doc_sentences:list):
    #클러스터링 계수는 문단의 계수보다는 커야 함. 
    #assert num_clusters <= len(doc_sentences), f"num_clusters:{num_clusters} > len(doc_sentences):{len(doc_sentences)}"
    #-------------------------------------------------------------
    # 각 문단의 문장들에 벡터를 구하고 리스트에 저장해 둠.
    start = time.time()
    cluster_list = []

    rfile_names = df_questions['contextid'].values.tolist()
    rfile_texts = df_questions['question'].values.tolist()

    docs = []
    count = 0
    for i, sentences in enumerate(tqdm(doc_sentences)):
        embeddings = embedding(sentences)
        if i < 3:
            print(f'[{i}] sentences---------------------------EMBEDDING_METHOD={EMBEDDING_METHOD}')
            if len(sentences) > 50:
                print(sentences[:50])
            else:
                print(sentences)
                
            print(f'embeddings.shape: {embeddings.shape}')
            print()

        # 0=문장클러스터링 임베딩
        if EMBEDDING_METHOD == 0:
            if CLUSTRING_MODE == "kmeans":
                # 각 문단에 분할한 문장들의 임베딩 값을 입력해서 클러스터링 하고 평균값을 구함.
                #emb1 = clustering_embedding(embeddings = embeddings, outmode=outmode, num_clusters= 50, seed=seed)
                emb = clustering_embedding(embeddings = embeddings, outmode=outmode, num_clusters= num_clusters, seed=seed).astype(FLOAT_TYPE) 
            else:
                emb = kmedoids_clustering_embedding(embeddings = embeddings, outmode=outmode, num_clusters= num_clusters, seed=seed).astype(FLOAT_TYPE) 
        # 1= 문장평균임베딩
        elif EMBEDDING_METHOD == 1:
            # 문장들에 대해 임베딩 값을 구하고 평균 구함.
            arr = np.array(embeddings).astype(FLOAT_TYPE)
            emb = arr.mean(axis=0).reshape(1,-1) #(128,) 배열을 (1,128) 형태로 만들기 위해 reshape 해줌
        # 2=문장임베딩
        else:
            emb = embeddings

        #emb.astype('float16')
        if i < 3:
            print(f'emb.shape: {emb.shape}')
            print(f'emb:{emb[0]}')
            print()

        #--------------------------------------------------- 
        count += 1
        doc = {} #dict 선언

        doc['rfile_name'] = rfile_names[i]      # contextid 담음
        doc['rfile_text'] = rfile_texts[i]      # text 담음.
        doc['dense_vectors'] = emb

        docs.append(doc)
        #---------------------------------------------------    

        if count % BATCH_SIZE == 0:
            index_batch(es, docs, vector_len=num_clusters, dim_size=dimension)
            docs = []
            print("Indexed {} documents.".format(count))
            print()

    if docs:
        index_batch(es, docs, vector_len=num_clusters, dim_size=dimension)
        print("Indexed {} documents.".format(count))   
        print()

    es.indices.refresh(index=INDEX_NAME)

    logger.info(f'*인덱싱 시간 : {time.time()-start:.4f}\n')
    print()
    
#======================================================================================
# ElasticSearch(이하:ES) 데이터 인텍싱
#======================================================================================   
def main():
    # 1. 추출된 문서들 불러와서 df로 만듬
    df_contexts, df_questions = load_docs()
    
    # 2. 문장 추출
    doc_sentences = get_sentences(df_contexts, df_questions)
    
    # 3. elasticsearch 접속
    es = Elasticsearch("http://192.168.0.27:9200/")
    print(es.info())

    # 4. 인덱스 생성
    create_index(es, True)

    # 5. index 처리
    index_data(es, df_contexts, df_questions, doc_sentences)

if __name__ == '__main__':
    main()
    