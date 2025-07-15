from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.db.base import Base

class Memo(Base):
  __tablename__ = 'memo'
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String(100))
  content = Column(String(1000))
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))