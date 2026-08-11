"""Recovery recommendation data models (placeholder). No logic implemented yet."""
"""Recommendation domain models."""

from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    """A recommended action for an incident."""

    action: str
    priority: str
    reason: str


class RecommendationResult(BaseModel):
    """Collection of recommendations for an incident."""

    recommendations: list[Recommendation] = Field(
        default_factory=list
    )