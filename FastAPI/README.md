# FastAPI
FastAPI는 현대적이고, 빠르며(고성능), 파이썬 표준 타입 힌트에 기초한 Python3.6+의 API를 빌드하기 위한 웹 프레임워크입니다.
<br>출처 : https://fastapi.tiangolo.com/ko/


설치

```
pip install fastapi[all]
```

실행
- test : python.py 파일명
- app : .py 코드에 app = FastAPI() 인스턴스 명
```
uvicorn test:app --reload --host=0.0.0.0 --port=8000
```

예제

|소스명|설명|기타|
|:-----------------|:-----------------------------------------------------------|:---------------------|
|[get_test](https://github.com/kobongsoo/BERT/blob/master/FastAPI/get_test.py)|GET RestAPI 예제||
|[post_test](https://github.com/kobongsoo/BERT/blob/master/FastAPI/post_test.py)| POST RestAPI 예제||
|[model_test](https://github.com/kobongsoo/BERT/blob/master/FastAPI/model_test.ipynb)|ES 검색 테스트 예제||
|[yaml_test](https://github.com/kobongsoo/BERT/blob/master/FastAPI/yaml_test.py)|yaml 파일 로딩 예제||
|[model](https://github.com/kobongsoo/BERT/blob/master/FastAPI/model.py)| **ES 연동한 문서클러스터링 임베딩 및 검색 예제**|data/settings.yaml에 설정값이 있음|

