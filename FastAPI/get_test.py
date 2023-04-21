#----------------------------------------------------------------------
# 매개변수(GET) 예제
# - 설치 :pip install fastapi[all]
# - python 업데이트(옵션) : conda install -c anaconda python=3.10 (3.10이상 필요)
# - 실행 : uvicorn test:app --reload --host=0.0.0.0 --port=8000
# - POST 확인 : IP/docs
# - 출처 : https://fastapi.tiangolo.com/ko/
#----------------------------------------------------------------------
from enum import Enum
from typing import Union

from fastapi import Query
from typing_extensions import Annotated
from fastapi import Cookie
from fastapi import Form

from fastapi import FastAPI # FastAPI 임포트.

class ModelName(str, Enum):
	alexnet = "alexnet"
	resnet = "resnet"
	lenet = "lenet"

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

app=FastAPI() # app 인스턴스 생성

@app.get("/")  # 경로 동작 데코레이터 작성
async def root(): # 경로 동작 함수 작성
	return {"msg": "Hello World"}

@app.get("/users/me")
async def read_user_me():
	return {"user_id": "me->current id"}

@app.get("/users/{user_id}")
async def read_user(user_id:str):
	return {"user_id": user_id}

# Enum 설정
@app.get("/models/{model_name}")
async def get_models(model_name: ModelName):
	if model_name.value == "lenet":
		return {"model_name": model_name, "msg": 3} 
	elif model_name == "alexnet":
		return {"model_name": model_name, "msg": 1} 
	elif model_name == "resnet":
		return {"model_name": model_name, "msg": 2} 

	return {"model_name": model_name, "msg": "Not Enum"} 

# 경로매개변수 : 파일경로 설정
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
	return {"file_path": file_path}

# 쿼리 매개변수 설정
#-> ?뒤에 &로 구분하여 쿼리=값 쌍으로 함..
# http://127.0.0.1:8000/items/?skip=0&limit=10
@app.get("/items/")
async def read_item(skip:int=0, limit:int=10):
	return fake_items_db[skip:skip+limit]

# 쿼리매개변수들은 Union 정의해서 선태적, = 이용해서 기본값 지정 가능
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short:bool=False):
	item={"item_id":item_id}
	if q:
		item.update({"q":q})

	if short == True:
		item.update({"short": "short is true"})

	return item

# 경로 매개변수: 여러개 지정할수 있음
# http://127.0.0.1:8000/users/test/items/god?q=111&short=1
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id:str, item_id:str, q:Union[str, None]=None, short:bool=False):
	item={"user_id": user_id, "item_id": item_id}
	if q:
		item.update({"q": q})

	if short == True:
		item.update({"short": "short is True"})

	return item

# 쿼리 매개변수: 길이 제한하기(q입력값=3이상 10이하)
# - http://127.0.0.1:8000/max/?q=fffffffffffffffffffffffffffff
# - Annotated 이용
@app.get("/max/")
async def read_items_max(q: Annotated[Union[str, None], Query(min_length=3, max_length=10)]=None):
	results = {"items": [{"item_id": "Foo"},{"item_id": "Bar"}]}

	if q:
		results.update({"query":q})

	return results

# 쿼리 매개변수 : 줄임표(...) 혹은 Required 로 필수 쿼리매개변수 지정
@app.get("/max1/")
async def read_items_max(q: Annotated[str, Query(min_length=3, max_length=10)]=...):
	results = {"items": [{"item_id": "Foo"},{"item_id": "Bar"}]}

	if q:
		results.update({"query":q})

	return results

# 쿼리 매개변수: 키는1개에 다중값 지정.
# - http://127.0.0.1:8000/query/?q=1&q=2&q=5
# - {"query": ["1", "2", "5"]}
#
@app.get("/query/")
async def read_items(q: Annotated[list, Query()]=[]):
	query_items = {"query": q}
	return query_items

from typing import Union

from fastapi import FastAPI, Path, Query

app = FastAPI()

# 경로매개변수:
@app.get("/items1/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: Union[str, None] = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

#Form 매개변수 
@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}