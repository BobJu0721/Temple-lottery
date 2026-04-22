from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class FortuneDrawRequest(BaseModel):
    god_id: int
    wish_text: Optional[str] = None

class FortuneContentResponse(BaseModel):
    id: int
    god_id: int
    fortune_no: int
    level: str
    poem: str
    career_interp: str
    love_interp: str
    health_interp: str
    study_interp: str
    updated_at: datetime

    class Config:
        from_attributes = True

class FortuneDrawResponse(BaseModel):
    record_id: str
    fortune_no: int
    level: str
    poem: str
    interpretation: Dict[str, str]
    drawn_at: datetime

class FortuneRecordResponse(BaseModel):
    id: str
    session_id: str
    god_id: int
    fortune_no: int
    level: str
    wish_text: Optional[str] = None
    drawn_at: datetime
    
    # We can also include the related fortune content if needed for history display
    poem: Optional[str] = None
    interpretation: Optional[Dict[str, str]] = None

    class Config:
        from_attributes = True
