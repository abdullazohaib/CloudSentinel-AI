"""Prometheus metrics API endpoint."""

from fastapi import APIRouter
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest


router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"],
)


@router.get("")
async def metrics() -> Response:
    """Return Prometheus metrics."""

    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )