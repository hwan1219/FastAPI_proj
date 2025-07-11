# My Memo App
# FastAPI + SQLAlchemy + MySQL 예제

# 1) 기본 라이브러리 임포트
from typing import Optional # 선택적 필드를 위한 타입 힌트
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import Session # 실제 DB 세션 객체
from sqlalchemy.ext.declarative import declarative_base # ORM 모델 서비스
from pydantic import BaseModel

# 2) 앱 & 템플릿 초기화
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 3) 데이터베이스 설정
database_url = "mysql+pymysql://root:1234@localhost/my_memo_app"
engine = create_engine(database_url, echo=False, pool_pre_ping=True)
Base = declarative_base()

# 4) ORM 모델 정의 (python → DB)
class Memo(Base):
  __tablename__ = 'memo'
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String(100))
  content = Column(String(1000))

# 5) Pydantic(검증) 스키마
class MemoCreate(BaseModel):
  title: str
  content: str
  
# 6) DB 세션 의존성
def get_db():
  db = Session(bind=engine)
  try:
    yield db
  finally:
    db.close()
    

# CRUD 라우트 정의

# 1) 메모 생성
@app.post("/memos")
async def create_memo(
  memo: MemoCreate,
  db: Session = Depends(get_db)
):
  new_memo = Memo(title=memo.title, content=memo.content)
  db.add(new_memo) # DB INSERT
  db.commit() # DB COMMIT
  db.refresh(new_memo) # DB id(PK) 포함 최신 상태 반영
  return {
    "id": new_memo.id,
    "title": new_memo.title,
    "content": new_memo.content
  }