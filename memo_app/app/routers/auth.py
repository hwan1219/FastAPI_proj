from fastapi import APIRouter, Depends, Response, Cookie, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import uuid
from datetime import datetime, timezone, timedelta

from app.db.connection import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserUpdate, PasswordUpdate

router = APIRouter(
  prefix="/auth",
  tags=["auth"]
)

# 비밀번호 해시화 모듈
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 비밀번호 해시화 함수
def hash_pwd(pwd: str):
  return pwd_context.hash(pwd)

# 비밀번호 검증 함수
def verify_pwd(plain_pwd: str, hashed_pwd: str):
  return pwd_context.verify(plain_pwd, hashed_pwd)

# 로그인 상태 확인
def get_current_user(session_token: str = Cookie(None), db: Session = Depends(get_db)):
  if not session_token:
    raise HTTPException(
      status_code=401,
      detail="로그인이 필요합니다"
    )
  
  session = db.query(Session).filter(Session.token == session_token).first()
  if not session or session.expires_at < datetime.now(timezone.utc):
    raise HTTPException(
      status_code=401,
      detail="세션이 만료되었습니다"
    )
  
  user = db.query(User).filter(User.id == session.user_id).first()
  
  return user

# 회원가입
@router.post("/register", status_code=201)
def register(
  user: UserCreate,
  db: Session = Depends(get_db)
):
  existing_user = db.query(User).filter(User.username == user.username).first()
  
  if existing_user:
    raise HTTPException(
      status_code=400,
      detail="이미 존재하는 사용자명입니다"
    )
  
  hashed_pwd = hash_pwd(user.password)
  new_user = User(
    username=user.username,
    hashed_password=hashed_pwd
  )
  
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  
  return Response(status_code=201)


# 로그인 (세션 쿠키 발급)
@router.post("/login")
def login(
  user: UserLogin,
  response: Response,
  db: Session = Depends(get_db)
):
  db_user = db.query(User).filter(User.username == user.username).first()
  
  if not db_user or not verify_pwd(user.password, db_user.hashed_password):
    raise HTTPException(
      status_code=401,
      detail="아이디 또는 비밀번호가 올바르지 않습니다"
    )
  
  # 세션 토큰, 기간 생성  
  session_token = str(uuid.uuid4())
  expires_at = datetime.now(timezone.utc) + timedelta(days=7)
  
  session = Session(user_id=db_user.id, token=session_token, expires_at=expires_at)
  
  db.add(session)
  db.commit()
  
  response.set_cookie(
    key="session_token",
    value=session_token,
    httponly=True,
    max_age=60*60*24*7,
    secure=True,
    samesite="lax"
  )
  
  return Response(status_code=201)

# 정보 수정
@router.put("/user/update")
def update_user(
  user_update: UserUpdate,
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  try:
    if user_update.email:
      existing_email = db.query(User).filter(User.email == user_update.email).first()
      if existing_email and existing_email.id != current_user.id:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
      current_user.email = user_update.email

    # username은 그냥 업데이트
    if user_update.username:
      current_user.username = user_update.username

    db.commit()
    db.refresh(current_user)
    return {"msg": "유저 정보가 업데이트되었습니다."}
  
  except Exception:
    db.rollback()
    raise HTTPException(status_code=500, detail="업데이트 중 오류가 발생했습니다.")

# 비밀번호 수정
@router.put("/user/password")
def update_password(
  pwd_update: PasswordUpdate,
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  if not verify_pwd(pwd_update.current_password, current_user.hashed_password):
    raise HTTPException(status_code=400, detail="현재 비밀번호가 올바르지 않습니다.")

  try:
    current_user.hashed_password = hash_pwd(pwd_update.new_password)
    db.commit()
    return {"msg": "비밀번호가 변경되었습니다."}
  
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail="비밀번호 변경 중 오류가 발생했습니다.")

# 로그아웃
@router.post("/logout")
def logout(
  response: Response,
  session_token: Optional[str] = Cookie(None),
  # Optional 생략 가능
  # Cookie(None), Query(...), Path(...) 등의 의존성 함수에서 기본값이 None일 경우 자동으로 Optional로 취급
  db: Session = Depends(get_db)
):
  if session_token:
    session = db.query(Session).filter(Session.token == session_token).first()
    if session:
      db.delete(session)
      db.commit()
    
  response.delete_cookie("session_token")
  
  return Response(status_code=200)


