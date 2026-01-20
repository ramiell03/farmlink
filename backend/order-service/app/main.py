from fastapi import FastAPI
from app.db.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.database import engine
import logging
from app.core.core import settings
from app.models.order import Order
from app.models.cart import CartItem
from app.routes.orders import router as order_router
from app.routes.cart import router as cart_router


@asynccontextmanager
async def lifespan(app: FastAPI):
   logging.info("Order Service starting up....")
   
   yield

   logging.info("Order Service shutting down....")



app = FastAPI(
   title= "Order Service",
   description= "Order service for Farmlink application",
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

API_PREFIX = "/api/v3"

app.include_router(order_router, prefix=API_PREFIX)
app.include_router(cart_router, prefix=API_PREFIX)


