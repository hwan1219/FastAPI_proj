from pydantic import BaseModel

class MemoCreate(BaseModel):
  title: str
  content: str

class MemoUpdate(BaseModel):
  title: str
  content: str

class MemoDelete(BaseModel):
  id: int

class MemoResponse(BaseModel):
  id: int
  title: str
  content: str
  
  class Config:
    orm_mode = True