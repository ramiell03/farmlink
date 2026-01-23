from fastapi import APIRouter, Depends
from app.schemas.insights import CropRequest
from app.services.analytics_service import market_insights
from app.schemas.analytics import MarketInsightResponse
from app.clients.auth_client import require_roles

router = APIRouter(prefix="/insights", tags=["Insights"])


@router.post("/market", response_model=MarketInsightResponse)
def insights(
    data: CropRequest,
    user=Depends(require_roles(["farmer", "buyer"]))
):
    return market_insights(data.crop)
