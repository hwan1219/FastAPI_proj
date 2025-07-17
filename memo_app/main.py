from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import auth
from app.routers import memos
from app.models.memo import Memo
from sqlalchemy.orm import Session
from app.routers.auth import get_current_user
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
  
@app.get("/register", response_class=HTMLResponse)
def get_register(request: Request):
  return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def get_login(request: Request):
  return templates.TemplateResponse("login.html", {"request": request})

@app.get("/new_memo", response_class=HTMLResponse)
def get_login(request: Request):
  return templates.TemplateResponse("new_memo.html", {"request": request})

@app.get("/memo_detail", response_class=HTMLResponse)
def get_memo_detail(request: Request):
  return templates.TemplateResponse(
    "memo_detail.html", {"request": request}
  )

@app.get("/memo_edit", response_class=HTMLResponse)
def get_memo_edit(request: Request):
  return templates.TemplateResponse(
    "memo_edit.html",
    {"request": request}
  )
  
@app.get("/profile", response_class=HTMLResponse)
def profile_page(
  request: Request
):
  return templates.TemplateResponse(
    "profile.html", {"request": request}
  )