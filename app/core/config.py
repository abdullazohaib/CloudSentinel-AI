"""Centralized application configuration."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(
        default="CloudSentinel AI",
        description="Application name",
    )

    app_version: str = Field(
        default="1.0.0",
        description="Application version",
    )

    environment: str = Field(
        default="development",
        description="Application environment",
    )

    # API
    api_host: str = Field(
        default="0.0.0.0",
        description="API host",
    )

    api_port: int = Field(
        default=8000,
        description="API port",
    )

    # Ollama
    ollama_host: str = Field(
        default="http://localhost:11434",
        description="Ollama server URL",
    )

    ollama_model: str = Field(
        default="llama3.2",
        description="Ollama model name",
    )

    # Logging
    log_level: str = Field(
        default="INFO",
        description="Application log level",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached application settings instance."""

    return Settings()


settings = get_settings()