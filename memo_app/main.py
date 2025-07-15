from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import auth, memos
from sqlalchemy.orm import Session
from fastapi import Request
from fastapi.responses import HTMLResponse
from scheduler import scheduler, start_scheduler
from app.db.connection import get_db
from fastapi import HTTPException
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
  start_scheduler()
  yield
  scheduler.shutdown()
  
app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(memos.router)
app.include_router(auth.router)


@app.get("/", response_class=HTMLResponse)
def main(request: Request, db: Session = Depends(get_db)):
  try:
    auth.get_current_user(session_token=request.cookies.get("session_token"), db=db)
    return templates.TemplateResponse("index.html", {"request": request})
  except HTTPException:
    return templates.TemplateResponse("login.html", {"request": request})