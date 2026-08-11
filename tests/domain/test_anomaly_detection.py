"""Tests for anomaly detection and incident creation."""

from datetime import datetime

from app.domain.anomaly.detector import AnomalyDetector
from app.domain.incidents.manager import IncidentManager
from app.domain.logs.models import ParsedLog


def create_log(level: str, message: str) -> ParsedLog:
    """Create a test log."""

    return ParsedLog(
        timestamp=datetime(2026, 8, 10, 18, 0, 0),
        level=level,
        message=message,
    )


def test_error_log_is_anomaly() -> None:
    """ERROR logs should be detected as anomalies."""

    detector = AnomalyDetector()

    log = create_log(
        "ERROR",
        "Database connection failed",
    )

    assert detector.is_anomaly(log) is True


def test_critical_log_is_anomaly() -> None:
    """CRITICAL logs should be detected as anomalies."""

    detector = AnomalyDetector()

    log = create_log(
        "CRITICAL",
        "Service crashed",
    )

    assert detector.is_anomaly(log) is True


def test_timeout_is_anomaly() -> None:
    """Timeout messages should be detected as anomalies."""

    detector = AnomalyDetector()

    log = create_log(
        "INFO",
        "Database request timeout",
    )

    assert detector.is_anomaly(log) is True


def test_normal_log_is_not_anomaly() -> None:
    """Normal informational logs should not be anomalies."""

    detector = AnomalyDetector()

    log = create_log(
        "INFO",
        "Application started successfully",
    )

    assert detector.is_anomaly(log) is False


def test_incident_creation() -> None:
    """An anomalous log should create an open incident."""

    manager = IncidentManager()

    log = create_log(
        "ERROR",
        "Database connection failed",
    )

    incident = manager.create_incident(
        log,
        "payment-service",
    )

    assert incident.incident_id.startswith("INC-")
    assert incident.service_name == "payment-service"
    assert incident.severity == "high"
    assert incident.status == "open"
    assert incident.message == "Database connection failed"


def test_critical_incident_severity() -> None:
    """CRITICAL logs should create critical incidents."""

    manager = IncidentManager()

    log = create_log(
        "CRITICAL",
        "Service crashed",
    )

    incident = manager.create_incident(
        log,
        "payment-service",
    )

    assert incident.severity == "critical"