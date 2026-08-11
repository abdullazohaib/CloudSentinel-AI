"""Recovery verification (placeholder). No logic implemented yet."""
"""Recovery verification."""

from app.domain.recovery.models import RecoveryResult


class RecoveryVerifier:
    """Verify the result of a recovery action."""

    def verify(
        self,
        result: RecoveryResult,
    ) -> bool:
        """Return True when the recovery action succeeded."""

        return result.status == "executed"