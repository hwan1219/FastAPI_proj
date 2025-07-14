from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, models, db
# python 문법에서 폴더 이름을 app으로 하게되면 모듈/패키지 이름으로 인식함

router = APIRouter(
  prefix="/memos",
  tags=["memos"]
)

# 메모 목록 조회
@router.get("/", response_model=List[schemas.MemoResponse])
def get_memos(
  skip: int = 0,
  limit: int = 100,
  db: Session = Depends(db.get_db)
):
  memos = db.query(models.Memo).offset(skip).limit(limit).all()
  return memos

# 메모 단건 조회
@router.get("/", response_model=schemas.MemoResponse)
def get_memo(
  memo_id: int,
  db: Session = Depends(db.get_db)
):
  memo = db.query(models.Memo).filter(models.Memo.id == memo.id).first()
  
  if memo is None:
    raise HTTPException(
      status_code=404,
      detail="메모를 찾을 수 없습니다"
    )
  return memo

# 메모 생성
@router.post("/", response_model=schemas.MemoResponse)
def create_memo(
  memo: schemas.MemoCreate,
  db: Session = Depends(db.get_db)
):
  new_memo = models.Memo(title=memo.title, content=memo.content)
  db.add(new_memo)
  db.commit()
  db.refresh(new_memo)
  
  return {
    "id": new_memo.id,
    "title": new_memo.title,
    "content": new_memo.content
  }
  
# 메모 수정
@router.put("/{memo_id}", response_model=schemas.MemoResponse)
def update_memo(
  memo_id: int,
  memo_update: schemas.MemoUpdate,
  db: Session = Depends(db.get_db)
):
  memo = db.query(models.Memo).filter(models.Memo.id == memo_id).first()
  
  if memo is None:
    raise HTTPException(
      status_code=404,
      detail="메모를 찾을 수 없습니다"
    )
  
  memo.title = memo_update.title
  memo.content = memo_update.content
  
  db.commit()
  
  return memo

# 메모 삭제
@router.delete("/{memo_id}")
def delete_memo(
  memo_id: int,
  db: Session = Depends(db.get_db)
):
  memo = db.query(models.Memo).filter(models.Memo.id == memo_id).first()
  
  if memo is None:
    raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다")
  
  db.delete(memo)
  db.commit()
  
  return Response(status_code=204)