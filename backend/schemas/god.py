from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GodBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class GodResponse(GodBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
