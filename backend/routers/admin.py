import os
from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from backend.database import get_db
from backend import schemas, crud
from backend.models.donation_record import DonationRecord
from backend.models.fortune_record import FortuneRecord

router = APIRouter(prefix="/admin", tags=["admin"])

SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")

def verify_admin_session(admin_session: str | None = Cookie(default=None)):
    # Very simple session check for MVP, in real app use JWT or itsdangerous
    if not admin_session or admin_session != "admin_logged_in_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="請先登入後台"
        )
    return True

@router.post("/login", response_model=schemas.AdminLoginResponse)
def login(request: schemas.AdminLoginRequest, response: Response, db: Session = Depends(get_db)):
    admin = crud.admin.get_admin_by_username(db, request.username)
    if not admin or not crud.admin.verify_password(request.password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="帳號或密碼錯誤")
    
    # Update last login
    admin.last_login = datetime.now()
    db.commit()

    # Set fake token for MVP
    response.set_cookie(key="admin_session", value="admin_logged_in_token", httponly=True)
    return {"message": "登入成功"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("admin_session")
    return {"message": "登出成功"}

@router.get("/donations/stats", response_model=schemas.StatsResponse, dependencies=[Depends(verify_admin_session)])
def get_donation_stats(db: Session = Depends(get_db)):
    today = datetime.now().date()
    start_of_today = datetime.combine(today, datetime.min.time())
    start_of_week = start_of_today - timedelta(days=today.weekday())
    start_of_month = start_of_today.replace(day=1)

    daily = db.query(func.sum(DonationRecord.amount)).filter(DonationRecord.donated_at >= start_of_today).scalar() or 0
    weekly = db.query(func.sum(DonationRecord.amount)).filter(DonationRecord.donated_at >= start_of_week).scalar() or 0
    monthly = db.query(func.sum(DonationRecord.amount)).filter(DonationRecord.donated_at >= start_of_month).scalar() or 0

    return schemas.StatsResponse(daily=daily, weekly=weekly, monthly=monthly)

@router.get("/donations", response_model=List[schemas.AdminDonationRecordResponse], dependencies=[Depends(verify_admin_session)])
def get_donations(db: Session = Depends(get_db)):
    return db.query(DonationRecord).order_by(DonationRecord.donated_at.desc()).all()

@router.get("/fortune/stats", dependencies=[Depends(verify_admin_session)])
def get_fortune_stats(db: Session = Depends(get_db)):
    # Example: Top 10 drawn fortunes
    stats = db.query(
        FortuneRecord.fortune_no, 
        func.count(FortuneRecord.id).label("count")
    ).group_by(FortuneRecord.fortune_no).order_by(desc("count")).limit(10).all()
    
    return [{"fortune_no": row.fortune_no, "count": row.count} for row in stats]
