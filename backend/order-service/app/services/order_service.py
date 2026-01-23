from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from app.core.crop_client import get_listing_ids_by_crop, get_listing_price
from app.models.order import Order
from app.enums.order_status import OrderStatus
from app.core.order_queue import order_queue

def create_order(db: Session, buyer_id: UUID, data, token: str):
    listing_price = get_listing_price(data.listing_id, token)
    total_price = listing_price * data.quantity

    order = Order(
        id=uuid4(),
        buyer_id=buyer_id,
        listing_id=data.listing_id,
        quantity=data.quantity,
        total_price=total_price,
        status=OrderStatus.PENDING
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    order_queue.add(order)
    
    
    return order

def get_orders_by_crop(db: Session, crop: str, token: str):
    listing_ids = get_listing_ids_by_crop(crop, token)

    if not listing_ids:
        return []

    return (
        db.query(Order)
        .filter(Order.listing_id.in_(listing_ids))
        .all()
    )
