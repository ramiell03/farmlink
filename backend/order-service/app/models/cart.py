# app/models/cart.py
from sqlalchemy import Column, String, Integer, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
import enum
from datetime import datetime
from app.db.database import Base


class CartStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    ORDERED = "ORDERED"

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    buyer_id = Column(UUID(as_uuid=True), nullable=False)
    listing_id = Column(UUID(as_uuid=True), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(Enum(CartStatus), default=CartStatus.ACTIVE)
    added_at = Column(DateTime, default=datetime.utcnow)
