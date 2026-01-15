from fastapi import FastAPI
from app.routes import routes,admin, farmer, buyer
from app.db.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.database import engine
import logging
from app.core.core import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
   logging.info("Auth Service starting up....")
   
   yield
   
   logging.info("Auth Service shutting down....")
   


app = FastAPI(
   title= "Auth Service",
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

API_PREFIX = "/api/v1"

app.include_router(routes.router, prefix=API_PREFIX)
app.include_router(admin.router, prefix=API_PREFIX)
app.include_router(farmer.router, prefix=API_PREFIX)   
app.include_router(buyer.router, prefix=API_PREFIX)

