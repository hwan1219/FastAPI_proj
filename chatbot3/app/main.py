from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router
import uvicorn
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
app.include_router(router)