from typing import List
from fastapi import APIRouter, Depends, BackgroundTasks, Header
from requests import Session
from app.clients.crop_client import get_total_listings
from app.clients.order_client import get_orders_admin
from app.db.database import SessionLocal
from app.schemas.analytics import AdminStatsResponse, IngestPriceRequest, IngestPriceResponse, PredictionRequest, PredictionResponse
from app.services.analytics_service import predict_market
from app.clients.auth_client import get_token_from_header, get_total_users, require_roles
from app.tasks.workers import enqueue_price_update

router = APIRouter(prefix="/analytics", tags=["Analytics"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/predict", response_model=PredictionResponse)
def predict(
    data: PredictionRequest,
    authorization: str = Header(...),
    db: Session = Depends(get_db),
    user=Depends(require_roles(["farmer", "buyer", "admin"])),
    
):
    token = get_token_from_header(authorization)
    return predict_market(data.crop, token=token, listing_ids=data.listing_ids)

@router.post("/ingest-price", response_model=IngestPriceResponse)
def ingest_price(
    data: IngestPriceRequest,
    background_tasks: BackgroundTasks
):
    enqueue_price_update(
        background_tasks,
        data.crop,
        data.price,
        data.quantity
    )
    return {
        "crop": data.crop,
        "price": data.price,
        "quantity": data.quantity,
        "status": "queued"
    }

@router.get("/stats", response_model=AdminStatsResponse)
def admin_stats(
    authorization: str = Header(...),
    user=Depends(require_roles(["admin"])),

):
    token = get_token_from_header(authorization)

    users = get_total_users(token)
    listings = get_total_listings(token)
    orders_data = get_orders_admin(token)

    return {
        "users": users,
        "listings": listings,
        "orders": orders_data["total_orders"],      
        "revenue": orders_data["total_revenue"],    
    }
