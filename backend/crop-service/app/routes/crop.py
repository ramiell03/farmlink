from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import Query, FastAPI

from app.models.crop import Crop
from app.schemas.crop_schemas import CropCreate, CropResponse
from app.db.database import SessionLocal
from app.core.crop_trie import crop_trie


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

@router.get("/search/autocomplete")
def autocomplete_crops(
    q: str = Query(..., min_length=1, description="crop name prefix")
    
):
    suggestions = crop_trie.autocomplete(q)
    
    return{
        "query": q,
        "suggestions": suggestions
    }

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
  crop_trie.insert(crop.name)
  
  return crop


@router.get("/{crop_id}", response_model=CropResponse)
def get_crop(
    crop_id: int,
    db: Session = Depends(get_db)
):
    crop = db.query(Crop).filter(Crop.id == crop_id, crop.is_active == True).first()
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
    
    crop_trie.delete(crop.name)
    db.commit()
    
    return {"message": "Deleted"}
    
@router.put("/{crop_id}", response_model=CropResponse)
def update_crop(
    crop_id: int,
    payload: CropCreate,
    db: Session = Depends(get_db)
):
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    crop_trie.delete(crop.name)
    
    crop.name = payload.name
    crop.description = payload.description
    
    db.commit()
    db.refresh(crop)
    
    crop_trie.insert(crop.name)
    return crop




@router.patch("/{crop_id}/restore", response_model=CropResponse)
def restore_crop(crop_id:int, db:Session = Depends(get_db)):
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    
    if not crop:
        raise HTTPException(status_code=404, detail="crop not found")
    
    crop.is_active = True
    db.commit()
    db.refresh(crop)
    
    crop_trie.insert(crop.name)
    
    return crop
    


        
    