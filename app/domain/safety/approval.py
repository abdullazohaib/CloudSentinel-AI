"""Safety approval management."""

from app.domain.safety.rules import SafetyDecision, SafetyRules


class ApprovalManager:
    """Manage approval requirements for recovery actions."""

    def __init__(self) -> None:
        self.rules = SafetyRules()

    def evaluate_action(
        self,
        action: str,
    ) -> SafetyDecision:
        """Evaluate whether an action requires approval."""

        return self.rules.evaluate(action)

    def approve(
        self,
        action: str,
        approved: bool,
    ) -> bool:
        """Return whether the requested action was approved."""

        decision = self.rules.evaluate(action)

        if not approved:
            return False

        if decision.requires_approval:
            return True

        return True