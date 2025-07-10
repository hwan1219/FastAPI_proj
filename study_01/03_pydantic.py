from enum import Enum
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Path, Body
from pydantic import BaseModel, EmailStr, Field, field_validator

app = FastAPI(title="FastAPI Pydantic Demo")

# 1) 기본 User Model + 간단 CRUD
class User(BaseModel):
  id: int
  name: str = Field(..., min_length=1, max_length=30)
  email: EmailStr
  age: Optional[int] = Field(None, ge=0, le=120)
  
  # 커스텀 검증: 이름에 공백 허용 안 함
  @field_validator("name")
  @classmethod
  def no_space(cls, value):
    if " " in value:
      raise ValueError("공백 없는 이름만 허용")
    return value

fake_db: List[User] = []

# 새 사용자 등록
@app.post("/users", response_model=User, status_code=201)
def create_user(user: User):
  # id 중복 체크
  if any(u.id == user.id for u in fake_db):
    raise HTTPException(
      status_code=400,
      detail="ID가 이미 존재합니다."
    )
  fake_db.append(user)
  return user

# 모든 사용자 조회
@app.get("/users", response_model=List[User])
def get_users():
  return fake_db

# 사용자 전체 업데이트
@app.put("/users/{id}", response_model=User)
def update_user(
  id: int = Path(..., ge=1),
  updated_user: User = Body(...)
):
  for idx, user in enumerate(fake_db):
    if user.id == id:
      fake_db[idx] = updated_user
      return updated_user
  raise HTTPException(
    status_code=404,
    detail="사용자를 찾을 수 없습니다."
  )
  

# 2) 과제 - Book 모델 & POST
class Book(BaseModel):
  isbn: str = Field(..., pattern=r"^\d{13}") # 13자리 숫자
  title: str = Field(..., min_length=1, max_length=100)
  price: float = Field(..., gt=0)

books_db: List[Book] = []

@app.post("/books", response_model=Book, status_code=201)
def add_book(book: Book):
  books_db.append(book)
  return book