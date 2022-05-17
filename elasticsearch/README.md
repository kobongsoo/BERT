## ElasticSearch로 임베딩 벡터(Embedding Vector)를 이용한 문장 유사도 검색 구현하기
- 엘라스틱서치와 SentenceBert를 이용하여, 문장들의 임베딩 벡터들을 구하고, 이 벡터들의 코사인유사도를 측정하여, 의미가 유사한 문장들을 검색한다.

### 1. 엘라스틱서치에 접속하기
- 엘라스틱서치 서버 접속 모듈 설치
```
# elasticsearch 서버 접속 모듈 설치
# !pip install elasticsearch
```
- 엘라스틱서치 서버 접속(**기본포트 : 9200**)
```
# elastic 서버 접속 
#es = Elasticsearch("https://XXX.XXX.XXX.XXX:9200/", verify_certs=False)
es = Elasticsearch("http://XXX.XXX.XXX.XXX:9200/")
# 접속 서버 정보 확인
es.info()
```
