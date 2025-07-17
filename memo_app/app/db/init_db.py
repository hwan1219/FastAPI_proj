from app.db.connection import engine
from app.db.base import Base
from app.models import memo, session, user

def init_db():
  Base.metadata.create_all(bind=engine)
  
if __name__ == "__main__":
  init_db()

# source .venv/Scripts/activate  
# python -m app.db.init_db