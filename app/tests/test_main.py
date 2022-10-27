from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world. O projeto está feito meus caros"}