from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

data_list = []

@app.get("/text")
async def text(request: Request):
    return templates.TemplateResponse("text.html", {"request": request})

@app.get("/es/{esindex}/docs/answer")
async def search_documents(esindex:str, 
                     request: Request,
                     query: str = Query(..., min_length=1),
                     search_size: int = Query(..., gt=0)
                     ): 
    
    answer = f'답변 : {esindex}, size: {search_size}' 
    context = "문단 :" + query
    return templates.TemplateResponse("text.html", {"request": request, "query":query, "answer": answer, "context": context})


    