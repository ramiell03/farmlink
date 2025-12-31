from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.dependencies import require_roles
from app.db.database import SessionLocal
from sqlalchemy.orm import Session
from app.models.user import User
from typing import List
from app.schemas.user_schema import UserResponse

router = APIRouter(prefix="/admin", tags=["admin Operations"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@router.get("/users", response_model=List[UserResponse])
def list_users(
    current_user=Depends(require_roles(["admin"])),
    db: Session = Depends(get_db)
    ):
    return db.query(User).all()

@router.delete("/user/{user_id}")
def delete_user(
    user_id: int,
    current_user=Depends(require_roles(["admin"])),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.email == current_user["email"]:
        raise HTTPException(
            status_code=403, 
            detail="Admin cannot delete themselves")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

@router.get("/user/id/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id:int,
    current_user=Depends(require_roles(["admin"])),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("/user/email/{email}", response_model=UserResponse)
def get_user_by_email(
    email:str,
    current_user=Depends(require_roles(["admin"])),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("/user/search", response_model=List[UserResponse])
def search_users_by_role(
    role: str = Query(..., description="User role to filter by (admin,farmer,buyer)"),
    current_user=Depends(require_roles(["admin"])),
    db: Session = Depends(get_db)
):
    users = db.query(User).filter(User.role == role).all()
    
    if not users:
        raise HTTPException(
            status_code=404,
            detail=f"No users found with role: '{role}'"
        )
        
    return users
                                   