import requests, json
from fastapi import FastAPI, HTTPException, Form
from starlette.responses import Response
import time
import datetime
import pydantic 
import boto3
from pydantic import BaseModel

# API_GATEWAY = <link>
API_SITES = 'http://localhost:8002'
BASE_URL = "http://localhost:8001"


class Config:
    arbitrary_types_allowed = True

@pydantic.dataclasses.dataclass(config=Config)
class Intrusion(BaseModel):
    timestamp: str
    building_id: int
    device_id: int

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
app = FastAPI(
    openapi_url="/openapi.json",
    docs_url="/docs",)


@app.get("/")
def root():
    return {"message": "Welcome to Intrusion Management API :)"}


@app.post("/intrusions")
async def getIntrusionData(new_intrusion : Intrusion):
    payload = {"building_id": new_intrusion.building_id, "device_id": new_intrusion.device_id, "timestamp": new_intrusion.timestamp}
    sent_to_sitesAPI = requests.post(f"{API_SITES}/intrusions", json=payload)

    if sent_to_sitesAPI.status_code == 200:
        print(json.loads(sent_to_sitesAPI.content.decode('utf-8')))
    return sent_to_sitesAPI.content
    

"""
@app.get("/intrusions/frames")
def getVideoFrames():

@app.post("/intrusion")
def newIntrusionData(intrusion: Intrusion):
    # chega um timestamp que depois é passado às câmaras
    
    start, end = intrusion.getFirstFrameTimeStamp()
    getVideoFrames(start, end)

    return {"Intrusion": "detected", "timestamp": intrusion.timestamp, "frame": intrusion.frame_id}
"""

@app.get("/intrusion/frames")
def getVideoFrames(start, end):
    response = requests.get(BASE_URL+'/video?start='+str(start)+'&end='+str(end))
    return {"message": "get the video frames"}


@app.get("/intrusions/videos")
def getVideo():
    return {"message": "get video from cameras"}



@app.post("/intrusion/video")
def saveClips(video: VideoStore):
    """ sendo to AWS S3 """
    s3.upload_file(video.path_to_video, video.bucket_name, video.video_name)
    return {"message": "video saved"}


@app.post("/intrusions/activates")
def activateAlarms():
    return {"message": "send to message queue to activate alarms"}


@app.post("/intrusions/notifications")
def sendNotification():
    return {"message": "send request to notification API"}