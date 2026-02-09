from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.listing_index import listing_index
from app.db.database import SessionLocal
from app.models.crop import Crop
from app.models.crop_listing import CropListing
from app.schemas.crop_listing_schema import (CropListingCreate, CropListingResponse, CropListingUpdate, QualityRating)
from app.schemas.pagination import PaginatedResponse
from app.services.crop_listing_service import create_listing, rate_listing, update_listing
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

@router.get("/", response_model=PaginatedResponse[CropListingResponse])
def list_crop_listings(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    limit: int | None = Query(None, ge=1, le=100),
    crop_id: UUID | None = Query(None),
    location: str | None = Query(None),
    db: Session = Depends(get_db),
    user=Depends(require_roles(["admin", "farmer", "buyer"]))
):
    # If limit is provided, override page_size
    if limit:
        page_size = limit
        page = 1

    query = db.query(CropListing).filter(CropListing.available == True)

    if crop_id:
        query = query.filter(CropListing.crop_id == crop_id)

    if location:
        query = query.filter(CropListing.location.ilike(f"%{location}%"))

    total = query.count()

    listings = (
        query
        .order_by(CropListing.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": listings
    }
    
@router.get("/{listing_id}",
            response_model=CropListingResponse,
            dependencies=[Depends(require_roles(["admin","farmer","buyer"]))])
def get_crop_listing(
    listing_id: UUID,
    db: Session = Depends(get_db)
):
    listing = (
        db.query(CropListing)
        .filter(
            CropListing.id == listing_id,
            CropListing.available == True
        )
        .first()
    )

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    return listing

@router.get(
    "/by-crop/{crop_name}",
    response_model=list[CropListingResponse],
    dependencies=[Depends(require_roles(["admin", "farmer", "buyer"]))],
)
def get_listings_by_crop_name(
    crop_name: str,
    db: Session = Depends(get_db),
):
    listings = (
        db.query(CropListing)
        .join(Crop, Crop.id == CropListing.crop_id)
        .filter(
            CropListing.available == True,
            Crop.name.ilike(crop_name)
        )
        .all()
    )

    return listings

@router.post("/{listing_id}/rate",
             dependencies=[Depends(require_roles(["buyer", "admin"]))]
             )
def rate_crop(
    listing_id: UUID,
    rating: QualityRating,
    db: Session = Depends(get_db),
    user=Depends(require_roles(["buyer", "admin"]))
):
    return rate_listing(db, listing_id, rating.rating)

@router.get(
    "/by-farmer/{farmer_id}",
    dependencies=[Depends(require_roles(["farmer", "admin"]))]
)
def get_listings_by_farmer(
    farmer_id: UUID,
    db: Session = Depends(get_db)
):
    return (
        db.query(CropListing)
        .filter(CropListing.farmer_id == farmer_id)
        .all()
    )

@router.patch(
    "/{listing_id}",
    response_model=CropListingResponse,
    dependencies=[Depends(require_roles(["farmer"]))]
)
def update_crop_listing(
    listing_id: UUID,
    data: CropListingUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_roles(["farmer"]))
):
    return update_listing(
        db=db,
        listing_id=listing_id,
        quantity=data.quantity,
        farmer_id=user["id"]
    )