"""Severity classification for detected anomalies."""

from app.domain.logs.models import ParsedLog


class SeverityClassifier:
    """Classify the severity of a structured log."""

    def classify(self, log: ParsedLog) -> str:
        """Return a normalized severity level."""

        level = log.level.upper()

        if level == "CRITICAL":
            return "critical"

        if level == "ERROR":
            return "high"

        if level == "WARNING":
            return "medium"

        return "low"