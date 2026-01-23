from typing import List
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.order_schema import OrderResponse, OrderCreate
from app.services.order_service import create_order, get_orders_by_crop
from app.db.database import SessionLocal
from app.core.auth_client import require_roles, get_token_from_header
from app.core.core import settings
import httpx

router = APIRouter(prefix="/orders", tags=["orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=OrderResponse)
def place_order(
    data: OrderCreate,
    authorization: str = Header(...), 
    db: Session = Depends(get_db),
    user=Depends(require_roles(["buyer"]))
):
    token = get_token_from_header(authorization)
    return create_order(db, user["id"], data, token)

@router.get("/by-crop/{crop}", response_model=List[OrderResponse])
def orders_by_crop(
    crop: str,
    authorization: str = Header(...),
    db: Session = Depends(get_db),
    user=Depends(require_roles(["admin", "farmer"]))
):
    token = get_token_from_header(authorization)
    return get_orders_by_crop(db, crop, token)