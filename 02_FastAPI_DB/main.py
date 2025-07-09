# My Memo App
# FastAPI + SQLAlchemy + MySQL 예제

# 1) 기본 라이브러리 임포트
from typing import Optional # 선택적 필드를 위한 타입 힌트
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import Session # 실제 DB 세션 객체
from sqlalchemy.ext.declarative import declarative_base # ORM 모델 서비스
from pydantic import BaseModel

# 2) 앱 & 템플릿 초기화