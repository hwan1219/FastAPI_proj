from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MemoBase(BaseModel):
  title: str = Field(..., max_length=100)
  content: str = Field(..., max_length=1000)

class MemoCreate(MemoBase):
  pass

class MemoUpdate(MemoBase):
  pass

class MemoResponse(MemoBase):
  id: int
  created_at: Optional[datetime]
  updated_at: Optional[datetime]
  
  class Config:
    orm_mode = True