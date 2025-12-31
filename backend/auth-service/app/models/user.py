from sqlalchemy import Column,Integer,String
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False) # e.g., 'farmer', 'buyer', 'admin'
    
    location = Column(String, nullable=True)  
    phone_number = Column(String, nullable=True)