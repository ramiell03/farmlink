from pydantic import BaseModel
from typing import Optional

class CropListingBase(BaseModel):
    crop_id: int
    price: int
    quantity: float
    location: str
    
class CropListingCreate(CropListingBase):
    pass
    
class CropListingResponse(BaseModel):
    id: int
    crop_id: int
    farmer_id: int
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