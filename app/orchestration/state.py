"""LangGraph shared state model (placeholder). No logic implemented yet."""
"""Shared state for the incident response LangGraph workflow."""

from typing import TypedDict

from app.domain.incidents.models import Incident
from app.domain.rca.models import RCAResult
from app.domain.recommendation.models import RecommendationResult


class IncidentState(TypedDict, total=False):
    """State passed between incident-response workflow nodes."""

    incident: Incident
    severity: str
    rca: RCAResult
    recommendations: RecommendationResult
    status: str
    error: str | None