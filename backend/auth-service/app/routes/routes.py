from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserLogin, Token
from app.services.auth_service import register_user, authenticate_user
from app.db.database import SessionLocal
from app.core.config import SECRET_KEY, JWT_ALGORITHM
from jose import jwt
from app.core.dependencies import require_roles
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
        return register_user(db, user.email, user.password,user.username, user.role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login")
def login(user: UserLogin, db:Session = Depends(get_db)):
    token = authenticate_user(db, user.email, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    role = payload.get("role")
    return {"access_token": token, "token_type": "bearer", "role": role}

@router.get("/profile")
def user_profile(
    user=Depends(require_roles(["farmer", "buyer", "admin"]))
):
    return{
        "email": user["email"],
        "role": user["role"],
        "username": user["username"]
    }