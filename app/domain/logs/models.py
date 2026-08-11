"""Structured log domain models."""

from datetime import datetime

from pydantic import BaseModel


class ParsedLog(BaseModel):
    """Structured representation of a log entry."""

    timestamp: datetime
    level: str
    message: str