# app/schemas/cart_schema.py
from pydantic import BaseModel
from uuid import UUID
from typing import List

class CartItemCreate(BaseModel):
    listing_id: UUID
    quantity: int

class CartItemResponse(BaseModel):
    id: UUID
    buyer_id: UUID
    listing_id: UUID
    quantity: int
    status: str

    class Config:
        orm_mode = True

class CartCheckoutResponse(BaseModel):
    order_ids: List[UUID]
    total_amount: float
