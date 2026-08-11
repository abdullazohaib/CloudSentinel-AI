"""Tests for the recommendation engine."""

from datetime import datetime

from app.domain.incidents.models import Incident
from app.domain.rca.models import RCAResult
from app.domain.recommendation.engine import RecommendationEngine


def create_incident(
    message: str = "Database connection failed",
    severity: str = "high",
) -> Incident:
    """Create a test incident."""

    return Incident(
        incident_id="INC-REC123",
        service_name="payment-service",
        severity=severity,
        status="open",
        message=message,
        timestamp=datetime(2026, 8, 10, 18, 0, 0),
    )


def create_rca(root_cause: str) -> RCAResult:
    """Create a test RCA result."""

    return RCAResult(
        root_cause=root_cause,
        explanation="Test RCA explanation.",
        evidence=["test"],
        confidence=0.8,
    )


def test_database_recommendations() -> None:
    """Database RCA should produce database recommendations."""

    engine = RecommendationEngine()

    result = engine.generate(
        create_incident(),
        create_rca(
            "Database connectivity or database service issue"
        ),
    )

    assert len(result.recommendations) >= 2

    assert any(
        "database service health" in item.action.lower()
        for item in result.recommendations
    )


def test_network_recommendations() -> None:
    """Network RCA should produce network recommendations."""

    engine = RecommendationEngine()

    result = engine.generate(
        create_incident(
            message="Network connection timeout"
        ),
        create_rca("Network connectivity issue"),
    )

    assert any(
        "network connectivity" in item.action.lower()
        for item in result.recommendations
    )


def test_service_recommendations() -> None:
    """Service RCA should produce service recommendations."""

    engine = RecommendationEngine()

    result = engine.generate(
        create_incident(
            message="Payment service crashed"
        ),
        create_rca("Application service failure"),
    )

    assert any(
        "service health" in item.action.lower()
        for item in result.recommendations
    )


def test_unknown_rca_recommendation() -> None:
    """Unknown RCA should request additional investigation."""

    engine = RecommendationEngine()

    result = engine.generate(
        create_incident(
            message="Something unusual happened"
        ),
        create_rca("Unknown"),
    )

    assert len(result.recommendations) == 1
    assert "additional logs" in (
        result.recommendations[0].action.lower()
    )


def test_critical_incident_escalation() -> None:
    """Critical incidents should receive escalation advice."""

    engine = RecommendationEngine()

    result = engine.generate(
        create_incident(
            severity="critical"
        ),
        create_rca(
            "Database connectivity or database service issue"
        ),
    )

    assert result.recommendations[0].priority == "critical"
    assert "escalate" in (
        result.recommendations[0].action.lower()
    )