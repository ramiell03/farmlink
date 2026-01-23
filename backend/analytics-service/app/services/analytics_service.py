from sqlalchemy.orm import Session
from app.clients.crop_client import get_listing
from app.clients.order_client import get_orders_for_crop
from app.db.database import SessionLocal
from app.models.prediction import Prediction
from app.models.market_snapshot import MarketSnapshot
from app.schemas.insights import MarketSnapshotResponse
from app.services import aggregation_service
from app.storage.market_price_index import MarketPriceIndex
from app.storage.cache import cache_get, cache_set, cache_delete

price_index = MarketPriceIndex()



def ingest_market_price(crop: str, price: float):
    """
    Lightweight event-driven update
    """
    price_index.add_price(crop, price)

    cache_delete(f"prediction:{crop}")
    cache_delete(f"insights:{crop}")


async def recompute_analytics():
    """
    Periodically recompute analytics for all known crops
    """
    db: Session = SessionLocal()

    try:
        for crop, prices in price_index.prices.items():
            if not prices:
                continue

            avg_price = round(sum(prices[-7:]) / len(prices[-7:]), 2)

            snapshot = MarketSnapshot(
                crop=crop,
                average_price=avg_price,
                total_quantity=0,
                listings_count=0
            )

            db.add(snapshot)

            prediction = Prediction(
                crop=crop,
                prediction_type="price_short_term",
                predicted_value=avg_price,
                confidence="medium"
            )

            db.add(prediction)

            cache_delete(f"prediction:{crop}")
            cache_delete(f"insights:{crop}")

        db.commit()

    finally:
        db.close()


def predict_market(crop: str, token: str = None, listing_ids: list = None):
    if token and listing_ids:
        listings = [get_listing(lid, token) for lid in listing_ids]
    
    if token:
        orders = get_orders_for_crop(crop, token)
        if orders:
            print("[Analytics] No orders found or unauthorized")
            prices = [o["total_price"] / max(o["quantity"], 1) for o in orders]
        else:
            prices = price_index.prices.get(crop, [])
    else:
        prices = price_index.prices.get(crop, [])
        
    cache_key = f"prediction:{crop}"
    cached = cache_get(cache_key)
    if cached:
        return cached

    prices = price_index.prices.get(crop, [])
    if not prices:
        predicted_price = 0.0
        confidence = "low"
    else:
        predicted_price = round(sum(prices[-7:]) / len(prices[-7:]), 2)
        confidence = "medium"

    db: Session = SessionLocal()
    prediction = Prediction(
        crop=crop,
        prediction_type="price_short_term",
        predicted_value=predicted_price,
        confidence=confidence
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    db.close()

    cache_set(cache_key, serialize_prediction(prediction))

    return prediction

def serialize_prediction(pred):
    return {
        "id": str(pred.id),
        "crop": pred.crop,
        "prediction_type": pred.prediction_type,
        "predicted_value": pred.predicted_value,
        "confidence": pred.confidence,
        "created_at": pred.created_at.isoformat() if pred.created_at else None,
    }


def market_insights(crop: str):
    cache_key = f"insights:{crop}"
    cached = cache_get(cache_key)
    if cached:
        return cached

    avg_price = aggregation_service.average_price(crop)
    total_quantity = aggregation_service.total_quantity(crop)
    listings_count = aggregation_service.listings_count(crop)

    snapshot = MarketSnapshot(
        crop=crop,
        average_price=avg_price,
        total_quantity=total_quantity,
        listings_count=listings_count
    )

    snapshot_schema = MarketSnapshotResponse.model_validate(snapshot)
    cache_set(cache_key, snapshot_schema.model_dump(mode="json"))
    return snapshot_schema

