"""Tests for the incident-response LangGraph workflow."""

from datetime import datetime, timezone

from app.domain.incidents.models import Incident
from app.orchestration.graph import incident_graph


def create_incident(
    message: str = "Database connection failed",
    severity: str = "high",
) -> Incident:
    """Create a test incident."""

    return Incident(
        incident_id="INC-TEST-001",
        service_name="payment-service",
        severity=severity,
        status="open",
        message=message,
        timestamp=datetime.now(timezone.utc),
    )


def test_graph_processes_database_incident() -> None:
    """The complete graph should process a database incident."""

    incident = create_incident()

    result = incident_graph.invoke(
        {
            "incident": incident,
        }
    )

    assert result["severity"] == "high"
    assert "rca" in result
    assert "recommendations" in result
    assert result["status"] == "recommendations_generated"


def test_graph_produces_rca() -> None:
    """The graph should produce a root cause."""

    incident = create_incident(
        message="Database connection failed",
    )

    result = incident_graph.invoke(
        {
            "incident": incident,
        }
    )

    rca = result["rca"]

    assert rca.root_cause
    assert rca.explanation
    assert 0.0 <= rca.confidence <= 1.0


def test_graph_produces_recommendations() -> None:
    """The graph should generate recommendations."""

    incident = create_incident(
        message="Database connection failed",
    )

    result = incident_graph.invoke(
        {
            "incident": incident,
        }
    )

    recommendations = result["recommendations"]

    assert recommendations.recommendations
    assert all(
        recommendation.action
        for recommendation in recommendations.recommendations
    )


def test_graph_handles_network_incident() -> None:
    """The graph should handle network incidents."""

    incident = create_incident(
        message="Network connection timeout",
        severity="high",
    )

    result = incident_graph.invoke(
        {
            "incident": incident,
        }
    )

    assert result["rca"].root_cause == (
        "Network connectivity issue"
    )

    assert result["recommendations"].recommendations


def test_graph_handles_critical_incident() -> None:
    """Critical incidents should produce escalation recommendations."""

    incident = create_incident(
        message="Payment service crashed",
        severity="critical",
    )

    result = incident_graph.invoke(
        {
            "incident": incident,
        }
    )

    recommendations = result["recommendations"].recommendations

    assert recommendations

    assert recommendations[0].priority == "critical"


def test_graph_normalizes_unknown_severity() -> None:
    """Unknown severity values should safely become low."""

    incident = create_incident(
        message="Unknown system event",
        severity="unexpected",
    )

    result = incident_graph.invoke(
        {
            "incident": incident,
        }
    )

    assert result["severity"] == "low"