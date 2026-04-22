import random
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.models.fortune_content import FortuneContent
from backend.models.fortune_record import FortuneRecord
from backend.schemas.fortune import FortuneDrawRequest

def get_fortune_content(db: Session, god_id: int, fortune_no: int):
    return db.query(FortuneContent).filter(
        FortuneContent.god_id == god_id,
        FortuneContent.fortune_no == fortune_no
    ).first()

def get_all_fortune_contents(db: Session, god_id: int):
    return db.query(FortuneContent).filter(FortuneContent.god_id == god_id).all()

def draw_fortune(db: Session, request: FortuneDrawRequest, session_id: str):
    # Randomly pick a fortune_no from 1 to 60
    fortune_no = random.randint(1, 60)
    
    # Get the content
    content = get_fortune_content(db, request.god_id, fortune_no)
    if not content:
        return None, None
    
    # Create record
    db_record = FortuneRecord(
        session_id=session_id,
        god_id=request.god_id,
        fortune_no=fortune_no,
        level=content.level,
        wish_text=request.wish_text
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return db_record, content

def get_fortune_records_by_session(db: Session, session_id: str, limit: int = 20):
    records = db.query(FortuneRecord).filter(
        FortuneRecord.session_id == session_id
    ).order_by(desc(FortuneRecord.drawn_at)).limit(limit).all()
    
    return records
