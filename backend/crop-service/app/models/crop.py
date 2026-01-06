from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base

class Crop(Base):
    __tablename__ = "Crop"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)