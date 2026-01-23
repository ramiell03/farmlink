import uuid
from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.database import Base


class MarketSnapshot(Base):
    __tablename__ = "market_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crop = Column(String, index=True, nullable=False)

    average_price = Column(Float, nullable=False)
    total_quantity = Column(Integer, nullable=False)
    listings_count = Column(Integer, nullable=False)

    created_at = Column(DateTime, server_default=func.now(), index=True)
