import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')) 

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_ROLE = { 
  "role": "system", 
  "content": "당신은 30 년 경력의 금융 전문가입니다. 투자, 예금, 연금, 세금, 부동산, 주식 등 다양한 금융 분야에 대해 전문적인 조언을 제공하세요. 전문적이면서도 친절하고 이해하기 쉬운 방식으로 설명해주세요." 
} 

def get_gpt_response(user_message):
  try:
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[SYSTEM_ROLE, {"role": "user", "content": user_message}],
      max_tokens=512,
      temperature=0.7
    )
    return response.choices[0].message.content.strip()
  except Exception as e:
    return f"[오류] GPT API 호출 실패: {e}"