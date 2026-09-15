import pytest
from fastapi.testclient import TestClient
from vetra.api.server import create_app
from vetra.config import Settings
from vetra.core.enums import ExecutionMode


@pytest.fixture
def client():
    settings = Settings(execution_mode=ExecutionMode.SIMULATION)
    app = create_app(settings)
    with TestClient(app) as test_client:
        yield test_client


def test_api_health(client: TestClient):
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["mode"] == "simulation"


def test_api_stats(client: TestClient):
    resp = client.get("/api/v1/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert "gpu_stats" in data
    assert "cache_stats" in data
    assert "cost_breakdown" in data


def test_api_recommendations(client: TestClient):
    resp = client.get("/api/v1/recommendations")
    assert resp.status_code == 200
    data = resp.json()
    assert "recommendations" in data
    assert "gpu_pressure" in data


def test_api_decisions_apply_501(client: TestClient):
    payload = {
        "block_id": "test_blk",
        "tenant_id": "tenant_1",
        "current_location": "GPU",
        "recommended_location": "CPU",
        "decision": "OFFLOAD_CPU",
    }
    resp = client.post("/api/v1/cache/decisions/apply", json=payload)
    assert resp.status_code == 501
