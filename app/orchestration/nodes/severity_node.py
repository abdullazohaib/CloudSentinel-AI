"""Severity classification node for the incident-response workflow."""

from app.orchestration.state import IncidentState


VALID_SEVERITIES = {
    "critical",
    "high",
    "medium",
    "low",
}


def severity_node(state: IncidentState) -> IncidentState:
    """Classify and store incident severity."""

    incident = state["incident"]

    supplied_severity = (
        incident.severity.strip().lower()
        if incident.severity
        else ""
    )

    if supplied_severity in VALID_SEVERITIES:
        severity = supplied_severity

    else:
        log_text = " ".join(
            str(
                log.get("message", "")
                if isinstance(log, dict)
                else getattr(log, "message", "")
            )
            for log in getattr(incident, "logs", [])
        ).lower()

        incident_text = (
            f"{incident.service_name} "
            f"{incident.message} "
            f"{log_text}"
        ).lower()

        if any(
            keyword in incident_text
            for keyword in [
                "critical",
                "system down",
                "service down",
                "service unavailable",
                "data loss",
                "security breach",
            ]
        ):
            severity = "critical"

        elif any(
            keyword in incident_text
            for keyword in [
                "database connection timeout",
                "connection refused",
                "timeout",
                "failed",
                "error",
                "unavailable",
            ]
        ):
            severity = "high"

        elif any(
            keyword in incident_text
            for keyword in [
                "warning",
                "slow",
                "latency",
                "retry",
            ]
        ):
            severity = "medium"

        else:
            severity = "low"

    return {
        **state,
        "severity": severity,
        "status": "severity_classified",
    }