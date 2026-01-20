from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Optional

class CropCreate(BaseModel):
    name: str
    description: Optional[str] = None
    
class CropResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] 
    is_active:bool
    created_at: datetime | None = None
    
    class Config:
        from_attributes = True