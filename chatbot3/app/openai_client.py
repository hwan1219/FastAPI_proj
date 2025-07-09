import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')) 

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)

def get_gpt_response(
  user_message,
  temperature=1.0,
  top_p=1.0,
  max_tokens=500,
  presence_penalty=0.0,
  frequency_penalty=0.0
):
  try:
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": user_message}],
      temperature=temperature,
      top_p=top_p,
      max_tokens=max_tokens,
      presence_penalty=presence_penalty,
      frequency_penalty=frequency_penalty
    )
    return response.choices[0].message.content.strip()
  except Exception as e:
    return f"[오류] GPT API 호출 실패: {e}"