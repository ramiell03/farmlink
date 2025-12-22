from fastapi import APIRouter, Depends
from app.core.dependencies import require_roles

router = APIRouter(prefix="/admin", tags=["admin Operations"])

@router.get("/users")
def admin_users(
    user=Depends(require_roles(["admin"]))
):
    return{
        "message": "Admin access granted",
        "user": user
    }