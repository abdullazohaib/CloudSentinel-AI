"""Incident-related data models (placeholder). No logic implemented yet."""
"""Incident domain models."""

from datetime import datetime

from pydantic import BaseModel


class Incident(BaseModel):
    """Represents a detected system incident."""

    incident_id: str
    service_name: str
    severity: str
    status: str
    message: str
    timestamp: datetime