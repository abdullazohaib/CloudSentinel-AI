"""Tests for Prometheus metrics."""

from prometheus_client import generate_latest

from app.integrations.metrics import (
    record_ai_analysis,
    record_anomaly,
    record_incident,
    record_recovery_action,
    record_recovery_blocked,
    record_recovery_success,
)


def test_incident_metric_exists() -> None:
    """Incident metric should be registered."""

    record_incident()

    output = generate_latest().decode()

    assert "cloudsentinel_incidents_detected_total" in output


def test_anomaly_metric_exists() -> None:
    """Anomaly metric should be registered."""

    record_anomaly()

    output = generate_latest().decode()

    assert "cloudsentinel_anomalies_detected_total" in output


def test_recovery_metrics_exist() -> None:
    """Recovery metrics should be registered."""

    record_recovery_action()
    record_recovery_success()
    record_recovery_blocked()

    output = generate_latest().decode()

    assert "cloudsentinel_recovery_actions_total" in output
    assert "cloudsentinel_recovery_actions_success_total" in output
    assert "cloudsentinel_recovery_actions_blocked_total" in output


def test_ai_metric_exists() -> None:
    """AI analysis metric should be registered."""

    record_ai_analysis()

    output = generate_latest().decode()

    assert "cloudsentinel_ai_analyses_total" in output