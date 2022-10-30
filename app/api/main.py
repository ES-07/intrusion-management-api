from fastapi import FastAPI, Form
from app.redis import init_redis_pool
import requests, json

app = FastAPI(
    openapi_url="/openapi.json",
    docs_url="/docs",)
# incluir router mais tarde3


# API_GATEWAY = <link>
API_SITES = 'http://localhost:8002'

@app.on_event("startup")
async def startup_event():
    app.state.redis = await init_redis_pool()
    # criar repositório bd


@app.get("/")
def root():
    return {"message": "Welcome to Intrusion Management API :)"}


@app.post("/intrusions")
async def getIntrusionData(building_id: int = Form(), device_id: int = Form(), timestamp: str = Form()):
    payload = {"building_id": building_id, "device_id": device_id, "timestamp": timestamp}
    sent_to_sitesAPI = requests.post(f"{API_SITES}/intrusions", json=payload)

    if sent_to_sitesAPI.status_code == 200:
        print(json.loads(sent_to_sitesAPI.content.decode('utf-8')))

    return sent_to_sitesAPI.content
    


@app.get("/intrusions/frames")
def getVideoFrames():
    return {"message": "get the video frames"}


@app.get("/intrusions/videos")
def getVideo():
    return {"message": "get video from cameras"}


@app.post("/intrusions/videos")
def saveClips():
    """ sendo to AWS S3 """
    return {"message": "save the video clip in ASW S3"}


@app.post("/intrusions/activates")
def activateAlarms():
    return {"message": "send to message queue to activate alarms"}


@app.post("/intrusions/notifications")
def sendNotification():
    return {"message": "send request to notification API"}