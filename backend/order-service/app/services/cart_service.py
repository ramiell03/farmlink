from sqlalchemy.orm import Session
from app.models.cart import CartItem, CartStatus
from app.core.crop_client import get_listing_price  # reuse crop listing price
from fastapi import HTTPException

def add_to_cart(db: Session, buyer_id, listing_id, quantity):
    existing = db.query(CartItem).filter(
        CartItem.buyer_id == buyer_id,
        CartItem.listing_id == listing_id,
        CartItem.status == CartStatus.ACTIVE
    ).first()
    if existing:
        existing.quantity += quantity
        db.commit()
        db.refresh(existing)
        return existing

    item = CartItem(
        buyer_id=buyer_id,
        listing_id=listing_id,
        quantity=quantity
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def list_cart_items(db: Session, buyer_id):
    return db.query(CartItem).filter(
        CartItem.buyer_id == buyer_id,
        CartItem.status == CartStatus.ACTIVE
    ).all()

# New function to get a cart item by ID
def get_cart_item_by_id(db: Session, buyer_id, cart_item_id):
    return db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.buyer_id == buyer_id,
        CartItem.status == CartStatus.ACTIVE
    ).first()

def remove_cart_item(db: Session, buyer_id, cart_item_id):
    item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.buyer_id == buyer_id,
        CartItem.status == CartStatus.ACTIVE
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()

def update_cart_item(db: Session, buyer_id, cart_item_id, quantity):
    item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.buyer_id == buyer_id,
        CartItem.status == CartStatus.ACTIVE
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    item.quantity = quantity
    db.commit()
    db.refresh(item)
    return item

def checkout_cart(db: Session, buyer_id, token, create_order_func):
    items = list_cart_items(db, buyer_id)
    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    order_ids = []
    total_amount = 0

    for item in items:
        price = get_listing_price(item.listing_id, token)
        total_amount += price * item.quantity

        order = create_order_func(db, buyer_id, item, token)
        order_ids.append(order.id)

        item.status = CartStatus.ORDERED

    db.commit()
    return {"order_ids": order_ids, "total_amount": total_amount}
