"""Incident analysis API route."""

from fastapi import APIRouter

from app.api.schemas.analysis import AnalysisRequest, AnalysisResponse


router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"],
)


@router.post("", response_model=AnalysisResponse)
async def analyze_incident(
    request: AnalysisRequest,
) -> AnalysisResponse:
    """Receive incident logs for analysis."""

    return AnalysisResponse(
        status="received",
        incident_id="INC-PENDING",
        message=(
            f"Received {len(request.logs)} log entries "
            f"for service '{request.service_name}'."
        ),
    )