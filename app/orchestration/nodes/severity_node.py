"""LangGraph severity assessment node (placeholder). No logic implemented yet."""
"""Severity classification node for the incident-response workflow."""

from app.orchestration.state import IncidentState


def severity_node(state: IncidentState) -> IncidentState:
    """Normalize and store the incident severity."""

    incident = state["incident"]

    severity = incident.severity.strip().lower()

    if severity not in {
        "critical",
        "high",
        "medium",
        "low",
    }:
        severity = "low"

    return {
        **state,
        "severity": severity,
        "status": "severity_classified",
    }