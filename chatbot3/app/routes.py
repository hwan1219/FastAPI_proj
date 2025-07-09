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

@router.post("/api/chat")
def chat(
  request: Request,
  user_message: str = Form(...),
  temperature: float = Form(1.0),
  top_p: float = Form(1.0),
  max_tokens: int = Form(500),
  presence_penalty: float = Form(0.0),
  frequency_penalty: float = Form(0.0)
):
  bot_response = get_gpt_response(
    user_message,
    temperature=temperature,
    top_p=top_p,
    max_tokens=max_tokens,
    presence_penalty=presence_penalty,
    frequency_penalty=frequency_penalty
  )
  insert_chat(
    user_message,
    bot_response,
    temperature=temperature,
    top_p=top_p,
    presence_penalty=presence_penalty,
    frequency_penalty=frequency_penalty,
    max_tokens=max_tokens
  )

  chats = get_all_chats()
  return templates.TemplateResponse("index.html", {
    "request": request,
    "chats": chats,
    "temperature": temperature,
    "top_p": top_p,
    "max_tokens": max_tokens,
    "presence_penalty": presence_penalty,
    "frequency_penalty": frequency_penalty
  })