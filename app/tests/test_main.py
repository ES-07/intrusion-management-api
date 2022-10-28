from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world. O projeto está feito meus caros"}



def test_getIntrusionData():
    response = client.get("/intrusion/frames")
    assert response.status_code == 200
    assert response.json() == {"message": "get the video frames"}