"""
포함 내용
  Jinja2Templates 설정, HTML 응답 렌더
  DEMO: /welcome?name= 홍길동 (과제1)
  DEMO: /users (과제2) +/users/add 로 데이터 추가
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
import os

app = FastAPI(title="FastAPI Jinja2 Demo")

# 템플릿 설정
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# 메모리 사용자 리스트
user_list: List[str] = []

# 기본 /welcome
"""
Query name 받아서 HTML 페이지 렌더
curl "127.0.0.1:8000/welcome?name=홍길동"
"""
@app.get("/welcome", response_class=HTMLResponse)
def welcome(
  request: Request,
  name: str = "World"
):
  return templates.TemplateResponse(
    "welcome.html",
    {"request": request, "name": name}
  )

#  – 사용자 목록 페이지
"""
HTML form 또는 curl 로 사용자 추가
curl -X POST -d "name=Tom" 127.0.0.1:8000/users/add
"""
@app.post("/api/users")
def add_user(name: str = Form(...)):
  user_list.append(name)
  return {"name": name}


"""
사용자 리스트를 테이블로 렌더
curl 127.0.0.1:8000/users
"""
@app.get("/users", response_class=HTMLResponse)
def show_users(request: Request):
  return templates.TemplateResponse(
    "users.html",
    {"request": request, "users": user_list}
  )