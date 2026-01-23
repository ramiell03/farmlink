import uuid
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crop = Column(String, index=True, nullable=False)

    prediction_type = Column(String, nullable=False)
    predicted_value = Column(Float, nullable=False)
    confidence = Column(String, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), index=True)
