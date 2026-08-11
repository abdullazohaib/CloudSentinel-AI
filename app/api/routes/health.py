"""Health check route (placeholder). No logic implemented yet."""
"""Health check API route."""

from fastapi import APIRouter


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
async def health_check() -> dict[str, str]:
    """Return application health status."""

    return {
        "status": "healthy",
        "service": "CloudSentinel AI",
        "version": "1.0.0",
    }