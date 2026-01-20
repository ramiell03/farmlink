from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.crop import Crop
from app.models.crop_listing import CropListing
from app.core.listing_index import listing_index

def create_listing(db: Session, farmer_id: UUID, data):
    
    crop = db.query(Crop).filter(Crop.id == data.crop_id, Crop.is_active == True).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found or inactive")
    listing = CropListing(
        crop_id=data.crop_id,
        farmer_id=farmer_id,
        price=data.price,
        quantity=data.quantity,
        location=data.location,
        average_quality=0.0,
        rating_count=0,
        available=True
    )
    db.add(listing)
    db.commit()
    db.refresh(listing)

    listing_index.add_listing(crop.name.lower(), listing)
    return listing

def rate_listing(db: Session, listing_id: UUID, rating: float):
    listing = db.query(CropListing).get(listing_id)
    
    total = listing.average_quality * listing.rating_count
    new_average = (total + rating) / (listing.rating_count + 1)

    listing.average_quality = new_average
    listing.rating_count += 1

    db.commit()
    return listing