"""Root cause analysis data models (placeholder). No logic implemented yet."""
"""Root Cause Analysis domain models."""

from pydantic import BaseModel, Field


class RCAResult(BaseModel):
    """Represents the result of a root cause analysis."""

    root_cause: str
    explanation: str
    evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)