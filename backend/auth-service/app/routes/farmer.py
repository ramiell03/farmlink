from fastapi import APIRouter, Depends
from app.core.dependencies import require_roles

router = APIRouter(prefix="/farmer", tags=["Farmer Operations"])

@router.get("/dashboard")
def farmer_dashborad(
    user=Depends(require_roles(["farmer"]))
):
    return{
        "message": "Welcome Farmer",
        "user": user
    }