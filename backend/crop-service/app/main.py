from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from app.core.core import Settings
from app.core.crop_trie import crop_trie
from app.db.database import SessionLocal
from app.models import Crop, CropListing
from app.routes.crop_listings import router as crop_listings_router
from app.routes.crop import router as crop_router
from starlette.middleware.cors import CORSMiddleware
from app.core.core import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
   logging.info("Crop Service starting up....")
   
   yield
   
   logging.info("Crop Service shutting down....")
   


app = FastAPI(
   title= "Crop Service",
   description= "Authentication service for Farmlink application",
   version= "1.0.0",
   lifespan=lifespan
)

app.add_middleware(
   CORSMiddleware,
   allow_origins=settings.ALLOWED_ORIGINS,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"]
)

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
        
API_PREFIX = "/api/v1"


app.include_router(crop_router, prefix=API_PREFIX)
app.include_router(crop_listings_router, prefix=API_PREFIX)