# FastAPI
FastAPI는 현대적이고, 빠르며(고성능), 파이썬 표준 타입 힌트에 기초한 Python3.6+의 API를 빌드하기 위한 웹 프레임워크입니다.
<br>**ASGI(Ansynchronous Server Gateway Interface: 비동기 서버 게이트웨이 인터페이스)** 지원
<br>출처 : https://fastapi.tiangolo.com/ko/

- CGI : Common Gateway Interface , 서버<->클라이언트간 요청을 처리하는 공통의 표준 인터페이스, 단점은 프로세스를 다시 실행해야 함.
- WCGI : Web Server Gateway Interface, CGI 단점을 보안하기 위해 요청을 Callable object, 함수, 객체등으로 처리함, 단 비동기 처리에 단점이 있음.
- ASGI : Asynchronous Server Gateway Interface, 비동기식으로 요청을 처리하는 CGI, 대규모 웹 에플리케이션 개발에 적함

<br>

설치

```
pip install fastapi[all]
```

실행
- test : python.py 파일명
- app : .py 코드에 app = FastAPI() 인스턴스 명
- --limit-concurrency: 연결 최대 허용 수
<br>uvicorn 옵션들 : https://www.uvicorn.org/deployment/
```
uvicorn test:app --reload --host=0.0.0.0 --port=8000 --limit-concurrency=200
```

### aync(비동기)
- FastAPI는 requests와 같은 non async 라이브러리도 쓰레드풀을 이용하여 async 하게 실행시켜준다.
- def로 선언된 경우, 별도의 쓰레드 풀로 non-async를 async 하게 처리한다.
<br> 출처 : https://keyhyuk-kim.medium.com/fastapi-%EB%8A%94-non-async-%ED%95%A8%EC%88%98-%EB%B9%84%EB%8F%99%EA%B8%B0%EB%A1%9C-%EC%B2%98%EB%A6%AC%ED%95%98%EA%B8%B0-8e3345a69517

```
# Non-block
@router.get("/sync/sync")
def sync():
  time.sleep(10)
  logger.info('running...')
```
- 하지만 스코프가 async로 선언되어있는 경우는 non-async 함수를 이벤트루프에서 처리하여 **서버가 blocking** 된다.
<br>이벤트 루프를 block 시키지 않게하려면 아래와 같이 호출하려는 non-async 함수를 **run_in_threadpool** 을 사용해 명시적으로 처리하거나,
<br> worker옵션을 통해서 non-async 를 async하게 처리할 수 있다. **worker옵션은, 생성하는 worker수만큼 만 비동기가 보장된다**.

```
# Non-Block
@router.get("/async/sync")
async def async_with_sync():
  from fastapi.concurrency import run_in_threadpool
  await run_in_threadpool(sleep, 10)
  logger.info('running...')
```
```
uvicorn src.app:app --port 8000 --workers 3
```


FastAPI 테스트 예제

|소스명|설명|기타|
|:-----------------|:-----------------------------------------------------------|:---------------------|
|[get_test](https://github.com/kobongsoo/BERT/blob/master/FastAPI/get_test.py)|GET RestAPI 예제||
|[post_test](https://github.com/kobongsoo/BERT/blob/master/FastAPI/post_test.py)| POST RestAPI 예제||
|[model_test](https://github.com/kobongsoo/BERT/blob/master/FastAPI/model_test.ipynb)|ES 검색 테스트 예제||
|[yaml_test](https://github.com/kobongsoo/BERT/blob/master/FastAPI/yaml_test.py)|yaml 파일 로딩 예제||
|[security_test](https://github.com/kobongsoo/BERT/blob/master/FastAPI/security_test.py)|password flow(암호 로그인) 테스트 예제||
|[jwt_test](https://github.com/kobongsoo/BERT/blob/master/FastAPI/jwt_test.py)|json web token 으로 로그인하는 테스트 예제||

임베딩 예제
|소스명|설명|기타|
|:-----------------|:-----------------------------------------------------------|:---------------------|
|[embedserver](https://github.com/kobongsoo/BERT/blob/master/FastAPI/embedserver.py)| **ES 연동한 문서클러스터링 임베딩 및 검색 예제**|설정값(환경에 맞게 수정 필요): data/settings.yaml<br>sh 실행스크립트: embedserver.sh(python으로 실행함)|
|[embedserver2](https://github.com/kobongsoo/BERT/blob/master/FastAPI/embedserver2.py)| **ES 연동한 문서클러스터링 임베딩 및 검색 예제2**|설정값(환경에 맞게 수정 필요): data/settings.yaml<br>sh 실행스크립트: embedserver2.sh(**uvicorn 으로 실행함-좀더 옵션을 많이 설정할수 있음**)|
|[embedserver_test](https://github.com/kobongsoo/BERT/blob/master/FastAPI/embedserver_test.ipynb)| 위서버와 RESTFul API를 이용한 Client 검색 및 임베딩 예제|embedserver 실행 필요|




