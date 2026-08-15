"""Rule-based incident recommendation engine."""

from app.domain.incidents.models import Incident
from app.domain.rca.models import RCAResult
from app.domain.recommendation.models import (
    Recommendation,
    RecommendationResult,
)


class RecommendationEngine:
    """Generate safe recommendations from RCA results."""

    def generate(
        self,
        incident: Incident,
        rca: RCAResult,
    ) -> RecommendationResult:
        """Generate recommendations for an incident."""

        root_cause = rca.root_cause.lower()
        message = incident.message.lower()
        evidence = [
            item.lower()
            for item in rca.evidence
        ]

        recommendations: list[Recommendation] = []

        if "database" in root_cause:
            recommendations.extend(
                [
                    Recommendation(
                        action=(
                            "Check database service health "
                            "and connectivity."
                        ),
                        priority="high",
                        reason=(
                            "The RCA identifies a database-related "
                            "incident."
                        ),
                    ),
                    Recommendation(
                        action=(
                            "Review database connection limits, "
                            "recent errors, and recent deployments."
                        ),
                        priority="medium",
                        reason=(
                            "Connection or configuration changes "
                            "may be contributing to the failure."
                        ),
                    ),
                ]
            )

            if (
                "timeout" in message
                or "timeout" in evidence
            ):
                recommendations.append(
                    Recommendation(
                        action=(
                            "Check database response latency, "
                            "connection pool usage, and timeout settings."
                        ),
                        priority="high",
                        reason=(
                            "Timeout evidence suggests the database "
                            "may be responding too slowly."
                        ),
                    )
                )

        elif "network" in root_cause:
            recommendations.extend(
                [
                    Recommendation(
                        action=(
                            "Check network connectivity between "
                            "the affected services."
                        ),
                        priority="high",
                        reason=(
                            "The RCA indicates a network "
                            "connectivity problem."
                        ),
                    ),
                    Recommendation(
                        action=(
                            "Check DNS resolution and recent "
                            "network configuration changes."
                        ),
                        priority="medium",
                        reason=(
                            "DNS or configuration problems can "
                            "cause service connectivity failures."
                        ),
                    ),
                ]
            )

            if (
                "timeout" in message
                or "timeout" in evidence
            ):
                recommendations.append(
                    Recommendation(
                        action=(
                            "Check network latency, connection "
                            "timeouts, and upstream service health."
                        ),
                        priority="medium",
                        reason=(
                            "Timeout evidence suggests a possible "
                            "communication delay."
                        ),
                    )
                )

        elif "service" in root_cause:
            recommendations.extend(
                [
                    Recommendation(
                        action=(
                            "Check the affected service health "
                            "and recent application logs."
                        ),
                        priority="high",
                        reason=(
                            "The RCA indicates an application "
                            "service failure."
                        ),
                    ),
                    Recommendation(
                        action=(
                            "Review recent deployments and "
                            "configuration changes."
                        ),
                        priority="medium",
                        reason=(
                            "Recent changes may have contributed "
                            "to the service failure."
                        ),
                    ),
                ]
            )

        else:
            recommendations.append(
                Recommendation(
                    action=(
                        "Collect additional logs and system "
                        "metrics before taking corrective action."
                    ),
                    priority="medium",
                    reason=(
                        "The root cause is currently uncertain."
                    ),
                )
            )

        if incident.severity.strip().lower() == "critical":
            recommendations.insert(
                0,
                Recommendation(
                    action=(
                        "Escalate the incident to the "
                        "on-call engineering team."
                    ),
                    priority="critical",
                    reason=(
                        "The incident has critical severity."
                    ),
                ),
            )

        return RecommendationResult(
            recommendations=recommendations
        )