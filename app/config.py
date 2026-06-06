"""
Configuration settings for Agent Auth Proxy
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Database
    DATABASE_URL: str

    # Bitwarden
    BW_EMAIL: str
    BW_MASTER_PASSWORD: str
    BW_COLLECTION_ID: str

    # Security
    PROXY_MASTER_SECRET: str
    ADMIN_API_KEY: str

    # Environment
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()