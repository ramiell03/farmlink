from pydantic import BaseModel
from uuid import UUID
from typing import List

class FarmerRecommendation(BaseModel):
    farmer_id: UUID
    price: float
    quantity: int
    score: float

class NearestFarmersRequest(BaseModel):
    buyer_id: str

class MatchResponse(BaseModel):
    crop: str
    recommendations: List[FarmerRecommendation]
    
class RecommendationsRequest(BaseModel):
    crop: str
    listing_ids: List[UUID]
