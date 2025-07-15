from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SessionBase(BaseModel):
  token: str
  user_id: int
  expires_at: datetime
  
class SessionCreate(SessionBase):
  pass

class SessionResponse(SessionBase):
  id: int
  created_at: Optional[datetime]
  
  class Config:
    orm_mode = True