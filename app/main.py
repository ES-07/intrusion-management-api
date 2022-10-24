from fastapi import FastAPI, HTTPException
from starlette.responses import Response
from app.redis import init_redis_pool

app = FastAPI()
# incluir router mais tarde3

@app.on_event("startup")
async def startup_event():
    app.state.redis = await init_redis_pool()
    # criar repositório bd


@app.get("/")
def root():
    return {"message": "Hello world. O projeto está feito meus caros"}


@app.post("/intrusion")
def getIntrusionData(request):
    data = request.data
    print(data)
    return {"message": "check if an intrusion occurs"}


@app.get("/intrusion/frames")
def getVideoFrames():
    return {"message": "get the video frames"}


@app.get("/intrusion/video")
def getVideo():
    return {"message": "get video from cameras"}


@app.post("/intrusion/video")
def saveClips():
    """ sendo to AWS S3 """
    return {"message": "save the video clip in ASW S3"}


@app.post("/intrusion/activate")
def activateAlarms():
    return {"message": "send to message queue to activate alarms"}


@app.post("/intrusion/notification")
def sendNotification():
    return {"message": "send request to notification API"}