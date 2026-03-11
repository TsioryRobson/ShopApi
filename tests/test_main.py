# TODO : Remove me at the end of project, it s just to test if the API-test is running

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Test shop API running"}