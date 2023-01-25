## ElasticSearch로 임베딩 벡터(Embedding Vector)를 이용한 문장 유사도 검색 구현하기

- 예시) “AI 관련 자료들” 검색 시, 키워드  방식으로는 검색되지 않는 
  <br>“Artificial intelligence”, “인공지능”, “머신러닝”, “딥러닝” 등의 내용도 검색 된다.

![image](https://user-images.githubusercontent.com/93692701/171549420-e9bdeaff-c66f-4bd1-9af0-5bbcd378b05e.png)


- 엘라스틱서치와 **SentenceBert**를 이용하여, 문장들의 임베딩 벡터들을 구하고, 이 벡터들의 코사인유사도를 측정하여, 의미가 유사한 문장들을 검색한다. (엘라스틱서치에 대한 자세한 내용은 [여기](https://esbook.kimjmin.net/) 참조)
- **ElasticSearch 7.3.0 버전부터는 cosine similarity 검색을 지원**한다.
  <br> ElasticSearch는 기본 9200 포트, Kibana(시각화 도구)는 5601 포트를 각각 사용한다
- **ElasticSearch 7.0** 부터는 **doc_type 개념이 사라지고, _doc 으로 접근**해야 함.
- 예제와 관련된 ElasticSearch에 Index 파일은 **/data/index.json** ,데이터 파일은 **/data/KorQuAD_v1.0_train_convert.json** 참조
- ElasticSearch에 Index(indices), Type, Filed, Document 등은 아래 처럼 관계형 DataBase 연관된다.(아래그림 참조)
- 아래는 [ElasticSearch Python Client](https://elasticsearch-py.readthedocs.io/en/v8.3.1/)를 이용한 예제임
<br> [ElasticSearch PHP Client](https://github.com/elastic/elasticsearch-php)를 이용할수도 있음.

![image](https://user-images.githubusercontent.com/93692701/168928961-8b426b51-d937-49a9-8eed-982f2be740bb.png)

|RDBMS(관계형DB)           | ElasticSearch               | 설명                          |
|:-------------------------|:----------------------------|:------------------------------|
|DataBase                  |Index(Indices)               |데이터를 모아놓은 집합          |
|Table                     |Type                         |테이블 (7.3.0 부터는 _doc 으로만 해야 함)|  
|Row                       |Document                     |단일 데이터 단위                |  
|Column                    |Field                        |필드명                          |  
|Primary Key               |_id                          |키                              |  
|Schema                    |Mapping                      | Indices의 Field 및 Field 타입을 미리 정의해 놓으면,해당 매핑에 맞추어 데이터가 입력됨                               |  
|Phyical Partition         |Shard                        |Indices가 분리되어 분산 저장되는 단위|  
|Logical Partition         |Route                        |                               |  
|Relational                |Parent/Child, Nested         |                               |  

출처: https://www.slideshare.net/deview/2d1elasticsearch

|소스     |내용 | 기타 |
|:--------|:---------------------------------|:---------|
|[elasticsearch_vector_search_test](https://github.com/kobongsoo/BERT/blob/master/elasticsearch/elasticsearch_vector_search_test.ipynb)|ElasticSearch+S-BERT를 이용한 임베딩 테스트 예제||
|[elasticsearch_vector_search_test2](https://github.com/kobongsoo/BERT/blob/master/elasticsearch/elasticsearch_vector_search_test2.ipynb)|ElasticSearch+ONNX-S-BERT를 이용한 임베딩 테스트 예제||
|[es_summarize_vector](https://github.com/kobongsoo/BERT/blob/master/elasticsearch/es_summarize_vector.ipynb)|ElasticSearch+S-BERT를 이용한 임베딩 테스트 예제+**추출요약**||
|[elasticsearch_search_test](https://github.com/kobongsoo/BERT/blob/master/elasticsearch/elasticsearch_search_test.ipynb)|ElasticSearch 접속/데이터 추가,삭제/인덱스 생성,삭제 등 관련 테스트 예제||
|[elasticsearch_analyze_test](https://github.com/kobongsoo/BERT/blob/master/elasticsearch/elasticsearch_analyze_test.ipynb)|ElasticSearch 검색/분석 관련  테스트 예제||

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
### 4. 인덱스에 도큐먼트(데이터) 추가
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
- ES 인덱스에 추가한 문장들에 대해, 쿼리와 문장들간의 코사인 유사도를 구하고, 가장 유사한 문장들을 출력함.(**cosineSimilarity** 스크립트 이용)
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

### 예제1
- ES 서버와 별도로 Flask 서버를 돌리고, **CURL 혹은 [curl_test.ipynb](https://github.com/kobongsoo/BERT/blob/master/Flask/curl_test.ipynb) pythoh을 이용하여 검색**하는 예시
- ES 서버에는 [es_summarize_vector](https://github.com/kobongsoo/BERT/blob/master/elasticsearch/es_summarize_vector.ipynb)코드를 이용하여 문서요약문들이 미리 인덱싱 되어 있어야 한다.
- [server.py](https://github.com/kobongsoo/BERT/blob/master/Flask/server.py) :문장 임베딩, 추출요약 후 임베딩, ElasticSearch와 연계한 검색을 수행하는 Server
```
서버 실행
python server.py
```
- [curl_test.ipynb](https://github.com/kobongsoo/BERT/blob/master/Flask/curl_test.ipynb) : restAPI를 이용하여 server에 접속후 임베딩, 추출요약, 검색등을 수행하는 client
- curl 이용시 아래 예시 참조(**text에는 한글인 경우에는 인코딩된 값을 넣어야함**)
```
# 문장 임베딩 ( '안녕하세요' 임베딩 값 추출)
# curl -d "{""text"":""%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94""}" -H "Content-Type: application/json" -X POST http://127.0.0.1:9999/embed

# 문장 요약후 임베딩
# => curl -d "{""text"":""%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94""}" -H "Content-Type: application/json" -X POST http://127.0.0.1:9999/summarize?min_length=10&num_sentence=3

# ES vector 검색
# => curl -d "{""text"":""%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94""}" -H "Content-Type: application/json" -X POST http://127.0.0.1:9999/search?eshost='http://192
.168.0.27:9000'&index='korquad-klue-sbert-v1.0-idx1'&size=3
```

- 테스트시 **doc(문서내용들) 요약한 후 (요약 문장들의 평균값으로 임베딩 + 제목 임베딩)/2**을 하는 방식이 가장 좋았음. 
- **단 문서 요약은 CPU 환경에서 테스트시 약 400 문서처리시 1시간 정도, 오래 걸리므로 GPU 환경도 고려해야 함**(korquad 1420 요약 처리.임베딩추출.ES 인덱싱까지 총 3.5H 걸림) 
- 최종적으로는 **doc2vec 을 어떻게 할 것인가가 핵심**임(요약해서 평균, 모든 문장 평균, 타이틀만 이용 등...)

### 예제2
- ES 서버와 별도로 Flask 서버를 돌리고, **웹에서 Flask서버로 접속하여 ES 서버와 연동해서 검색**하는 예시임.
- ES 서버에는 [es_summarize_vector](https://github.com/kobongsoo/BERT/blob/master/elasticsearch/es_summarize_vector.ipynb) 혹은 [es_summarize_vector_ai_hub](https://github.com/kobongsoo/BERT/blob/master/elasticsearch/es_summarize_vector_ai_hub.ipynb)코드를 이용하여 문서요약문들이 미리 인덱싱 되어 있어야 한다.

- [server.py](https://github.com/kobongsoo/BERT/blob/master/Flask/server.py) :문장 임베딩, 추출요약 후 임베딩, ElasticSearch와 연계한 검색을 수행하는 Server
```
서버 실행
python server.py
```
![image](https://user-images.githubusercontent.com/93692701/213373591-5edb5005-cec7-4fe6-a8bd-6d9d21d8af1d.png)

- 임베딩 모델, 추출요약모델(기본:bongsoo/albert-small-kor-sbert-v1.1), cross-encoder 모델(기본:ongsoo/albert-small-kor-cross-encoder-v1)등을 인자로 넘겨 실행할수 있음.
```
python server.py -host=0.0.0.0 -port=9999 -embedder={embedder 모델 경로} -summarizer={summarizer 모델 경로} -crossencoder={crossencoder 모델 경로}
```

웹에서 검색 실행 
- [search.html](https://github.com/kobongsoo/BERT/blob/master/Flask/search.html)코드에서 서버ip와 es 인덱스, 검색 수 등을 아래처럼 변경해야 함.
```
// **엘라스틱서치 서버 정보를 추가해서 url 구성해야 함.
// =>esurl={elasticsearch 서버 url}&index={elasticserch 검색 index}&size={검색계수}
url: "/essearch?esurl=http://192.168.0.27:9200/&index=korquad-albert-small-kor-sbert-v1.1&size=5",
```
- 웹페이지 실행해서 url에  {서버 ip}/search 입력
- 검색어(예:대한민국) 입력하면 검색 결과 출력됨.

![image](https://user-images.githubusercontent.com/93692701/213374856-8669e92f-c5f9-4f7a-af90-5c4fe8ee8cb2.png)


## 기타

### 1. ElasticSearch 지원 함수 예제
- 생성/삭제/업데이트/쿼리 등의 ElastricSearch 함수들 정의(참고 : https://jvvp.tistory.com/1152)
- 해당 함수 구현 내용은 [elasticsearch_search_test](https://github.com/kobongsoo/BERT/blob/master/elasticsearch/elasticsearch_search_test.ipynb), [elasticsearch_analyze_test](https://github.com/kobongsoo/BERT/blob/master/elasticsearch/elasticsearch_analyze_test.ipynb) 참조

#### ElasticSearch 접속
```
es = Elasticsearch("http://XXX.XXX.XXX.XXX:9200/")
```
#### 인스 생성/삭제
```
## 인덱스 생성
def create_index(index, mapping=None):
    if not es.indices.exists(index=index):
        return es.indices.create(index=index ,body=mapping)

## 인덱스 자체 삭제
def delete_index(index):
    if es.indices.exists(index=index):
        return es.indices.delete(index=index)
```
#### 도큐먼트(데이터) 추가
```
def insert(index, doc_type, body):
    return es.index(index=index, doc_type=doc_type, body=body)
```

#### 도큐먼트 조회
```
def search(index, data=None):
    if data is None: #모든 데이터 조회
        data = {"match_all":{}}
    else:
        data = {"match": data}
        
    body = {"query": data}
    res = es.search(index=index, body=body)
    return res
```

#### 도큐먼트 삭제
```
## 인덱스 내의 데이터 삭제 => query 이용
def delete(index, data):
    if data is None:  # data가 없으면 모두 삭제
        data = {"match_all":{}}
    else:
        data = {"match": data}
        
    body = {"query": data}
    return es.delete_by_query(index=index, body=body)

## 인덱스 내의 데이터 삭제 => id 이용
def delete_by_id(index, id):
    return es.delete(index=index, id=id) 
```

#### 도큐먼트 업데이트
```
def update(index, id, doc, doc_type):
    
    body = {
        'doc': doc
    }
    
    res=es.update(index=index, id=id, body=body, doc_type=doc_type)
    return res
```

#### 분석(Analyze)
- nori_tokenizer는 7.x 부터 지원하는 한국어 tokenizer(Mecab:은전한닢)
```
# tokenzier 분석예 
body = {
    "tokenizer":"nori_tokenizer",
    "filter" : [
        "lowercase",
        "stop",
        "snowball"
    ],
    "text" : ["매일 비가 오네요"]
}
es.indices.analyze(body=body)
# es.indices.analyze(index=INDEX_NAME, body=body)
```
