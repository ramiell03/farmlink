from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

def register_user(db:Session, email:str, password:str, username:str, role:str):
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise ValueError("User already exists")
    
    hashed_pw = hash_password(password)
    
    new_user = User(
        email=email,
        hashed_password=hashed_pw,
        username=username,
        role=role
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, email:str, password:str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None

    token = create_access_token({
        "sub": user.email,
        "role": user.role
    })
    return token