from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_task_success():
    response = client.post("/task", json={"latitude": 45.0, "longitude": -105.0, "priority": 5})
    assert response.status_code == 202
    assert "task_id" in response.json()

def test_create_task_invalid_latitude():
    response = client.post("/task", json={"latitude": 100.0, "longitude": -105.0, "priority": 1})
    assert response.status_code == 422