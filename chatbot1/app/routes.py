from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.db import insert_chat, get_all_chats
from app.openai_client import get_gpt_response

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def index(request: Request):
  chats = get_all_chats()
  return templates.TemplateResponse("index.html", {"request": request, "chats": chats})

@router.post("/chat")
def chat(request: Request, user_message: str = Form(...)):
  bot_response = get_gpt_response(user_message)
  insert_chat(user_message, bot_response)
  return RedirectResponse(url="/", status_code=303)