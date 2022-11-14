from fastapi import FastAPI, HTTPException
from starlette.responses import Response
import requests
import time
import datetime
import pydantic 
import boto3





BASE_URL = "http://localhost:8001"

class Config:
    arbitrary_types_allowed = True

@pydantic.dataclasses.dataclass(config=Config)
class Intrusion:
    timestamp: int
    first_frame: int
    frame_id: int

    def __init__(self, timestamp, first_frame, frame_id)->None:
        self.timestamp = timestamp
        self.first_frame = first_frame
        self.frame_id = frame_id

    def getFirstFrameTimeStamp(self):
        # 0 ---------------- first_frame
        # frame_id --------- timestamp
        self.start = self.timestamp - 3 * 60 if self.timestamp -3 * 60 > self.first_frame else self.first_frame
        # checkar se o vídeo não está no fim
        self.end = self.timestamp + 3 * 60
        return self.start, self.end
        

@pydantic.dataclasses.dataclass(config=Config)
class VideoStore:
    path_to_video: str
    bucket_name: str
    video_name: str

    def __init__(self, path_to_video, bucket_name, video_name)->None:
        self.path_to_video = path_to_video
        self.bucket_name = bucket_name
        self.video_name = video_name




s3 = boto3.client('s3')
contador=0

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
def newIntrusionData(intrusion: Intrusion):
    # chega um timestamp que depois é passado às câmaras
    
    start, end = intrusion.getFirstFrameTimeStamp()
    getVideoFrames(start, end)

    return {"Intrusion": "detected", "timestamp": intrusion.timestamp, "frame": intrusion.frame_id}


@app.get("/intrusion/frames")
def getVideoFrames(start, end):
    response = requests.get(BASE_URL+'/video?start='+str(start)+'&end='+str(end))

    return {"message": "get the video frames"}


@app.get("/intrusion/video")
def getVideo():
    return {"message": "get video from cameras"}


@app.post("/intrusion/video")
def saveClips(video: VideoStore):
    """ sendo to AWS S3 """
    s3.upload_file(video.path_to_video, video.bucket_name, video.video_name)
    return {"message": "video saved"}


@app.post("/intrusion/activate")
def activateAlarms():
    return {"message": "send to message queue to activate alarms"}


@app.post("/intrusion/notification")
def sendNotification():
    return {"message": "send request to notification API"}