"""Tests for safety and approval."""

from app.domain.safety.approval import ApprovalManager
from app.domain.safety.rules import SafetyRules


def test_read_only_action_does_not_require_approval() -> None:
    """Read-only diagnostic actions should not require approval."""

    rules = SafetyRules()

    decision = rules.evaluate("check_health")

    assert decision.allowed is True
    assert decision.requires_approval is False


def test_log_collection_is_safe() -> None:
    """Collecting logs should be considered safe."""

    rules = SafetyRules()

    decision = rules.evaluate("collect_logs")

    assert decision.allowed is True
    assert decision.requires_approval is False


def test_state_changing_action_requires_approval() -> None:
    """State-changing actions should require human approval."""

    rules = SafetyRules()

    decision = rules.evaluate("restart_service")

    assert decision.allowed is True
    assert decision.requires_approval is True


def test_unknown_action_requires_approval() -> None:
    """Unknown actions should default to approval."""

    rules = SafetyRules()

    decision = rules.evaluate("unknown_action")

    assert decision.allowed is True
    assert decision.requires_approval is True


def test_approved_action_returns_true() -> None:
    """An approved action should return True."""

    manager = ApprovalManager()

    result = manager.approve(
        "restart_service",
        approved=True,
    )

    assert result is True


def test_rejected_action_returns_false() -> None:
    """A rejected action should return False."""

    manager = ApprovalManager()

    result = manager.approve(
        "restart_service",
        approved=False,
    )

    assert result is False