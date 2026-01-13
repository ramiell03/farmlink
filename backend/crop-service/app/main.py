from fastapi import FastAPI
from app.core.crop_trie import crop_trie
from app.db.database import SessionLocal
from app.models.crop import Crop
from app.routes.crop import router as crop_router

app = FastAPI(title= "Crop Service")


@app.on_event("startup")
def load_trie_from_db():
    db = SessionLocal()
    try:
        crops = db.query(Crop.name).all()
        for (name,) in crops:
            crop_trie.insert(name)
        print("crop Trie synced from DB")
    finally:
        db.close()

app.include_router(crop_router)