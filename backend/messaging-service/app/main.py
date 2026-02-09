from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from app.db.database import SessionLocal
from app.models import messages
from app.routes.communication_ws import router as communication_ws_router
from app.routes.communication import router as communication_router
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
   logging.info("messaging Service starting up....")
   
   yield
   
   logging.info("meassaging Service shutting down....")
   
app = FastAPI(
   title= "messaging Service",
   description= "messaging service for Farmlink application",
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



app.include_router(communication_router, prefix="/api/v1")
app.include_router(communication_ws_router, prefix="/api/v1")