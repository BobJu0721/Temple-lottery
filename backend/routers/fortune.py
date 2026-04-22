import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import schemas, crud

router = APIRouter(tags=["fortune"])

def get_or_create_session(response: Response, session_id: str | None = Cookie(default=None)):
    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=31536000)
    return session_id

@router.get("/gods", response_model=List[schemas.GodResponse])
def get_gods(db: Session = Depends(get_db)):
    return crud.god.get_gods(db)

@router.post("/fortune/draw", response_model=schemas.FortuneDrawResponse)
def draw_fortune(
    request: schemas.FortuneDrawRequest,
    response: Response,
    session_id: str = Depends(get_or_create_session),
    db: Session = Depends(get_db)
):
    record, content = crud.fortune.draw_fortune(db, request, session_id)
    if not record or not content:
        raise HTTPException(status_code=404, detail="神明或籤詩資料不存在")
    
    return schemas.FortuneDrawResponse(
        record_id=record.id,
        fortune_no=record.fortune_no,
        level=record.level,
        poem=content.poem,
        interpretation={
            "career": content.career_interp,
            "love": content.love_interp,
            "health": content.health_interp,
            "study": content.study_interp
        },
        drawn_at=record.drawn_at
    )

@router.get("/fortune/history", response_model=List[schemas.FortuneRecordResponse])
def get_fortune_history(
    session_id: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):
    if not session_id:
        return []
    records = crud.fortune.get_fortune_records_by_session(db, session_id)
    
    # Enrich with poems and interpretations
    result = []
    for r in records:
        content = crud.fortune.get_fortune_content(db, r.god_id, r.fortune_no)
        r_dict = {
            "id": r.id,
            "session_id": r.session_id,
            "god_id": r.god_id,
            "fortune_no": r.fortune_no,
            "level": r.level,
            "wish_text": r.wish_text,
            "drawn_at": r.drawn_at,
        }
        if content:
            r_dict["poem"] = content.poem
            r_dict["interpretation"] = {
                "career": content.career_interp,
                "love": content.love_interp,
                "health": content.health_interp,
                "study": content.study_interp
            }
        result.append(r_dict)
    return result

@router.get("/fortune/{god_id}/{fortune_no}", response_model=schemas.FortuneContentResponse)
def get_fortune_content(god_id: int, fortune_no: int, db: Session = Depends(get_db)):
    content = crud.fortune.get_fortune_content(db, god_id, fortune_no)
    if not content:
        raise HTTPException(status_code=404, detail="找不到籤詩")
    return content
