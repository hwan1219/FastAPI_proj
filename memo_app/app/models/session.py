from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base

class Session(Base):
  __tablename__ = 'sessions'
  id = Column(Integer, primary_key=True, index=True)
  token = Column(String(64), unique=True, index=True)
  user_id = Column(Integer, ForeignKey("users.id"))
  user = relationship("User", backref="sessions")
  expires_at = Column(TIMESTAMP, nullable=False)
  created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)