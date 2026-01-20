from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserLogin, UserUpdateSelf, PasswordChange, EmailChangeRequest, EmailConfirm
from app.services.auth_service import register_user, authenticate_user, verify_password, hash_password
from app.db.database import SessionLocal
from app.core.config import SECRET_KEY, JWT_ALGORITHM
from jose import jwt
from datetime import timedelta
from app.models.user import User
from app.core.dependencies import require_roles
from app.core.security import create_access_token, decode_token

router = APIRouter(prefix="/auth",tags=["Authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return register_user(db, user.email, user.password,user.username, user.role, user.location, user.phone_number)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login")
def login(user: UserLogin, db:Session = Depends(get_db)):
    token = authenticate_user(db, user.email, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    role = payload.get("role")
    refresh_token = create_access_token(
        {"sub": user.email, "role": role})

    return {"access_token": token, "token_type": "bearer", "role": role, "refresh-token": refresh_token}

@router.get("/profile")
def user_profile(
    db: Session = Depends(get_db),
    token_data=Depends(require_roles(["farmer", "buyer", "admin"]))
):
    user = db.query(User).filter(User.email == token_data["email"]).first()
    return{
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "username": user.username
    }
    
@router.post("/refresh-token")
def refresh_token(refresh_token:str):
    payload = decode_token(refresh_token)
    
    new_token = create_access_token({
        "sub": payload["sub"],
        "role": payload["role"]
    })
    
    return {"access_token": new_token}

@router.put("/me")
def update_my_profile(
    payload: UserUpdateSelf,
    current_user=Depends(require_roles(["farmer", "buyer", "admin"])),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == current_user["email"]).first()
    
    if payload.username:
        user.username = payload.username
    if payload.location:
        user.location = payload.location
    if payload.phone_number:
        user.phone_number = payload.phone_number
        
    db.commit()
    db.refresh(user)
    return user
    
@router.put("/me/password")
def change_password(
    payload: PasswordChange,
    current_user=Depends(require_roles(["farmer","buyer","admin"])),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == current_user["email"]).first()
    
    if not verify_password(payload.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="current password is incorrect")
    
    user.hashed_password = hash_password(payload.new_password)
    db.commit()
    
    return {"message": "Password updated sucessfully"}

@router.post("/me/email/request")
def request_email_change(
    payload: EmailChangeRequest,
    current_user=Depends(require_roles(["farmer", "buyer", "admin"])),
    db: Session = Depends(get_db)
):
    token = create_access_token(
        {"sub": current_user["email"], "new_email": payload.new_email},
        expires_delta=timedelta(minutes=15)
    )
    
    print("Email verification token:",token)
    
    return {"message": "verification email sent"}

@router.post("/me/email/confirm")
def confirm_email_change(
    payload: EmailConfirm,
    db: Session = Depends(get_db)
):
    data = decode_token(payload.token)
    
    user = db.query(User).filter(User.email == data["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.email = data["new_email"]
    db.commit()
    
    return {"massage": "Email updated sucessfully"}
    
    