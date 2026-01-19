from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.listing_index import listing_index
from app.db.database import SessionLocal
from app.schemas.crop_listing_schema import (CropListingCreate, CropListingResponse, QualityRating)
from app.services.crop_listing_service import create_listing, rate_listing
from app.core.auth_client import require_roles


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
router = APIRouter(prefix="/crop-listings", tags=["Crop Listings"])

@router.get("/search/autocomplete",
            dependencies=[Depends(require_roles(["admin","farmer","buyer"]))])

def autocomplete_crop_listings(
    q: str = Query(..., min_length=1)
):
    return {
        "query": q,
        "suggestions": listing_index.autocomplete(q.lower(), limit=10)
    }

@router.post("/", 
             response_model=CropListingResponse,
             dependencies=[Depends(require_roles(["farmer", "admin"]))])

def create_crop_listing(
    data: CropListingCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles(["farmer", "admin"]))
):
    return create_listing(db, user["id"], data)

@router.post("/{listing_id}/rate",
             dependencies=[Depends(require_roles(["buyer", "admin"]))]
             )
def rate_crop(
    listing_id: int,
    rating: QualityRating,
    db: Session = Depends(get_db),
    user=Depends(require_roles(["buyer", "admin"]))
):
    return rate_listing(db, listing_id, rating.rating)