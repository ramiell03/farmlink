from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.schemas.crop_schemas import CropCreate, CropResponse
from app.db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
router = APIRouter(
    prefix="/crops",
    tags=["Crops"]
)

@router.post("/", response_model=CropResponse, status_code=status.HTTP_201_CREATED)
def create_crop(
    payload:CropCreate,
    db: Session = Depends(get_db)
):
  existing = db.query(Crop).filter(Crop.name == payload.name).first()
  if existing:
      raise HTTPException(
          status_code=400,
          detail="Crop already exists"
    )
  crop = Crop(
      name=payload.name,
      description=payload.description
    )
  db.add(crop)
  db.commit()
  db.refresh(crop)
  
  return crop


@router.get("/{crop_id}", response_model=CropResponse)
def get_crop(
    crop_id: int,
    db: Session = Depends(get_db)
):
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    return crop

@router.get("/", response_model=list[CropResponse])
def list_crops(db: Session = Depends(get_db)):
    return db.query(Crop).filter(Crop.is_active == True).all()

@router.delete("/{crop_id}", status_code=204)
def delete_crop(
    crop_id: int,
    db: Session = Depends(get_db)
):
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    crop.is_active = False
    db.commit()
        
    