"""AI-assisted Root Cause Analysis."""

from app.domain.incidents.models import Incident
from app.domain.rca.models import RCAResult
from app.integrations.ollama_client import OllamaClient


class AIRCAEngine:
    """Enhance rule-based RCA using an LLM."""

    def __init__(
        self,
        ollama_client: OllamaClient | None = None,
    ) -> None:
        self.ollama = ollama_client or OllamaClient()

    def analyze(
        self,
        incident: Incident,
        base_rca: RCAResult,
    ) -> RCAResult:
        """Use Ollama to enhance an existing RCA."""

        prompt = f"""
You are a cloud incident response assistant.

Analyze this incident.

Service: {incident.service_name}
Severity: {incident.severity}
Message: {incident.message}

Existing rule-based root cause:
{base_rca.root_cause}

Existing evidence:
{", ".join(base_rca.evidence)}

Provide a concise technical explanation of:
1. Probable root cause
2. Why it happened
3. What engineers should investigate next

Do not invent infrastructure details that are not provided.
"""

        ai_response = self.ollama.generate(prompt)

        if not ai_response:
            return base_rca

        return RCAResult(
            root_cause=base_rca.root_cause,
            explanation=ai_response,
            evidence=base_rca.evidence,
            confidence=base_rca.confidence,
        )