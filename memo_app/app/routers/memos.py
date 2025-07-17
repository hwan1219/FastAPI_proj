from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.connection import get_db
from app.schemas.memo import MemoCreate, MemoUpdate, MemoResponse
from app.models.memo import Memo
from app.models.user import User
from app.routers.auth import get_current_user
# python 문법에서 폴더 이름을 app으로 하게되면 모듈/패키지 이름으로 인식함

router = APIRouter(
  prefix="/memos",
  tags=["memos"]
)

# 메모 목록 조회
@router.get("/", response_model=List[MemoResponse])
def get_memos(
  skip: int = 0,
  limit: int = 100,
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  memos = db.query(Memo).filter(Memo.user_id == current_user.id).offset(skip).limit(limit).all()
  
  return memos

@router.get("/count")
def get_memo_count(
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  count = db.query(Memo).filter(Memo.user_id == current_user.id).count()
  
  return {"count": count}

# 메모 단건 조회
@router.get("/{memo_id}", response_model=MemoResponse)
def get_memo(
  memo_id: int,
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  memo = db.query(Memo).filter(Memo.id == memo_id, Memo.user_id == current_user.id).first()
  
  if memo is None:
    raise HTTPException(
      status_code=404,
      detail="메모를 찾을 수 없거나 접근 권한이 없습니다"
    )
  return memo

# 메모 생성
@router.post("/", response_model=MemoResponse)
def create_memo(
  memo: MemoCreate,
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  new_memo = Memo(
    title=memo.title,
    content=memo.content,
    user_id=current_user.id
  )
  db.add(new_memo)
  db.commit()
  db.refresh(new_memo)
  
  return new_memo
  
# 메모 수정
@router.put("/{memo_id}", response_model=MemoResponse)
def update_memo(
  memo_id: int,
  memo_update: MemoUpdate,
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  memo = db.query(Memo).filter(
    Memo.id == memo_id,
    Memo.user_id == current_user.id
  ).first()
  
  if memo is None:
    raise HTTPException(
      status_code=404,
      detail="메모를 찾을 수 없습니다"
    )
  
  memo.title = memo_update.title
  memo.content = memo_update.content
  
  db.commit()
  db.refresh(memo)
  
  return memo

# 메모 삭제
@router.delete("/{memo_id}")
def delete_memo(
  memo_id: int,
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  memo = db.query(Memo).filter(Memo.id == memo_id, Memo.user_id == current_user.id).first()
  
  if memo is None:
    raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다")
  
  db.delete(memo)
  db.commit()
  
  return Response(status_code=204)