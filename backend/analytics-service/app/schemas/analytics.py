from typing import List, Optional
from pydantic import BaseModel

class PredictionResponse(BaseModel):
    crop: str
    predicted_value: float
    confidence: str

    class Config:
        from_attributes = True


class MarketInsightResponse(BaseModel):
    crop: str
    average_price: float
    total_quantity: int
    listings_count: int

    class Config:
        from_attributes = True
        
class PredictionRequest(BaseModel):
    crop: str
    listing_ids: Optional[List[str]] = None
    
class IngestPriceRequest(BaseModel):
    crop: str
    price: float
    quantity: int


class IngestPriceResponse(BaseModel):
    crop: str
    price: float
    status: str
    
class AdminStatsResponse(BaseModel):
    users: int
    listings: int
    orders: int
    revenue: float