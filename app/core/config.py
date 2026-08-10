"""Centralized application configuration."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "AI-Powered Cloud Incident Response & Observability Platform"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    ollama_timeout: int = 60

    # Kubernetes
    kubernetes_enabled: bool = False
    kubernetes_namespace: str = "default"
    kubernetes_config_path: str | None = None

    # Logging
    log_level: str = "INFO"

    # Anomaly detection
    anomaly_error_rate_threshold: float = 0.20
    anomaly_repeated_error_threshold: int = 5

    # Safety
    auto_approve_low_risk: bool = False
    allowed_namespaces: str = "default"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached application settings instance."""
    return Settings()


settings = get_settings()