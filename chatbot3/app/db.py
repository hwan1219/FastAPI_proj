import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
# DB 관련 값도 로컬 환경이 아닐 땐 env 파일에 넣어서 쓸 것

DB_CONFIG = {
  'host': os.getenv('DB_HOST'),
  'user': os.getenv('DB_USER'),
  'password': os.getenv('DB_PASSWORD'),
  'database': os.getenv('DB_DATABASE'),
  'port': int(os.getenv('DB_PORT', 3306))
}

def get_connection():
  try:
    connection = mysql.connector.connect(**DB_CONFIG)
    return connection
  except Error as e:
    print(f"DB 연결 오류: {e}")
    return None

def insert_chat(user_message, bot_response, temperature=1.0, top_p=1.0, presence_penalty=0.0, frequency_penalty=0.0, max_tokens=500):
  conn = get_connection()
  if conn:
    try:
      cursor = conn.cursor()
      sql = """
      INSERT INTO chat_history
      (user_message, bot_response, temperature, top_p, presence_penalty, frequency_penalty, max_tokens)
      VALUES (%s, %s, %s, %s, %s, %s, %s)
      """
      cursor.execute(sql, (user_message, bot_response, temperature, top_p, presence_penalty, frequency_penalty, max_tokens))
      conn.commit()
    finally:
      cursor.close()
      conn.close()

def get_all_chats():
  conn = get_connection()
  chats = []
  if conn:
    try:
      cursor = conn.cursor()
      sql = "SELECT user_message, bot_response, timestamp FROM chat_history ORDER BY id ASC"
      cursor.execute(sql)
      chats = cursor.fetchall()
    finally:
      cursor.close()
      conn.close()
  return chats