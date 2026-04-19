"""
Centralized application configuration.

This module loads environment variables and provides
a strongly-typed settings object used across the app.
"""

from functools import lru_cache
from pydantic import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application Settings loaded from environment variables.
    """

    #AppSettings
    projectName: str = "AuthForge"
    apiV1Str: str = "/api/v1"
    debug: bool = True

    #Security Settings
    secretKey: str
    algorithm: str = "HS256"
    accessTokenExpireMinutes: int = 30
    refreshTokenExpireDays: int = 7

    #Database Settings
    postgresServer:str
    postgresUser: str
    postgresPassword: str
    postgresDB: str
    postgresPort: int = 5432

    #Redis
    redisUrl: str | None = None

    #Pydantic Config

    modelConfig = SettingsConfigDict(
        envFile=".env",
        caseSensitive=True
    )

    @property
    def databaseUrl(self) -> str:
        """
        Builds the SQLAchemy database URL
        """
        return (
            f"postgresql://{self.postgresUser}:{self.postgresPassword}"
            f"@{self.postgresServer}:{self.postgresPort}/{self.postgresDB}"
        )

#Cached Settings Instance
@lru_cache
def getSettings() -> Settings:
    """
    Returns a cached instance of the settings.
    Prevents reloading environment variables multiple times.
    """
    return Settings()

#Global settings object
settings = getSettings()