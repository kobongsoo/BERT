## ElasticSearch로 임베딩 벡터(Embedding Vector)를 이용한 문장 유사도 검색 구현하기
- 엘라스틱서치와 **SentenceBert**를 이용하여, 문장들의 임베딩 벡터들을 구하고, 이 벡터들의 코사인유사도를 측정하여, 의미가 유사한 문장들을 검색한다. (엘라스틱서치 서버 구축 방법은 여기서 설명 하지 않음)
- ElasticSearch 7.3.0 버전부터는 cosine similarity 검색을 지원한다.
- ElasticSearch에 index 파일은 **/data/index.json** ,데이터 파일은 **/data/KorQuAD_v1.0_train_convert.json** 참조

### 1. SentenceBert 정의
- sentenceTransformers 라이브러리 설치
```
!pip install -U sentence-transformers
```
- embeddding 벡터를 구할 SentenceBert 정의
```
import torch
from sentence_transformers import SentenceTransformer, util
device = torch.device('cpu')

# s-bert 모델 테스트
sbert_model_path = '../../model/sbert/sbert-ts2022-04-01-distiluse-7'

# cpu 모델로 실행할때는 device=cpu, 기본은 GPU임
embedder = SentenceTransformer(sbert_model_path, device=device)

text = '나는 오늘 밥을 먹는다.'
vectors = embedder.encode(text, convert_to_tensor=True)
vector_list = [vector.numpy().tolist() for vector in vectors]

print(f'vector_len:{len(vector_list)}')

```

### 2. 엘라스틱서치 서버에 접속하기
- 엘라스틱서치 서버 접속 모듈 설치
```
# elasticsearch 서버 접속 모듈 설치
# !pip install elasticsearch
```
- 엘라스틱서치 서버 접속(**기본포트 : 9200**)
```
from elasticsearch import Elasticsearch
from elasticsearch import helpers

# elastic 서버 접속 
#es = Elasticsearch("https://XXX.XXX.XXX.XXX:9200/", verify_certs=False)
es = Elasticsearch("http://XXX.XXX.XXX.XXX:9200/")
# 접속 서버 정보 확인
es.info()
```
### 3. 인덱스 생성
- index.json 파일에 정의된 mapping 구조를 불러와서 ES 인덱스를 생성한다.
```
INDEX_NAME = 'korquad'    # ES에 생성할 인덱스명
INDEX_FILE = './data/index.json' # 생성할 인덱스 구조

# 인덱스 생성
with open(INDEX_FILE) as index_file:
        source = index_file.read().strip()     
        es.indices.create(index=INDEX_NAME, body=source)
```
### 4. 인덱스에 데이터 추가
- KorQuAD_v1.0_train_convert.json 파일에 title과 paragraph(문장)을 불러와서, SentenceBert를 통해 embedding 벡터를 만듬.
- 만든 embedding 벡터와 title, paragraph등을 추가하여 ES 인덱스에 데이터 추가함.

```
from elasticsearch.helpers import bulk

def index_batch(docs):
   
    titles = [doc["title"] for doc in docs]
    title_vectors = embed_text(titles)
    
    # 문장이 길면 분할해서 embedding을 구해야 하는데, 여기서는 분할하지 않고 embedding을 구함
    paragraphs = [doc["paragraph"] for doc in docs]
    paragraph_vectors = embed_text(paragraphs)
    
    requests = []
    for i, doc in enumerate(tqdm(docs)):
        request = doc
        
        request["_op_type"] = "index"
        request["_index"] = INDEX_NAME
        
        request["title_vector"] = title_vectors[i]
        request["paragraph_vector"] = paragraph_vectors[i]
        
        requests.append(request)
        
    # batch 단위로 한꺼번에 es에 데이터 insert 시킴     
    bulk(es, requests)
```
### 5. 검색하기
- ES 인덱스에 추가한 문자들을 코사인유사도로 검색 함.(**cosineSimilarity** 스크립트 이용)
```
def handle_query():
    
    query = input("검색어 입력: ")
    
    start_embedding_time = time.time()
    query_vector = embed_text([query])[0]
    end_embedding_time = time.time() - start_embedding_time
    
    # 쿼리 구성
    script_query = {
        "script_score":{
            "query":{
                "match_all": {}},
            "script":{
                "source": "cosineSimilarity(params.query_vector, doc['paragraph_vector']) + 1.0",  # 뒤에 1.0 은 코사인유사도 측정된 값 + 1.0을 더해준 출력이 나옴
                "params": {"query_vector": query_vector}
            }
        }
    }
    
     # 실제 ES로 검색 쿼리 날림
    start_search_time = time.time()
    response = es.search(
        index=INDEX_NAME,
        body={
            "size": SEARCH_SIZE,
            "query": script_query,
            "_source":{"includes": ["title", "paragraph"]}
        }
    )
    end_search_time = time.time() - start_search_time
    
    print("{} total hits.".format(response["hits"]["total"]["value"])) 
    print("embedding time: {:.2f} ms".format(end_embedding_time * 1000)) 
    print("search time: {:.2f} ms".format(end_search_time * 1000)) 
    print('\n')
    
    # 쿼리 응답 결과값에서 _id, _score, _source 등을 뽑아냄
    # print(response)
    
    for hit in response["hits"]["hits"]: 
        
        print("index:{}, type:{}".format(hit["_index"], hit["_type"]))
        print("id: {}, score: {}".format(hit["_id"], hit["_score"])) 
        
        print(f'[제목] {hit["_source"]["title"]}')
        
        print('[내용]')
        print(hit["_source"]["paragraph"]) 
    
```
