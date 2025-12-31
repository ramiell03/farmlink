from fastapi import APIRouter, Depends
from app.core.dependencies import require_roles

router = APIRouter(prefix="/farmer", tags=["Farmer Operations"])

@router.get("/dashboard")
def farmer_dashboard(
    user=Depends(require_roles(["farmer", "admin"]))
):
    return{
        "message": "Welcome Farmer",
        "user": user
    }