"""Kubernetes health API routes."""

from typing import Any

from fastapi import APIRouter, Query

from app.integrations.kubernetes_client import KubernetesClient


router = APIRouter(
    prefix="/kubernetes",
    tags=["Kubernetes"],
)


@router.get("/health")
async def kubernetes_health(
    namespace: str = Query(
        default="default",
        min_length=1,
    ),
) -> dict[str, Any]:
    """Return Kubernetes cluster and workload health."""

    client = KubernetesClient()

    return client.health(namespace)