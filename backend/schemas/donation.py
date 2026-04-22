from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DonationCreateRequest(BaseModel):
    amount: int = Field(..., gt=0)
    name: Optional[str] = None
    phone: Optional[str] = None
    note: Optional[str] = None

class DonationCreateResponse(BaseModel):
    reference_no: str
    message: str

class DonationRecordResponse(BaseModel):
    id: str
    reference_no: str
    amount: int
    name: Optional[str] = None
    note: Optional[str] = None
    status: str
    donated_at: datetime
    # Intentionally not exposing full phone number to frontend for privacy

    class Config:
        from_attributes = True

class AdminDonationRecordResponse(BaseModel):
    id: str
    reference_no: str
    session_id: str
    amount: int
    name: Optional[str] = None
    phone: Optional[str] = None
    note: Optional[str] = None
    status: str
    donated_at: datetime

    class Config:
        from_attributes = True
