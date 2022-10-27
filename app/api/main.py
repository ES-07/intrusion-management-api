from fastapi import FastAPI, HTTPException
from starlette.responses import Response

app = FastAPI()
# incluir router mais tarde3

@app.get("/")
def hello():    
    return {"message": "CI/CD done in AWS EC2"}

@app.get("/hello")
def hello():    
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