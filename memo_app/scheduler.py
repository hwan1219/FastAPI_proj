from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker
from app.db.connection import engine
from app.models.session import Session

SessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  expire_on_commit=False,
  bind=engine
)

def delete_expired_sessions():
  db = SessionLocal()
  try:
    now = datetime.now(timezone.utc)
    expired_sessions = db.query(Session).filter(Session.expires_at < now).all()
    for session in expired_sessions:
      db.delete(session)
    db.commit()
    print(f"[{now}] Expired sessions deleted.")
  
  except Exception as e:
    db.rollback()
    print(f"Error deleting expired sessions: {e}")
  
  finally:
    db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(delete_expired_sessions, 'interval', minutes=60)

def start_scheduler():
  scheduler.start()