from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    ENV: str = "development"

    # Database
    DATABASE_URL: str

    # Service-to-service communication
    AUTH_SERVICE_URL: str
    LISTING_SERVICE_URL: str

    ALLOWED_ORIGINS: List[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="forbid"
    )

settings = Settings()
