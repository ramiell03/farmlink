from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL")
LISTING_SERVICE_URL = os.getenv("LISTING_SERVICE_URL")
DATABASE_URL = os.getenv("DATABASE_URL")


class Settings(BaseSettings):
    ENV: str = "development"
    SERVICE_NAME: str = "analytics-service"

    LISTING_SERVICE_URL: str
    AUTH_SERVICE_URL: str
    ORDER_SERVICE_URL: str
    DATABASE_URL: str

    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    ALLOWED_ORIGINS: List[str] = ["*"]

    ANALYTICS_REFRESH_INTERVAL: int = 300  

    class Config:
        env_file = ".env"
        # optional: treat .env as case-insensitive
        case_sensitive = False


settings = Settings()