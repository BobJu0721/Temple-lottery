from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class AdminLoginResponse(BaseModel):
    message: str

class AdminUserResponse(BaseModel):
    id: int
    username: str
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class StatsResponse(BaseModel):
    daily: int
    weekly: int
    monthly: int
