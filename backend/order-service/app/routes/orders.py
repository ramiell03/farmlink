from datetime import datetime, timedelta
from typing import List
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.order_schema import OrderResponse, OrderCreate
from app.services.order_service import confirm_order_payment, create_order, get_orders_by_crop
from app.db.database import SessionLocal
from app.core.auth_client import require_roles, get_token_from_header
from app.core.crop_client import get_listing_ids_by_farmer
from app.core.core import settings
import httpx
from math import ceil
from fastapi import Query
from app.schemas.common import PaginatedResponse


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
    user=Depends(require_roles(["buyer","admin"]))
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


@router.get("/", response_model=PaginatedResponse[OrderResponse])
def list_orders(
    authorization: str = Header(...),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user=Depends(require_roles(["admin", "farmer", "buyer"]))
):
    token = get_token_from_header(authorization)
    offset = (page - 1) * limit

    query = db.query(Order)

    # 🔐 Role-based filtering
    if user["role"] == "buyer":
        query = query.filter(Order.buyer_id == user["id"])

    elif user["role"] == "farmer":
        listing_ids = get_listing_ids_by_farmer(user["id"], token)
        if not listing_ids:
            return {
                "items": [],
                "total": 0,
                "page": page,
                "limit": limit,
                "pages": 0,
            }
        query = query.filter(Order.listing_id.in_(listing_ids))

    # 📊 Count BEFORE pagination
    total = query.count()
    pages = ceil(total / limit) if total > 0 else 0

    # 📦 Fetch paginated data
    items = (
        query
        .order_by(Order.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": pages,
    }
    
@router.post("/{order_id}/confirm")
def confirm_payment(
    order_id: UUID,
    delivered_quantity: int = Body(..., embed=True),
    authorization: str = Header(...),
    db: Session = Depends(get_db),
    user=Depends(require_roles(["farmer"]))
):
    token = get_token_from_header(authorization)

    return confirm_order_payment(
        db=db,
        order_id=order_id,
        delivered_quantity=delivered_quantity,
        farmer_id=user["id"],
        token=token
    )

@router.get("/admin/stats")
def admin_order_stats(
    db: Session = Depends(get_db),
    user=Depends(require_roles(["admin"]))
):
    orders = db.query(Order).all()

    total_orders = len(orders)
    total_revenue = sum(
        o.total_price for o in orders if o.status == "confirmed"
    )

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue
    }

@router.get("/farmers/{farmer_id}/stats")
def get_farmer_stats(
    farmer_id: UUID,
    authorization: str = Header(...),
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles(["admin", "farmer"]))
):
    token = get_token_from_header(authorization)

    # 🔐 Enforce ownership
    if user["role"] != "admin":
        farmer_id = user["id"]  # override path param

    listing_ids = get_listing_ids_by_farmer(str(farmer_id), token)

    if not listing_ids:
        raise HTTPException(
            status_code=404,
            detail="No listings found for this farmer"
        )

    farmer_orders = db.query(Order).filter(
        Order.listing_id.in_(listing_ids)
    ).all()

    total_orders = len(farmer_orders)
    pending_orders = len(
        [o for o in farmer_orders if o.status in ("pending", "processing")]
    )

    start_of_month = datetime.now().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )

    monthly_sales = sum(
        o.total_price for o in farmer_orders
        if o.status == "confirmed" and o.created_at >= start_of_month
    )

    active_buyers = len(set(
        o.buyer_id for o in farmer_orders
        if o.created_at >= datetime.now() - timedelta(days=30)
    ))

    return {
        "total_crops": len(listing_ids),
        "active_buyers": active_buyers,
        "monthly_sales": monthly_sales,
        "pending_orders": pending_orders,
        "total_orders": total_orders
    }
