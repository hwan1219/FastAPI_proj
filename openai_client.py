"""
settings_openai.py
Python 3.12 / python-dotenv 사용 예시
"""

from dotenv import load_dotenv
import os

# 1) .env 읽어 환경변수에 주입
load_dotenv() # 기본값: cwd의 .env 파일

# 2) 변수 추출
OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
  raise RuntimeError("OPENAI_API_KEY가 설정되지 않았습니다!")

# 3) OpenAI 패키지 사용 예
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

resp = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[{"role": "user", "content": "안녕, GPT!"}],
)
print(resp.choices[0].message.content)