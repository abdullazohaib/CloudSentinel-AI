"""Safety rules for recovery actions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyDecision:
    """Result of evaluating an action."""

    allowed: bool
    requires_approval: bool
    reason: str


class SafetyRules:
    """Evaluate whether an action requires human approval."""

    SAFE_ACTIONS = {
        "collect_logs",
        "check_health",
        "check_metrics",
        "inspect_configuration",
    }

    def evaluate(self, action: str) -> SafetyDecision:
        """Evaluate an action against safety rules."""

        normalized_action = action.strip().lower()

        if normalized_action in self.SAFE_ACTIONS:
            return SafetyDecision(
                allowed=True,
                requires_approval=False,
                reason="Read-only diagnostic action.",
            )

        return SafetyDecision(
            allowed=True,
            requires_approval=True,
            reason=(
                "The action may modify system state and "
                "requires human approval."
            ),
        )