from main import Base, engine
from main import Memo

def init_db():
  Base.metadata.create_all(bind=engine)
  print("테이블 생성 완료")
  
if __name__ == "__main__":
  init_db()