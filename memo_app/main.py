from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import auth, memos
from fastapi import Request
from fastapi.responses import HTMLResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(memos.router)
app.include_router(auth.router)

@app.get("/", response_class=HTMLResponse)
def main_page(request: Request):
  session_token = request.cookies.get("session_token")
  
  if session_token == "valid_token":
    return templates.TemplateResponse("index.html", {"request": request})
  else:
    return templates.TemplateResponse("login.html", {"request": request})