import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.tasks.scheduler import AnalyticsScheduler

from app.routes.analytics import router as analytics_router
from app.routes.matching import router as matching_router
from app.routes.insights import router as insights_router
from app.routes.health import router as health_router


setup_logging()

app = FastAPI(
    title="Analytics Service",
    description="Market analytics & recommendation engine",
    version="1.0.0",
    docs_url="/docs" if settings.ENV != "production" else None,
    redoc_url="/redoc" if settings.ENV != "production" else None,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



scheduler = AnalyticsScheduler(
    interval=settings.ANALYTICS_REFRESH_INTERVAL
)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(scheduler.start())

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.stop()


app.include_router(analytics_router, prefix="/api/v1")
app.include_router(matching_router, prefix="/api/v1")
app.include_router(insights_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")
