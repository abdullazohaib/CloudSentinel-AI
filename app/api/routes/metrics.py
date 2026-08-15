"""Prometheus metrics API endpoint."""

from fastapi import APIRouter
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

# Import the metrics module so all CloudSentinel metrics
# are registered with Prometheus.
from app.integrations import metrics as cloudsentinel_metrics


router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"],
)


@router.get("")
async def metrics() -> Response:
    """Return Prometheus metrics."""

    # Keep the module import explicit so the custom
    # CloudSentinel counters and histograms are registered.
    _ = cloudsentinel_metrics

    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )