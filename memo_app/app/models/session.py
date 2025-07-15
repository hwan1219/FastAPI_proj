from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base

class Session(Base):
  __tablename__ = 'sessions'
  id = Column(Integer, primary_key=True, index=True)
  token = Column(String(64), unique=True, index=True)
  user_id = Column(Integer, ForeignKey("users.id"))
  user = relationship("User", backref="sessions")
  expires_at = Column(DateTime)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))