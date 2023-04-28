#---------------------------------
# Form 테스트 예제
# pip install starlette
#---------------------------------

from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from typing_extensions import Annotated

app = FastAPI()

# HTML 파일을 제공하기 위한 정적 파일 경로를 설정합니다.
#----------------------------------------------------------------------
# FastAPI 이용한 Form 테스트
# => 로그인 폼에 id/pwd 입력하면 입력받은 id/pwd 출력하는 예제임.
#
# - 설치 :pip install fastapi[all]
# - python 업데이트(옵션) : conda install -c anaconda python=3.10 (3.10이상 필요)
# - 실행 : uvicorn model1:app --reload --host=0.0.0.0 --port=9000 -> 이후 http://127.0.0.1:9000/ 젒속
# - 설명 : https://fastapi.tiangolo.com/ko/tutorial/request-forms/
#----------------------------------------------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    result = {"username": username, "password": password}
    return result

@app.get("/")
async def read_form():
    
    # HTML 파일의 경로를 지정합니다.
    html_content = """
   <html>
    <head>
        <title>Login Form</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Login</h1>
        <form action="/login/" method="post" onsubmit="submitForm(event)">
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username"><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password"><br><br>
            <input type="submit" value="Submit">
        </form>
        <div id="result"></div>
        <script>
            function submitForm(event) {
                event.preventDefault();
                const form = event.target;
                const username = form.elements.username.value;
                const password = form.elements.password.value;
                const result = document.getElementById("result");
                result.innerText = `Username: ${username}\nPassword: ${password}`;
            }
        </script>
    </body>
 </html>
    """
    
    # HTML 코드를 반환합니다.
    return HTMLResponse(content=html_content, status_code=200)

