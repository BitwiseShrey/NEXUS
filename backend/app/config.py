"""
NEXUS Configuration Management
Handles application settings, paths, database URLs, and environment variables.
"""

from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "NEXUS"
    APP_ENV: str = "development"
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Base Directory
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    # Database
    DATABASE_URL: str = "sqlite:///./data/nexus.db"

    # Reproducibility
    RANDOM_SEED: int = 42

    # Data directories
    DATA_RAW_DIR: str = "./data/raw"
    DATA_PROCESSED_DIR: str = "./data/processed"
    DATA_SYNTHETIC_DIR: str = "./data/synthetic"
    MODEL_DIR: str = "./models"

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()

# Ensure directories exist
for path_str in [settings.DATA_RAW_DIR, settings.DATA_PROCESSED_DIR, settings.DATA_SYNTHETIC_DIR, settings.MODEL_DIR]:
    Path(path_str).mkdir(parents=True, exist_ok=True)
