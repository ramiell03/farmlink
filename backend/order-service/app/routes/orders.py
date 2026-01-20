from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.schemas.order_schema import OrderResponse, OrderCreate
from app.services.order_service import create_order
from app.db.database import SessionLocal
from app.core.auth_client import require_roles, get_token_from_header

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
