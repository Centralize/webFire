from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "ok"

def test_login_for_access_token():
    response = client.post(
        "/token",
        data={"username": "admin", "password": "secret"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_get_status_unauthorized():
    response = client.get("/api/status")
    assert response.status_code == 401

def test_get_status_authorized():
    # First, get a token
    token_response = client.post(
        "/token",
        data={"username": "admin", "password": "secret"}
    )
    access_token = token_response.json()["access_token"]

    # Then, use the token to access the protected endpoint
    response = client.get(
        "/api/status",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert "status" in response.json()
