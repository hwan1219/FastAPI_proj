# Python 3.12 / FastAPI 최신 버전 기준


# FastAPI 클래스 임포트
from fastapi import FastAPI, Query

# FastAPI 인스턴스 생성 → app 변수 이름은 uvicorn 실행 시 필요
appEX = FastAPI()

# 가장 단순한 GET 엔드포인트
# '/hello' 경로로 GET 요청이 오면 아래 함수가 실행
# 함수가 dict 를 리턴하면 FastAPI가 자동으로 JSONResponse로 변환
@appEX.get("/hello")
def read_hello():
  # Hello, FastAPI!
  # 반환: {"message": "Hello FastAPI"}
  return {"message": "Hello FastAPI"}

@appEX.get("/greet") 
def greet_user(name: str = Query(default=..., min_length=1, max_length=50)):
# def greet_user(name: str = Query(..., min_length=1, max_length=50)):
  return {"message": f"Hello, {name}!"}

# 서버 실행 방법 (터미널):
# uvicorn main:app --reload 
# └─ main  : 모듈 이름(파일명)
# └─ app   : FastAPI 인스턴스 변수
# └─ --reload : 수정 시 자동 재시작 (개발용)



# 터미널에서 api 내용 확인
# curl http://127.0.0.1:8000/hello