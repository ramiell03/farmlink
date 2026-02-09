from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class CropListingBase(BaseModel):
    crop_id: UUID
    price: int
    quantity: float
    location: str
    
class CropListingCreate(CropListingBase):
    pass
    
class CropListingResponse(BaseModel):
    id: UUID
    crop_id: UUID
    farmer_id: UUID
    price: int
    quantity: float
    location: str
    average_quality: float
    available: bool

    class Config:
        from_attributes = True

class QualityRating(BaseModel):
    rating: float
    comment: Optional[str] = None
    
class CropListingUpdate(BaseModel):
    quantity: int
    available: Optional[bool] = True