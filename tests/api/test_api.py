"""API endpoint tests."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    """Health endpoint should return a healthy status."""

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data


def test_analyze_endpoint() -> None:
    """Analyze endpoint should accept valid logs."""

    payload = {
        "service_name": "payment-service",
        "logs": [
            {
                "timestamp": "2026-08-10T18:00:00",
                "level": "ERROR",
                "message": "Database connection failed",
            }
        ],
    }

    response = client.post("/analyze", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "recommendations_generated"
    assert data["incident_id"] == "INC-PENDING"
    assert data["message"] == "Incident analysis completed."


def test_analyze_invalid_request() -> None:
    """Analyze endpoint should reject invalid request data."""

    payload = {
        "service_name": "",
        "logs": [],
    }

    response = client.post("/analyze", json=payload)

    assert response.status_code == 422

    data = response.json()

    assert data["error"] == "Invalid request data"
    assert data["status_code"] == 422
    assert "details" in data