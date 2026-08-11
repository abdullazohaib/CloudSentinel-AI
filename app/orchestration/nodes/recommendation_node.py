"""LangGraph recovery recommendation node (placeholder). No logic implemented yet."""
"""Recommendation node for the incident-response workflow."""

from app.domain.recommendation.engine import RecommendationEngine
from app.orchestration.state import IncidentState


def recommendation_node(state: IncidentState) -> IncidentState:
    """Generate recommendations from the incident RCA."""

    incident = state["incident"]
    rca = state["rca"]

    engine = RecommendationEngine()

    recommendations = engine.generate(
        incident,
        rca,
    )

    return {
        **state,
        "recommendations": recommendations,
        "status": "recommendations_generated",
    }