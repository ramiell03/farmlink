import uuid
from sqlalchemy import UUID, Column, Integer, String,Float, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.database import Base
from sqlalchemy.orm import relationship
import uuid


class CropListing(Base):
    __tablename__ = "marketplace"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)   
    crop_id = Column(UUID(as_uuid=True), ForeignKey("crops.id"), nullable=False)
    farmer_id = Column(UUID(as_uuid=True), nullable=False)
    
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    
    average_quality = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    
    available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    crop = relationship("Crop", back_populates="listings")