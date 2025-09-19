from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_main():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "ok"
