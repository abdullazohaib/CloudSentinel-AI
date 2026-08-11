"""Tests for AI-assisted RCA."""

from datetime import datetime

from app.domain.incidents.models import Incident
from app.domain.rca.ai_engine import AIRCAEngine
from app.domain.rca.models import RCAResult


class FakeOllamaClient:
    """Fake Ollama client for testing."""

    def generate(self, prompt: str) -> str:
        """Return a deterministic fake AI response."""

        return (
            "The database connection failure is the probable "
            "root cause. Engineers should investigate database "
            "availability, connection limits, and recent changes."
        )


class EmptyOllamaClient:
    """Fake Ollama client that returns no response."""

    def generate(self, prompt: str) -> str:
        """Return an empty response."""

        return ""


def create_incident() -> Incident:
    """Create a test incident."""

    return Incident(
        incident_id="INC-AI123",
        service_name="payment-service",
        severity="high",
        status="open",
        message="Database connection failed",
        timestamp=datetime(2026, 8, 10, 18, 0, 0),
    )


def create_base_rca() -> RCAResult:
    """Create a base RCA result."""

    return RCAResult(
        root_cause=(
            "Database connectivity or database service issue"
        ),
        explanation="Database evidence was detected.",
        evidence=["database", "connection"],
        confidence=0.8,
    )


def test_ai_rca_enhances_explanation() -> None:
    """AI RCA should replace the explanation with AI analysis."""

    engine = AIRCAEngine(
        ollama_client=FakeOllamaClient(),
    )

    result = engine.analyze(
        create_incident(),
        create_base_rca(),
    )

    assert result.root_cause == (
        "Database connectivity or database service issue"
    )

    assert "probable root cause" in result.explanation
    assert result.evidence == ["database", "connection"]
    assert result.confidence == 0.8


def test_ai_rca_falls_back_when_ai_returns_empty() -> None:
    """Base RCA should remain when AI gives no response."""

    base_rca = create_base_rca()

    engine = AIRCAEngine(
        ollama_client=EmptyOllamaClient(),
    )

    result = engine.analyze(
        create_incident(),
        base_rca,
    )

    assert result == base_rca