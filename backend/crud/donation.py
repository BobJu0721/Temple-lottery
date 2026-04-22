from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.models.donation_record import DonationRecord
from backend.schemas.donation import DonationCreateRequest

def generate_reference_no(db: Session) -> str:
    today = datetime.now().strftime("%Y%m%d")
    count = db.query(DonationRecord).filter(
        DonationRecord.reference_no.like(f"DON-{today}-%")
    ).count()
    return f"DON-{today}-{count+1:04d}"

def create_donation(db: Session, request: DonationCreateRequest, session_id: str):
    masked_phone = None
    if request.phone:
        if len(request.phone) >= 7:
            masked_phone = f"{request.phone[:4]}***{request.phone[-3:]}"
        else:
            masked_phone = "***"

    reference_no = generate_reference_no(db)

    db_record = DonationRecord(
        reference_no=reference_no,
        session_id=session_id,
        amount=request.amount,
        name=request.name,
        phone=masked_phone,
        note=request.note
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return db_record

def get_donation_records_by_session(db: Session, session_id: str, limit: int = 20):
    return db.query(DonationRecord).filter(
        DonationRecord.session_id == session_id
    ).order_by(desc(DonationRecord.donated_at)).limit(limit).all()

def get_donation_by_reference(db: Session, reference_no: str):
    return db.query(DonationRecord).filter(
        DonationRecord.reference_no == reference_no
    ).first()
