from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

class Settings(BaseSettings):
    ENV: str = "development"
    SERVICE_NAME: str = "messaging-service"

    AUTH_SERVICE_URL: str
    DATABASE_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str
    ALLOWED_ORIGINS: List[str] = ["*"]

    ANALYTICS_REFRESH_INTERVAL: int = 300  

    class Config:
        env_file = ".env"
        # optional: treat .env as case-insensitive
        case_sensitive = False


settings = Settings()