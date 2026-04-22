from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.database import Base

class FortuneContent(Base):
    __tablename__ = "fortune_contents"

    id = Column(Integer, primary_key=True, index=True)
    god_id = Column(Integer, ForeignKey("gods.id", ondelete="RESTRICT"), nullable=False)
    fortune_no = Column(Integer, nullable=False)
    level = Column(String, nullable=False)
    poem = Column(String, nullable=False)
    career_interp = Column(String, nullable=False)
    love_interp = Column(String, nullable=False)
    health_interp = Column(String, nullable=False)
    study_interp = Column(String, nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    god = relationship("God", back_populates="fortune_contents")

    __table_args__ = (
        UniqueConstraint("god_id", "fortune_no", name="uix_god_fortune_no"),
    )
