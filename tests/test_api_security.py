
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_claims_endpoint():
    response = client.get("/claims")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_unknown_claim_returns_404():
    response = client.get("/claims/UNKNOWN-CLAIM")
    assert response.status_code == 404


def test_unknown_ai_claim_returns_404():
    response = client.get("/ai/explain/UNKNOWN-CLAIM")
    assert response.status_code == 404


def test_ai_explanation_rejects_non_denied_claim():
    response = client.get("/ai/explain/CLM-1002")
    assert response.status_code == 400
    assert "only for denied claims" in response.json()["detail"]


def test_metrics_endpoint():
    response = client.get("/metrics/summary")
    assert response.status_code == 200

    data = response.json()
    assert "total_claims" in data
    assert "denial_rate" in data
