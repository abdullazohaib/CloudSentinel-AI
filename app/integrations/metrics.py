"""Prometheus metrics definitions (placeholder). No logic implemented yet."""
"""Prometheus metrics for CloudSentinel AI."""

from prometheus_client import Counter, Histogram


# Number of incidents detected by the platform.
INCIDENTS_DETECTED = Counter(
    "cloudsentinel_incidents_detected_total",
    "Total number of incidents detected.",
)


# Number of anomalies detected.
ANOMALIES_DETECTED = Counter(
    "cloudsentinel_anomalies_detected_total",
    "Total number of anomalies detected.",
)


# Number of recovery actions attempted.
RECOVERY_ACTIONS = Counter(
    "cloudsentinel_recovery_actions_total",
    "Total number of recovery actions attempted.",
)


# Number of recovery actions successfully executed.
RECOVERY_ACTIONS_SUCCESS = Counter(
    "cloudsentinel_recovery_actions_success_total",
    "Total number of successful recovery actions.",
)


# Number of recovery actions blocked.
RECOVERY_ACTIONS_BLOCKED = Counter(
    "cloudsentinel_recovery_actions_blocked_total",
    "Total number of blocked recovery actions.",
)


# Number of AI analyses performed.
AI_ANALYSES = Counter(
    "cloudsentinel_ai_analyses_total",
    "Total number of AI analyses performed.",
)


# API request latency.
API_REQUEST_LATENCY = Histogram(
    "cloudsentinel_api_request_latency_seconds",
    "API request processing latency in seconds.",
)


def record_incident() -> None:
    """Record a detected incident."""

    INCIDENTS_DETECTED.inc()


def record_anomaly() -> None:
    """Record a detected anomaly."""

    ANOMALIES_DETECTED.inc()


def record_recovery_action() -> None:
    """Record a recovery action."""

    RECOVERY_ACTIONS.inc()


def record_recovery_success() -> None:
    """Record a successful recovery action."""

    RECOVERY_ACTIONS_SUCCESS.inc()


def record_recovery_blocked() -> None:
    """Record a blocked recovery action."""

    RECOVERY_ACTIONS_BLOCKED.inc()


def record_ai_analysis() -> None:
    """Record an AI analysis."""

    AI_ANALYSES.inc()