from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_url = "mysql+pymysql://root:1234@localhost/my_memo_app"
engine = create_engine(database_url, echo=False, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()