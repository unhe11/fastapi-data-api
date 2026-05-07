from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}

def test_create_data():
    response = client.post(
        "/api/v1/data/test",
        json={"x": 1.5, "y": 2.3, "z": 0.8}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["device_id"] == "test"
    assert "timestamp" in data

def test_get_data():
    response = client.get("/api/v1/data/test")
    assert response.status_code == 200
    data = response.json()
    assert data["device_id"] == "test"
    assert isinstance(data["data"], list)
    assert isinstance(data["count"], int)
