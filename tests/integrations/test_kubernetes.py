"""Tests for Kubernetes integration."""

from app.integrations.kubernetes_client import KubernetesClient


def test_kubernetes_client_can_initialize() -> None:
    """Kubernetes client should initialize safely."""

    client = KubernetesClient()

    assert isinstance(client.connected, bool)


def test_kubernetes_health_response() -> None:
    """Kubernetes health should return a consistent structure."""

    client = KubernetesClient()

    result = client.health()

    assert "connected" in result
    assert "namespace" in result
    assert "pod_count" in result
    assert "service_count" in result
    assert "pods" in result
    assert "services" in result


def test_kubernetes_pods_returns_list() -> None:
    """Pod inspection should return a list."""

    client = KubernetesClient()

    result = client.get_pods()

    assert isinstance(result, list)


def test_kubernetes_services_returns_list() -> None:
    """Service inspection should return a list."""

    client = KubernetesClient()

    result = client.get_services()

    assert isinstance(result, list)
    