from typing import List, Optional
from fastapi import FastAPI, Query, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(item_id:int=Path(...,ge=0,le=100), 
                     q:Optional[List[str]] = Query(["test1","test2","exe1"], deprecated=True)
                    ):
    
    query_items = {"item_id": item_id, "q": q}
    return query_items

    