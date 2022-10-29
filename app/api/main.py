from time import time
from fastapi import FastAPI, HTTPException
from starlette.responses import Response

from app.api.notification import Notification

app = FastAPI()
# incluir router mais tarde3

@app.get("/")
def hello():    
    return {"message": "CI/CD done in AWS EC2"}

@app.get("/marta")
def hello():    
    return {"message": "paiga"}

@app.get("/hello")
def hello():    
    return {"message": "Hello world. O projeto está feito meus caros"}


@app.post("/intrusion")
def getIntrusionData(request):
    data = request.data
    print(data)
    timestamp = data['timestamp']
    camera_id = data['camera_id']
    frame_id = data['frame_id']
    notificate_client(timestamp, camera_id, frame_id)
    activate_alarms()
    request_video()
    store_video()
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


def notificate_client(timestamp, camera_id, frame_id):

    RABBIT_MQ_URL = "localhost:5672"
    RABBIT_MQ_USERNAME = "myuser"
    RABBIT_MQ_PASSWORD = "mypassword"
    RABBIT_MQ_EXCHANGE_NAME = "intrusion-management-exchange"
    RABBIT_MQ_QUEUE_NAME = "intrusion-management-queue"

    notification = Notification()
    notification.attach_to_message_broker(
        RABBIT_MQ_URL, 
        RABBIT_MQ_USERNAME, 
        RABBIT_MQ_PASSWORD, 
        RABBIT_MQ_EXCHANGE_NAME, 
        RABBIT_MQ_QUEUE_NAME
    )
    
def activate_alarms():
    pass

def request_video():
    pass

def store_video():
    pass