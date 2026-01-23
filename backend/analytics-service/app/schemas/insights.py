from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class MarketInsightResponse(BaseModel):
    crop: str
    average_price: float
    total_quantity: int
    listings_count: int


class CropRequest(BaseModel):
    crop: str
    

class MarketSnapshotResponse(BaseModel):
    id: UUID
    crop: str
    average_price: float
    total_quantity: int
    listings_count: int
    created_at: datetime

    class Config:
        from_attributes = True  
