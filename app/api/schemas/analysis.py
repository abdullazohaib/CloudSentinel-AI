"""Pydantic schemas for incident analysis API."""

from pydantic import BaseModel, Field


class LogEntry(BaseModel):
    """A single application log entry."""

    timestamp: str = Field(..., description="Timestamp of the log entry")
    level: str = Field(..., description="Log severity level")
    message: str = Field(..., description="Log message")


class AnalysisRequest(BaseModel):
    """Request body for incident analysis."""

    logs: list[LogEntry] = Field(
        ...,
        min_length=1,
        description="Log entries to analyze",
    )
    service_name: str = Field(
        ...,
        min_length=1,
        description="Name of the affected service",
    )


class AnalysisResponse(BaseModel):
    """Response returned by the analysis endpoint."""

    status: str
    incident_id: str
    message: str