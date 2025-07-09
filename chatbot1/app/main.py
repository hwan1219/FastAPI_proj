# 실행시 : uvicorn app.main:app --reload

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router
import uvicorn
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
app.include_router(router)

if __name__ == "__main__":
  uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)