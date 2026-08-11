"""Anomaly detection engine (placeholder). No logic implemented yet."""
"""Rule-based anomaly detection."""

from app.domain.logs.models import ParsedLog


class AnomalyDetector:
    """Detect anomalies from structured logs."""

    ANOMALY_LEVELS = {"ERROR", "CRITICAL"}

    ANOMALY_KEYWORDS = {
        "failed",
        "failure",
        "timeout",
        "exception",
        "unavailable",
        "connection refused",
        "crashed",
    }

    def is_anomaly(self, log: ParsedLog) -> bool:
        """Return True when a log represents an anomaly."""

        if log.level.upper() in self.ANOMALY_LEVELS:
            return True

        message = log.message.lower()

        return any(
            keyword in message
            for keyword in self.ANOMALY_KEYWORDS
        )