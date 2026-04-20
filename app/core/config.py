#app/core/config.py
"""
Centralized application configuration.

This module loads environment variables and provides
a strongly-typed settings object used across the app.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # -----------------------------
    # App Settings
    # -----------------------------
    PROJECT_NAME: str = "AuthForge"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # -----------------------------
    # Security Settings
    # -----------------------------
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # -----------------------------
    # Database Settings
    # -----------------------------
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432

    # -----------------------------
    # Redis (optional)
    # -----------------------------
    REDIS_URL: str | None = None

    # -----------------------------
    # Pydantic Config
    # -----------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

    @property
    def database_url(self) -> str:
        """
        Builds the SQLAlchemy database URL.
        """
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()