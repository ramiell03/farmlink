from fastapi import BackgroundTasks
from app.services import aggregation_service
from app.services.analytics_service import ingest_market_price
import logging
from app.services.analytics_service import price_index

logger = logging.getLogger(__name__)


def enqueue_price_update(background_tasks: BackgroundTasks, crop: str, price: float, quantity: int):
    # Record in price_index
    background_tasks.add_task(price_index.add_price, crop, price)
    
    # Record in aggregation service
    background_tasks.add_task(aggregation_service.record_price, crop, price, quantity)

