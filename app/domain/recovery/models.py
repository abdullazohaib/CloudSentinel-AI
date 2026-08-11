"""Recovery domain models."""

from pydantic import BaseModel


class RecoveryAction(BaseModel):
    """A recovery action proposed for an incident."""

    action_id: str
    incident_id: str
    action: str
    status: str = "pending"
    approved: bool = False


class RecoveryResult(BaseModel):
    """Result of a recovery execution."""

    action_id: str
    status: str
    message: str