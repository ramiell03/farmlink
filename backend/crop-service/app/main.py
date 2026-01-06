from fastapi import FastAPI
from app.routes.crop import router as crop_router

app = FastAPI(title= "Crop Service")

app.include_router(crop_router)