# 실행시 : uvicorn app.main:app --reload

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router
import uvicorn
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
app.include_router(router)

# if __name__ == "__main__":
#   uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
# 현재 파일을 기준으로 uvicorn.run 에 들어가는 경로나 모듈의 경로 등을 맞춰 줘야함
# app.main:app >> main:app
# from app.routes >> from .routes