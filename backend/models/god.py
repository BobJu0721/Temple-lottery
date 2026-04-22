from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from backend.database import Base

class God(Base):
    __tablename__ = "gods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

    fortune_contents = relationship("FortuneContent", back_populates="god")
    fortune_records = relationship("FortuneRecord", back_populates="god")
