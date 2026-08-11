"""Rule-based Root Cause Analysis engine."""

from app.domain.incidents.models import Incident
from app.domain.rca.models import RCAResult


class RCAEngine:
    """Analyze incidents and determine probable root causes."""

    RULES = {
        "network": {
            "keywords": [
                "network",
                "connection refused",
                "unreachable",
                "timeout",
                "dns",
            ],
            "root_cause": "Network connectivity issue",
            "explanation": (
                "The incident contains network-related evidence, "
                "suggesting a connectivity or communication problem."
            ),
        },
        "database": {
            "keywords": [
                "database",
                "db",
                "sql",
                "query",
                "connection",
            ],
            "root_cause": "Database connectivity or database service issue",
            "explanation": (
                "The incident contains database-related evidence, "
                "suggesting a database connectivity or service problem."
            ),
        },
        "service": {
            "keywords": [
                "crashed",
                "service unavailable",
                "service down",
                "unavailable",
            ],
            "root_cause": "Application service failure",
            "explanation": (
                "The incident indicates that an application service "
                "may have failed or become unavailable."
            ),
        },
    }

    def analyze(self, incident: Incident) -> RCAResult:
        """Determine the most likely root cause."""

        text = (
            f"{incident.service_name} "
            f"{incident.message}"
        ).lower()

        # Network-specific patterns get priority.
        network_rule = self.RULES["network"]

        network_matches = [
            keyword
            for keyword in network_rule["keywords"]
            if keyword in text
        ]

        if network_matches:
            return RCAResult(
                root_cause=network_rule["root_cause"],
                explanation=network_rule["explanation"],
                evidence=network_matches,
                confidence=min(
                    0.60 + (0.10 * len(network_matches)),
                    0.95,
                ),
            )

        # Check database-related patterns.
        database_rule = self.RULES["database"]

        database_matches = [
            keyword
            for keyword in database_rule["keywords"]
            if keyword in text
        ]

        if database_matches:
            return RCAResult(
                root_cause=database_rule["root_cause"],
                explanation=database_rule["explanation"],
                evidence=database_matches,
                confidence=min(
                    0.60 + (0.10 * len(database_matches)),
                    0.95,
                ),
            )

        # Check application service patterns.
        service_rule = self.RULES["service"]

        service_matches = [
            keyword
            for keyword in service_rule["keywords"]
            if keyword in text
        ]

        if service_matches:
            return RCAResult(
                root_cause=service_rule["root_cause"],
                explanation=service_rule["explanation"],
                evidence=service_matches,
                confidence=min(
                    0.60 + (0.10 * len(service_matches)),
                    0.95,
                ),
            )

        return RCAResult(
            root_cause="Unknown",
            explanation=(
                "No known root-cause pattern matched the "
                "available incident information."
            ),
            evidence=[],
            confidence=0.30,
        )