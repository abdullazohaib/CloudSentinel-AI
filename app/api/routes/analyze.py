"""Incident analysis API route."""

from fastapi import APIRouter

from app.api.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.core.logging import get_logger
from app.domain.incidents.models import Incident
from app.integrations.metrics import record_ai_analysis
from app.orchestration.graph import incident_graph


router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"],
)

logger = get_logger(__name__)


@router.post("", response_model=AnalysisResponse)
async def analyze_incident(
    request: AnalysisRequest,
) -> AnalysisResponse:
    """Analyze incident logs using the LangGraph workflow."""

    logger.info(
        "Starting incident analysis for service=%s logs=%d",
        request.service_name,
        len(request.logs),
    )

    incident = Incident(
        incident_id="INC-PENDING",
        service_name=request.service_name,
        severity="Unknown",
        status="Investigating",
        message="Incident received for AI analysis.",
        timestamp=request.logs[0].timestamp,
        logs=[
            {
                "timestamp": log.timestamp,
                "level": log.level,
                "message": log.message,
            }
            for log in request.logs
        ],
    )

    result = incident_graph.invoke(
        {
            "incident": incident,
        }
    )

    record_ai_analysis()

    logger.info(
        "Incident analysis completed status=%s",
        result.get("status", "analyzed"),
    )

    return AnalysisResponse(
        status=result.get(
            "status",
            "analyzed",
        ),
        incident_id="INC-PENDING",
        message="Incident analysis completed.",
        analysis={
            "severity": result.get("severity"),
            "rca": result.get("rca"),
            "recommendations": result.get(
                "recommendations"
            ),
        },
    )