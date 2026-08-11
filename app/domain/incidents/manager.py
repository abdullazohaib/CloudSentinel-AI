"""Incident lifecycle manager (placeholder). No logic implemented yet."""
"""Incident management."""

from uuid import uuid4

from app.domain.anomaly.severity import SeverityClassifier
from app.domain.incidents.models import Incident
from app.domain.logs.models import ParsedLog


class IncidentManager:
    """Create incidents from detected anomalies."""

    def __init__(self) -> None:
        self.severity_classifier = SeverityClassifier()

    def create_incident(
        self,
        log: ParsedLog,
        service_name: str,
    ) -> Incident:
        """Create an incident from an anomalous log."""

        severity = self.severity_classifier.classify(log)

        return Incident(
            incident_id=f"INC-{uuid4().hex[:8].upper()}",
            service_name=service_name,
            severity=severity,
            status="open",
            message=log.message,
            timestamp=log.timestamp,
        )