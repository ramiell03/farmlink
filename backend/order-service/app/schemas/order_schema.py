from uuid import UUID
from pydantic import BaseModel

class OrderCreate(BaseModel):
    listing_id: UUID
    quantity: int
    total_price: float | None = None
    
class OrderResponse(BaseModel):
    id: UUID
    buyer_id: UUID
    listing_id: UUID
    quantity: int
    total_price: float
    status: str
    
    class Config:
        from_attributes = True