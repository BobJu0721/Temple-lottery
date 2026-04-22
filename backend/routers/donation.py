import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import schemas, crud

router = APIRouter(tags=["donation"])

def get_or_create_session(response: Response, session_id: str | None = Cookie(default=None)):
    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=31536000)
    return session_id

@router.post("/donation", response_model=schemas.DonationCreateResponse)
def create_donation(
    request: schemas.DonationCreateRequest,
    response: Response,
    session_id: str = Depends(get_or_create_session),
    db: Session = Depends(get_db)
):
    record = crud.donation.create_donation(db, request, session_id)
    return schemas.DonationCreateResponse(
        reference_no=record.reference_no,
        message=f"感謝 {request.name or '大德'}，捐款 ${request.amount} 已成功記錄"
    )

@router.get("/donation/history", response_model=List[schemas.DonationRecordResponse])
def get_donation_history(
    session_id: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):
    if not session_id:
        return []
    records = crud.donation.get_donation_records_by_session(db, session_id)
    return records

@router.get("/donation/{reference_no}", response_model=schemas.DonationRecordResponse)
def get_donation_by_ref(reference_no: str, db: Session = Depends(get_db)):
    record = crud.donation.get_donation_by_reference(db, reference_no)
    if not record:
        raise HTTPException(status_code=404, detail="找不到該筆捐款紀錄")
    return record
