from sqlalchemy import Column, Integer, String, DateTime, func
from backend.database import Base

class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
