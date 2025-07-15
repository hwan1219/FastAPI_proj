from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
  username: str = Field(..., min_length=3, max_length=30)
  email: Optional[EmailStr] = None
  
class UserCreate(UserBase):
  password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
  username: str = Field(..., min_length=3, max_length=30)
  password: str = Field(..., min_length=6)
      
class UserUpdate(BaseModel):
  username: Optional[str] = Field(None, min_length=3, max_length=30)
  email: Optional[EmailStr] = None

class PasswordUpdate(BaseModel):
  current_password: str = Field(..., min_length=6)
  new_password: str = Field(..., min_length=6)
      
class UserResponse(UserBase):
  id: int
  created_at: Optional[datetime]
  
  class Config:
    orm_mode = True