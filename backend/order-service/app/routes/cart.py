from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.services.cart_service import (
    add_to_cart,
    list_cart_items,
    get_cart_item_by_id,  # new function
    remove_cart_item,
    update_cart_item,
    checkout_cart
)
from app.core.auth_client import require_roles, get_token_from_header
from app.schemas.cart_schema import CartItemCreate, CartItemResponse, CartCheckoutResponse
from typing import List

router = APIRouter(prefix="/cart", tags=["Cart"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/items", response_model=CartItemResponse)
def add_item(data: CartItemCreate,
             db: Session = Depends(get_db),
             user=Depends(require_roles(["buyer"]))):
    return add_to_cart(db, user["id"], data.listing_id, data.quantity)


@router.get("/items", response_model=List[CartItemResponse])
def get_items(db: Session = Depends(get_db),
              user=Depends(require_roles(["buyer"]))):
    return list_cart_items(db, user["id"])


# New: Get cart item by ID
@router.get("/items/{cart_item_id}", response_model=CartItemResponse)
def get_item(cart_item_id: str,
             db: Session = Depends(get_db),
             user=Depends(require_roles(["buyer"]))):
    item = get_cart_item_by_id(db, user["id"], cart_item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return item


@router.delete("/items/{cart_item_id}")
def delete_item(cart_item_id: str,
                db: Session = Depends(get_db),
                user=Depends(require_roles(["buyer"]))):
    remove_cart_item(db, user["id"], cart_item_id)
    return {"detail": "Removed"}


@router.patch("/items/{cart_item_id}", response_model=CartItemResponse)
def update_item(cart_item_id: str, quantity: int,
                db: Session = Depends(get_db),
                user=Depends(require_roles(["buyer"]))):
    return update_cart_item(db, user["id"], cart_item_id, quantity)


@router.post("/checkout", response_model=CartCheckoutResponse)
def checkout(db: Session = Depends(get_db),
             authorization: str = Header(...),
             user=Depends(require_roles(["buyer"]))):
    token = get_token_from_header(authorization)
    from app.services.order_service import create_order as create_order_func
    return checkout_cart(db, user["id"], token, create_order_func)
