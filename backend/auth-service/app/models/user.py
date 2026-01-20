from sqlalchemy import UUID, Column, DateTime,Integer,String, func
from app.db.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False) # e.g., 'farmer', 'buyer', 'admin'
    
    location = Column(String, nullable=True)  
    phone_number = Column(String, nullable=True)
   