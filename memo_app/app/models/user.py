from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.db.base import Base

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String(30), unique=True, index=True, nullable=False)
  email = Column(String(100), unique=True, index=True, nullable=True)
  hashed_password = Column(String(128), nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))