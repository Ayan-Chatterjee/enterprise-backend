"""Application configuration from environment variables"""
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    app_name: str = "Real Estate Backend"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, validation_alias="DEBUG")
    
    # Server
    host: str = Field(default="0.0.0.0", validation_alias="HOST")
    port: int = Field(default=8000, validation_alias="PORT")
    
    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://user:password@localhost/real_estate",
        validation_alias="DATABASE_URL"
    )
    database_echo: bool = Field(default=False, validation_alias="DATABASE_ECHO")
    
    # JWT
    secret_key: str = Field(default="your-secret-key-change-in-production", validation_alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", validation_alias="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Redis
    redis_url: Optional[str] = Field(default=None, validation_alias="REDIS_URL")
    redis_enabled: bool = Field(default=False, validation_alias="REDIS_ENABLED")
    
    # Logging
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    
    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        validation_alias="CORS_ORIGINS"
    )
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    """Get application settings"""
    return Settings()
