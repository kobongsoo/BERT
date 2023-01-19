## FLASK
- 파이썬으로 작성된 마이크로 웹 프레임워크의 하나로, Werkzeug 툴킷과 Jinja2 템플릿 엔진에 기반을 둔다.
- Document는 [여기](https://flask-docs-kr.readthedocs.io/ko/latest/quickstart.html) 참조

- 설치하기
```
pip install Flask
pip install flask-cors  # flask Cross-Origin Resource Sharing( CORS는 시스템 수준에서 타 도메인 간 자원 호출을 승인하거나 차단하는 것을 결정하는 것)
pip install argparse    # arg 파싱 처리
```
- 실행하기
1. 아래처럼 webservice.py 파일 생성
```
from flask import Flask, request, jsonify, render_template
def get_web_service_app():
  app = Flask(__name__, template_folder='')
  
  @app.route('/')
  def hello_world():
    return 'Hello World!'
    
  retrun app  
```
2. run.py 파일 생성
```
from webservice import get_web_service_app
#from model import classification_model_eval, sbert_model_eval

app = get_web_service_app()
app.run(host='0.0.0.0', port=5000)
```
3. 실행하기
```
python run.py
* Running on http://127.0.0.1:5000/
```
4. 웹페이지에서 접속하기
 ```
http://ip:5000/  혹은 http://127.0.0.1:5000/ 접속하면, 'Hello World!' 가 찍힘
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
- ES 서버에는 [es_summarize_vector](https://github.com/kobongsoo/BERT/blob/master/elasticsearch/es_summarize_vector.ipynb)코드를 이용하여 문서요약문들이 미리 인덱싱 되어 있어야 한다.

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

### 예제3

|소스명|설명|기타|
|:-----------------|:-----------------------------------------------------------|:---------------------|
|[webservice.py](https://github.com/kobongsoo/BERT/blob/master/Flask/webservice.py)|Flask 와 BERT 모델 추론 함수(model.py), UI html 연동||
|[run.py](https://github.com/kobongsoo/BERT/blob/master/Flask/run.py)| Flask 웹서비스 실행 |**host='0.0.0.0'** 하면, 웹에서 해당 ip로 접속가능|
|[model.py](https://github.com/kobongsoo/BERT/blob/master/Flask/model.py)| BERT 모델 추론 하고,그 결과를 리턴 함 |BERT 모델 로딩/추론 처리함|
|[classification.html](https://github.com/kobongsoo/BERT/blob/master/Flask/classification.html)| webservice.py에서 호출 하는 분류 UI 웹페이지 |http://ip:port/sc 접속시 보여지는 UI|
|[sb.html](https://github.com/kobongsoo/BERT/blob/master/Flask/sb.html)| webservice.py에서 호출 하는 쿼리와 분류문장 유사도 측정 UI 웹페이지 |http://ip:port/sb 접속시 보여지는 UI|
|[summarizer.html](https://github.com/kobongsoo/BERT/blob/master/Flask/summarizer.html)| webservice.py에서 호출 하는 추출 요약문 생성 UI 웹페이지 |http://ip:port/summ 접속시 보여지는 UI|

#### http://ip:port/sb 접속 화면 예시
![image](https://user-images.githubusercontent.com/93692701/165464853-b4cdd6d1-48fd-46c7-b462-32874934823c.png)

