# ORM 미사용, SQL 직접 사용 (db.py 참고)
# 필요시 Pydantic 모델 정의
from pydantic import BaseModel

class ChatMessage(BaseModel):
  user_message: str
  bot_response: str
  timestamp: str = None