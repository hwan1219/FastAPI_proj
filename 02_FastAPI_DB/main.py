# My Memo App
# FastAPI + SQLAlchemy + MySQL 예제

# 1) 기본 라이브러리 임포트
from typing import Optional, List # 선택적 필드를 위한 타입 힌트
from fastapi import FastAPI, Request, Response, Depends, Path, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import Session, sessionmaker # 실제 DB 세션 객체
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
# 생성용
class MemoCreate(BaseModel):
  title: str
  content: str

# 수정용
class MemoUpdate(BaseModel):
  title: str
  content: str
  
# 삭제용
class MemoDelete(BaseModel):
  id: int
  
# 출력용  
class MemoResponse(BaseModel):
  id: int
  title: str
  content: str
  
  class Config:
    orm_mode = True
  
# 6) DB 세션 의존성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
    

# CRUD 라우트 정의

# 1) 메모 생성
@app.post("/memos", response_model=MemoResponse, status_code=201)
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
  
# 2) 메모 목록 조회
@app.get("/memos", response_model=List[MemoResponse])
async def get_memo(
  db: Session = Depends(get_db)
):
  memos = db.query(Memo).all()
  return memos

# 3) 메모 수정
@app.put("/memos/{memo_id}", response_model=MemoResponse, status_code=201)
async def update_memo(
  memo_id: int,
  memo: MemoUpdate,
  db: Session = Depends(get_db)
):
  # 기존 메모 조회
  existing_memo = db.query(Memo).filter(Memo.id == memo_id).first()
  
  # 메모가 없으면 404 응답
  if existing_memo is None:
    raise HTTPException(
      status_code=404,
      detail="메모를 찾을 수 없습니다"
    )
  
  # 값 덮어쓰기
  existing_memo.title = memo.title
  existing_memo.content = memo.content
  
  # 커밋 & 최신화
  db.commit()
  db.refresh(existing_memo)
  
  return existing_memo
  
# 4) 메모 삭제
@app.delete("/memos/{memo_id}", status_code=204)
async def delete_memo(
  memo_id: int,
  db: Session = Depends(get_db)
):
  memo = db.query(Memo).filter(Memo.id == memo_id).first()
  
  if memo is None:
    raise HTTPException(
      status_code=404,
      detail="메모를 찾을 수 없습니다"
    )
  
  db.delete(memo)
  db.commit()
  
  return Response(status_code=204)

# 템플릿 & 기본 페이지 라우트
@app.get("/")
async def read_root(request: Request):
  return templates.TemplateResponse(
    "home.html",
    {"request": request}
  )

@app.get("/about")
async def about():
  return {"message": "이것은 마이 메모 앱의 소개 페이지입니다."}