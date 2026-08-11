"""Recovery executor (placeholder). No logic implemented yet."""
"""Safe recovery action executor."""

from app.domain.recovery.models import RecoveryAction, RecoveryResult


class RecoveryExecutor:
    """Execute approved recovery actions safely."""

    SAFE_ACTIONS = {
        "collect_logs",
        "check_health",
        "check_metrics",
        "inspect_configuration",
    }

    def execute(
        self,
        recovery_action: RecoveryAction,
    ) -> RecoveryResult:
        """Execute an approved recovery action."""

        if not recovery_action.approved:
            return RecoveryResult(
                action_id=recovery_action.action_id,
                status="blocked",
                message="Recovery action requires approval.",
            )

        action = recovery_action.action.strip().lower()

        if action not in self.SAFE_ACTIONS:
            return RecoveryResult(
                action_id=recovery_action.action_id,
                status="blocked",
                message=(
                    "Action is not available in the safe "
                    "local recovery executor."
                ),
            )

        return RecoveryResult(
            action_id=recovery_action.action_id,
            status="executed",
            message=f"Safe recovery action executed: {action}",
        )