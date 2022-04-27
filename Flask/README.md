## FLASK
- 파이썬으로 작성된 마이크로 웹 프레임워크의 하나로, Werkzeug 툴킷과 Jinja2 템플릿 엔진에 기반을 둔다.
- Document는 [여기](https://flask-docs-kr.readthedocs.io/ko/latest/quickstart.html) 참조

- 설치하기
```
pip install Flask
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
### 예제

|소스명|설명|기타|
|:-----------------|:-----------------------------------------------------------|:---------------------|
|[webservice.py](https://github.com/kobongsoo/BERT/blob/master/Flask/webservice.py)|Flask 와 BERT 모델 추론 함수(model.py), UI html( 연동||
|[run.py](https://github.com/kobongsoo/BERT/blob/master/Flask/run.py)| Flask 웹서비스 실행 |host='0.0.0.0' 하면, 웹에서 해당 ip로 접속가능|
|[model.py](https://github.com/kobongsoo/BERT/blob/master/Flask/model.py)| BERT 모델 추론 하고,그 결과를 리턴 함 |BERT 모델 로딩/추론 처리함|
|[classification.html](https://github.com/kobongsoo/BERT/blob/master/Flask/classification.html)| webservice.py에서 호출 하는 분류 UI 웹페이지 ||
|[sb.html](https://github.com/kobongsoo/BERT/blob/master/Flask/sb.html)| webservice.py에서 호출 하는 쿼리와 분류문장 유사도 측정 UI 웹페이지 ||
|[summarizer.html](https://github.com/kobongsoo/BERT/blob/master/Flask/summarizer.html)| webservice.py에서 호출 하는 추출 요약문 생성 UI 웹페이지 ||
