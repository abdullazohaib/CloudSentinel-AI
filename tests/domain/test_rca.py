"""Tests for Root Cause Analysis."""

from datetime import datetime

from app.domain.incidents.models import Incident
from app.domain.rca.engine import RCAEngine


def create_incident(message: str) -> Incident:
    """Create a test incident."""

    return Incident(
        incident_id="INC-TEST123",
        service_name="payment-service",
        severity="high",
        status="open",
        message=message,
        timestamp=datetime(2026, 8, 10, 18, 0, 0),
    )


def test_database_rca() -> None:
    """Database incidents should produce a database RCA."""

    engine = RCAEngine()

    incident = create_incident(
        "Database connection failed",
    )

    result = engine.analyze(incident)

    assert result.root_cause == (
        "Database connectivity or database service issue"
    )
    assert result.confidence >= 0.60
    assert "database" in result.evidence
    assert "connection" in result.evidence


def test_network_rca() -> None:
    """Network incidents should produce a network RCA."""

    engine = RCAEngine()

    incident = create_incident(
        "Network connection timeout",
    )

    result = engine.analyze(incident)

    assert result.root_cause == "Network connectivity issue"
    assert result.confidence >= 0.60
    assert "network" in result.evidence


def test_service_failure_rca() -> None:
    """Service failures should produce a service RCA."""

    engine = RCAEngine()

    incident = create_incident(
        "Payment service crashed",
    )

    result = engine.analyze(incident)

    assert result.root_cause == "Application service failure"
    assert result.confidence >= 0.60
    assert "crashed" in result.evidence


def test_unknown_rca() -> None:
    """Unknown incidents should return an unknown RCA."""

    engine = RCAEngine()

    incident = create_incident(
        "Something unusual happened",
    )

    result = engine.analyze(incident)

    assert result.root_cause == "Unknown"
    assert result.confidence == 0.30
    assert result.evidence == []