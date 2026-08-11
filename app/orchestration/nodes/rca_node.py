"""LangGraph root cause analysis node (placeholder). No logic implemented yet."""
"""Root-cause-analysis node for the incident-response workflow."""

from app.domain.rca.ai_engine import AIRCAEngine
from app.domain.rca.engine import RCAEngine
from app.orchestration.state import IncidentState


def rca_node(state: IncidentState) -> IncidentState:
    """Run rule-based RCA and optionally enhance it with AI."""

    incident = state["incident"]

    rule_engine = RCAEngine()
    base_rca = rule_engine.analyze(incident)

    try:
        ai_engine = AIRCAEngine()
        enhanced_rca = ai_engine.analyze(
            incident,
            base_rca,
        )
        result = enhanced_rca

    except Exception:
        # Ollama may not be running.
        # Rule-based RCA remains the safe fallback.
        result = base_rca

    return {
        **state,
        "rca": result,
        "status": "rca_completed",
    }