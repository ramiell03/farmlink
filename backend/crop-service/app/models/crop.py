from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db.database import Base

class Crop(Base):
    __tablename__ = "Crop"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now())