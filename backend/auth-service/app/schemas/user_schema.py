from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str
    role: str  # e.g., 'farmer', 'buyer', 'admin'
    location: Optional[str] = None
    phone_number: Optional[str] = None
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: str
    location: Optional[str] = None
    phone_number: Optional[str] = None
    
class UserUpdateSelf(BaseModel):
    username:   Optional[str]
    location: Optional[str]
    phone_number:Optional[str]
    
class UserUpdateAdmin(BaseModel):
    role:str
    
class PasswordChange(BaseModel):
    current_password:str
    new_password:str
    
class EmailChangeRequest(BaseModel):
    new_email: str
    
class EmailConfirm(BaseModel):
    token: str