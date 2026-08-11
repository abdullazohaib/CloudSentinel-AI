"""Tests for recovery and verification."""

from app.domain.recovery.executor import RecoveryExecutor
from app.domain.recovery.models import RecoveryAction
from app.domain.recovery.verification import RecoveryVerifier


def create_action(
    action: str,
    approved: bool = True,
) -> RecoveryAction:
    """Create a test recovery action."""

    return RecoveryAction(
        action_id="ACT-TEST123",
        incident_id="INC-TEST123",
        action=action,
        approved=approved,
    )


def test_approved_safe_action_executes() -> None:
    """Approved safe actions should execute."""

    executor = RecoveryExecutor()

    result = executor.execute(
        create_action("collect_logs")
    )

    assert result.status == "executed"
    assert "collect_logs" in result.message


def test_unapproved_action_is_blocked() -> None:
    """Unapproved actions should be blocked."""

    executor = RecoveryExecutor()

    result = executor.execute(
        create_action(
            "collect_logs",
            approved=False,
        )
    )

    assert result.status == "blocked"
    assert "approval" in result.message.lower()


def test_unsafe_action_is_blocked() -> None:
    """Unsupported state-changing actions should be blocked."""

    executor = RecoveryExecutor()

    result = executor.execute(
        create_action("restart_service")
    )

    assert result.status == "blocked"


def test_health_check_executes() -> None:
    """Health checks should execute when approved."""

    executor = RecoveryExecutor()

    result = executor.execute(
        create_action("check_health")
    )

    assert result.status == "executed"


def test_verification_succeeds() -> None:
    """Successful recovery should pass verification."""

    executor = RecoveryExecutor()
    verifier = RecoveryVerifier()

    result = executor.execute(
        create_action("check_metrics")
    )

    assert verifier.verify(result) is True


def test_verification_fails_for_blocked_action() -> None:
    """Blocked recovery should fail verification."""

    executor = RecoveryExecutor()
    verifier = RecoveryVerifier()

    result = executor.execute(
        create_action(
            "restart_service",
            approved=True,
        )
    )

    assert verifier.verify(result) is False