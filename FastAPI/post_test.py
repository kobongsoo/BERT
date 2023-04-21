#----------------------------------------------------------------------
# #Request body(요청본문:POST) 예제
# - 설치 :pip install fastapi[all]
# - python 업데이트(옵션)  : conda install -c anaconda python=3.10 (3.10이상 필요)
# - 실행 : uvicorn test:app --reload --host=0.0.0.0 --port=8000
# - 출처 : https://fastapi.tiangolo.com/ko/tutorial/body/
#----------------------------------------------------------------------
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name:str                     #필수=무조건입력
    description:Union[str, None]=None  #선택=입력안해도 됨.안하면=None
    price:float = 0              #기본값=입력안해도 됨. 안하면 기본값
    tax:float = 0.1              #기본값

app=FastAPI() # fastapi 인스턴스 생성.

@app.post("/items/{item_id}") # 경로동작 데코레이터 작성
async def create_item(item_id:int, item:Item, q:Union[str,None]=None): #경로동작 함수 작성
    result = {"item_id": item_id, **item.dict()}

    if q:
        result.update({"q":q})

    return result
