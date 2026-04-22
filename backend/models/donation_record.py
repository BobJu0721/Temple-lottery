import uuid
from sqlalchemy import Column, Integer, String, DateTime, func
from backend.database import Base

class DonationRecord(Base):
    __tablename__ = "donation_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    reference_no = Column(String, unique=True, nullable=False)
    session_id = Column(String, nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    note = Column(String, nullable=True)
    status = Column(String, default="recorded", nullable=False)
    donated_at = Column(DateTime, default=func.now(), index=True)
