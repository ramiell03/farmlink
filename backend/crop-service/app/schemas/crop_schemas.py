from pydantic import BaseModel
from typing import Optional

class CropCreate(BaseModel):
    name: str
    description: Optional[str] = None
    
class CropResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] 
    is_active:bool
    
    class Config:
        from_attributes = True