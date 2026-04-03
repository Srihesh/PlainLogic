from __future__ import annotations

from fastapi.testclient import TestClient

from resilienceos.environment import ResilienceOSEnvironment
from resilienceos import server


def _fresh_client() -> TestClient:
    server.env = ResilienceOSEnvironment()
    return TestClient(server.app)


def test_health_ok() -> None:
    client = _fresh_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_reset_returns_observation() -> None:
    client = _fresh_client()
    response = client.post("/reset", json={"task": "easy", "seed": 7})
    assert response.status_code == 200
    body = response.json()
    assert body["observation"]["task"] == "easy"
    assert body["observation"]["step"] == 0
    assert len(body["observation"]["incidents"]) == 1


def test_reset_is_deterministic_for_same_seed() -> None:
    client = _fresh_client()
    first = client.post("/reset", json={"task": "medium", "seed": 7})
    second = client.post("/reset", json={"task": "medium", "seed": 7})
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["observation"] == second.json()["observation"]


def test_invalid_task_returns_400() -> None:
    client = _fresh_client()
    response = client.post("/reset", json={"task": "invalid", "seed": 7})
    assert response.status_code == 400
    assert "task must be one of" in response.json()["detail"]


def test_step_and_state_flow() -> None:
    client = _fresh_client()
    reset = client.post("/reset", json={"task": "easy", "seed": 7})
    assert reset.status_code == 200

    step = client.post(
        "/step",
        json={
            "action_type": "classify_incident",
            "incident_id": "I1",
            "payload": {"label": "standard"},
        },
    )
    assert step.status_code == 200
    step_body = step.json()
    assert step_body["observation"]["step"] == 1

    state = client.get("/state")
    assert state.status_code == 200
    assert state.json()["step"] == 1


def test_step_without_reset_returns_400() -> None:
    client = _fresh_client()
    response = client.post(
        "/step",
        json={
            "action_type": "classify_incident",
            "incident_id": "I1",
            "payload": {"label": "standard"},
        },
    )
    assert response.status_code == 400
    assert "Call reset first" in response.json()["detail"]


def test_state_without_reset_returns_400() -> None:
    client = _fresh_client()
    response = client.get("/state")
    assert response.status_code == 400
    assert "Call reset first" in response.json()["detail"]
