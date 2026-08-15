"""Incident domain models."""

from datetime import datetime

from pydantic import BaseModel, Field


class Incident(BaseModel):
    """Represents a detected system incident."""

    incident_id: str
    service_name: str
    severity: str
    status: str
    message: str
    timestamp: datetime

    logs: list[dict[str, str]] = Field(
        default_factory=list,
        description="Incident log entries.",
    )