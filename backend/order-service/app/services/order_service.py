from uuid import UUID, uuid4
from fastapi import HTTPException
import requests
from sqlalchemy.orm import Session
from app.core.crop_client import get_listing_by_id, get_listing_ids_by_crop, get_listing_price, update_listing_quantity
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
    
def confirm_order_payment(
    db: Session,
    order_id: UUID,
    delivered_quantity: int,
    farmer_id: str,
    token: str
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail="Order already processed")

    # fetch listing
    listing = get_listing_by_id(order.listing_id, token)

    # security: only listing owner
    if listing["farmer_id"] != farmer_id:
        raise HTTPException(status_code=403, detail="Not your listing")

    if delivered_quantity > listing["quantity"]:
        raise HTTPException(status_code=400, detail="Not enough stock")

    # update listing quantity
    remaining_qty = listing["quantity"] - delivered_quantity

    update_listing_quantity(
        listing_id=order.listing_id,
        quantity=remaining_qty,
        available=remaining_qty > 0,
        token=token
    )

    # update order
    order.status = OrderStatus.CONFIRMED
    order.total_price = delivered_quantity * listing["price"]

    db.commit()
    db.refresh(order)

    return order
