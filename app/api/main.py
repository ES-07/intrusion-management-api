import requests
import json
from fastapi import FastAPI, HTTPException, Form
from starlette.responses import Response
import pydantic
import boto3
from pydantic import BaseModel
import kombu
from dotenv import load_dotenv
from pathlib import Path
import os


BASE_PREFIX = "/intrusion-management-api"
CAMERAS_API = "http://13.38.103.68:8003"
# Load environment variables
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

RABBIT_MQ_URL = os.getenv('RABBIT_MQ_URL')
RABBIT_MQ_USERNAME = os.getenv('RABBIT_MQ_USERNAME')
RABBIT_MQ_PASSWORD = os.getenv('RABBIT_MQ_PASSWORD')
RABBIT_MQ_EXCHANGE_NAME = os.getenv('RABBIT_MQ_EXCHANGE_NAME')
RABBIT_MQ_QUEUE_NAME = os.getenv('RABBIT_MQ_QUEUE_NAME')
ALB_PREFIX = os.getenv('ALB_PREFIX')


class Config:
    arbitrary_types_allowed = True


@pydantic.dataclasses.dataclass(config=Config)
class Intrusion:
    timestamp: str
    building_id: int
    device_id: int

    def __init__(self, timestamp, building_id, device_id) -> None:
        self.timestamp = timestamp
        self.building_id = building_id
        self.device_id = device_id

    def getFirstFrameTimeStamp(self):
        pass


@pydantic.dataclasses.dataclass(config=Config)
class VideoStore:
    path_to_video: str
    bucket_name: str
    video_name: str

    def __init__(self, path_to_video, bucket_name, video_name) -> None:
        self.path_to_video = "api/" + path_to_video
        self.bucket_name = bucket_name
        self.video_name = video_name


connection_string = f"amqp://{RABBIT_MQ_USERNAME}:{RABBIT_MQ_PASSWORD}" \
    f"@{RABBIT_MQ_URL}/"


# Kombu Connection
kombu_connection = kombu.Connection(connection_string, ssl=True)
kombu_channel = kombu_connection.channel()

# Kombu Exchange
kombu_exchange = kombu.Exchange(
    name=RABBIT_MQ_EXCHANGE_NAME,
    type="direct",
    delivery_mode=1
)

# Kombu Producer
kombu_producer = kombu.Producer(
    exchange=kombu_exchange,
    channel=kombu_channel
)

# Kombu Queue
kombu_queue = kombu.Queue(
    name=RABBIT_MQ_QUEUE_NAME,
    exchange=kombu_exchange
)
kombu_queue.maybe_bind(kombu_connection)
kombu_queue.declare()


s3 = boto3.client('s3')
app = FastAPI(
    openapi_url=BASE_PREFIX + "/openapi.json",
    docs_url=BASE_PREFIX + "/docs")


@app.get(BASE_PREFIX + "/")
def root():
    return {"message": "Welcome to Intrusion Management API :)"}


@app.post(BASE_PREFIX + "/intrusions")
async def getIntrusionData(new_intrusion: Intrusion):

    payload = {"building_id": new_intrusion.building_id,
               "device_id": new_intrusion.device_id, "timestamp": new_intrusion.timestamp}

    getVideoFrames(0, 100)
    activateAlarms(new_intrusion.timestamp)

    sent_to_sitesAPI = requests.post(f"{ALB_PREFIX}/sites-management-api/intrusions", json=payload)
    if sent_to_sitesAPI.status_code == 200:
        print(json.loads(sent_to_sitesAPI.content.decode('utf-8')))

    # mandar para o rabbitmq

    return {"message": "Intrusion data received"}


"""
@app.get(BASE_PREFIX + "/intrusions/frames")
def getVideoFrames():

@app.post(BASE_PREFIX + "/intrusion")
def newIntrusionData(intrusion: Intrusion):
    # chega um timestamp que depois é passado às câmaras
    
    start, end = intrusion.getFirstFrameTimeStamp()
    getVideoFrames(start, end)

    return {"Intrusion": "detected", "timestamp": intrusion.timestamp, "frame": intrusion.frame_id}
"""


@app.get(BASE_PREFIX + "/intrusion/frames")
def getVideoFrames(start, end):
    response = requests.get(CAMERAS_API + '/video?start=' +
                            str(start)+'&end='+str(end))

    return {"message": "get the video frames"}


@app.get(BASE_PREFIX + "/intrusions/videos")
def getVideo():
    return {"message": "get video from cameras"}


@app.post(BASE_PREFIX + "/intrusion/video")
def saveClips(video: VideoStore):
    """ sendo to AWS S3 """

    s3.upload_file(video.path_to_video, video.bucket_name, video.video_name)
    return {"message": "video saved"}


@app.post(BASE_PREFIX + "/intrusions/activates")
def activateAlarms(timestamp):
    kombu_producer.publish(
        content_type='application/json',
        body=json.dumps({"intrusionDetected": "True", "timestamp": timestamp}),
    )
    return {"message": "send to message queue to activate alarms"}


@app.post(BASE_PREFIX + "/intrusions/notifications")
def sendNotification():
    return {"message": "send request to notification API"}
