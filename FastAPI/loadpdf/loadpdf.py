from enum import Enum
from typing import Union
from fastapi import FastAPI, File, UploadFile, Query, Cookie, Form, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from PyPDF2 import PdfReader
from utils import MyUtils
import io

myutils = MyUtils(yam_file_path='./data/settings.yaml')

app=FastAPI() # app 인스턴스 생성
templates = Jinja2Templates(directory="template_files") # html 파일이 있는 경로를 지정.

@app.get("/")  # 경로 동작 데코레이터 작성
async def root(): # 경로 동작 함수 작성
	return {"msg": "load pdf 예제 World"}

# 업로드 파일 선택 창 
@app.get("/upload/file")
async def upload(request:Request, user_id:str):
    assert user_id, f'user_id is empty'

    myutils.log_message(f'\n[info][/upload/file] user_id:{user_id}\n')
    
    return templates.TemplateResponse("upload_file.html", {"request": request, "user_id":user_id})

# 업로드한  pdf 파일 읽어와서 처리
@app.post("/upload")
async def upload(request: Request, file: UploadFile = File(...)):
    form = await request.form()
    user_id = form.get("user_id")

    myutils.log_message(f'\n[info][/upload] user_id:{user_id}\n')
    
    # MIME 타입 확인
    if file.content_type != "application/pdf":
        return HTMLResponse(content=f"""
        <html>
            <head>
                <title>Error</title>
            </head>
            <body>
                <h1>Upload PDF</h1>
                <p style="color:red;">PDF 파일이 아닙니다.</p>
                <a href="/upload/file?user_id={user_id}">Go back</a>
            </body>
        </html>
        """, status_code=400)
    
    content = await file.read()
    pdf_reader = PdfReader(io.BytesIO(content))
    markdown_text = ""
    
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        if text:
            markdown_text += f"## Page {page_num + 1}\n\n{text}\n\n"

    file_name = file.filename
    
    return templates.TemplateResponse("upload_file_text.html", {"request": request, "user_id":user_id, "file_name":file_name, "text":markdown_text})
   