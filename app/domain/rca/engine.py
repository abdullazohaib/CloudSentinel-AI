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
                "connection reset",
                "connection timed out",
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
                "connection timeout",
                "database timeout",
                "deadlock",
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
                "failed",
                "failure",
            ],
            "root_cause": "Application service failure",
            "explanation": (
                "The incident indicates that an application service "
                "may have failed or become unavailable."
            ),
        },
    }

    @staticmethod
    def _get_log_value(log, key: str) -> str:
        """Read a log field from either a dict or an object."""

        if isinstance(log, dict):
            return str(log.get(key, ""))

        return str(getattr(log, key, ""))

    def analyze(self, incident: Incident) -> RCAResult:
        """Determine the most likely root cause."""

        log_text = " ".join(
            f"{self._get_log_value(log, 'level')} "
            f"{self._get_log_value(log, 'message')}"
            for log in getattr(incident, "logs", [])
        )

        text = (
            f"{incident.service_name} "
            f"{incident.message} "
            f"{log_text}"
        ).lower()

        matched_rules: list[tuple[str, list[str]]] = []

        for rule_name, rule in self.RULES.items():
            matches = [
                keyword
                for keyword in rule["keywords"]
                if keyword in text
            ]

            if matches:
                matched_rules.append(
                    (rule_name, matches)
                )

        if matched_rules:
            # If multiple rules match, prefer the most specific
            # database evidence when "database" is explicitly present.
            database_match = next(
                (
                    matches
                    for rule_name, matches in matched_rules
                    if rule_name == "database"
                    and "database" in matches
                ),
                None,
            )

            if database_match is not None:
                best_rule = "database"
                best_matches = database_match
            else:
                best_rule, best_matches = max(
                    matched_rules,
                    key=lambda item: len(item[1]),
                )

            rule = self.RULES[best_rule]

            return RCAResult(
                root_cause=rule["root_cause"],
                explanation=rule["explanation"],
                evidence=best_matches,
                confidence=min(
                    0.60 + (0.10 * len(best_matches)),
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