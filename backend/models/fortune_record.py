import uuid
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class FortuneRecord(Base):
    __tablename__ = "fortune_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, nullable=False, index=True)
    god_id = Column(Integer, ForeignKey("gods.id", ondelete="RESTRICT"), nullable=False)
    fortune_no = Column(Integer, nullable=False, index=True)
    level = Column(String, nullable=False)
    wish_text = Column(String, nullable=True)
    drawn_at = Column(DateTime, default=func.now(), index=True)

    god = relationship("God", back_populates="fortune_records")
