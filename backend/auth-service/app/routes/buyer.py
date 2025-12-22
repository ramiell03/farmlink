from fastapi import APIRouter, Depends
from app.core.dependencies import require_roles

router = APIRouter(prefix="/buyer", tags=["buyer Operations"])

@router.get("/market")
def buyer_market(
    user=Depends(require_roles(["buyer"]))
):
    return{
        "message": "Buyer market access granted",
        "user": user
    }