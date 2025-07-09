import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')) 

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)

def get_gpt_response(user_message):
  try:
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": user_message}],
      max_tokens=512,
      temperature=0.7
    )
    return response.choices[0].message.content.strip()
  except Exception as e:
    return f"[오류] GPT API 호출 실패: {e}"