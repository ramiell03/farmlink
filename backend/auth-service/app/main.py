from fastapi import FastAPI
from app.routes import routes
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
   title= "Auth Service",
   description= "Authentication service for Farmlink application",
   version= "1.0.0"
)

app.include_router(routes.router)