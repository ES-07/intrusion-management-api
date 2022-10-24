from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world. O projeto está feito meus caros"}



def test_getIntrusionData():
    response = client.get("/intrusion")
    assert response.status_code == 200
    assert response.json() == {"message": "check if an intrusion occurs"}