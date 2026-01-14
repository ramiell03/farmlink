from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.auth_cache import user_cache, role_cache

def register_user(db:Session, email:str, password:str, username:str, role:str, location:str | None = None, phone_number:str | None = None):
    
    if user_cache.get(email):
        raise ValueError("User already exixts")
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise ValueError("User already exists")
    
    if role in ["farmer", "buyer"]:
        if not location:
            raise ValueError("Location is required for farmers and buyers")
        if not phone_number:
            raise ValueError("Phone number is required for farmers and buyers")
    
    if role == "admin":
        location = None
        
    hashed_pw = hash_password(password)
    
    new_user = User(
        email=email,
        hashed_password=hashed_pw,
        username=username,
        role=role,
        location=location,
        phone_number=phone_number
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    user_cache.put(email, new_user)
    role_cache.put(email, role)
    
    return new_user

def authenticate_user(db: Session, email:str, password:str):
    
    user = user_cache.get(email)
    if not user:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        user_cache.put(email, user)
        role_cache.put(email, user.role)

    token = create_access_token({
        "sub": user.email,
        "role": user.role
    })
    return token