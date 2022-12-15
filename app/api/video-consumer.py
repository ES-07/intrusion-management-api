import cv2
import os
import numpy as np
import sys
import kombu
import requests


from kombu.mixins import ConsumerMixin
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

RABBIT_MQ_URL = os.getenv('RABBIT_MQ_URL')
RABBIT_MQ_USERNAME = os.getenv('RABBIT_MQ_USERNAME')
RABBIT_MQ_PASSWORD = os.getenv('RABBIT_MQ_PASSWORD')
RABBIT_MQ_EXCHANGE_NAME = 'video-exchange'
RABBIT_MQ_QUEUE_NAME = 'video-queue'


VIDEO_NAME = "video/records.mp4"
BASE_URL = "http://localhost:8000"

rabbit_url = f'amqp://{RABBIT_MQ_USERNAME}:{RABBIT_MQ_PASSWORD}@{RABBIT_MQ_URL}//'
# Kombu Message Consuming Worker


class Worker(ConsumerMixin):

    receivedImages = []
    
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues

        if not os.path.exists("video"):
            os.makedirs("video")

        self.out = cv2.VideoWriter(
            VIDEO_NAME, cv2.VideoWriter_fourcc(*'mp4v'), 3, (768, 432))
        self.contador = 0

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message],
                         accept=['image/jpeg', 'application/json'])]

    def on_message(self, body, message):
        # get the original jpeg byte array size
        if message.content_type == 'application/json':

            for i in self.receivedImages:
                self.out.write(i)

            self.out.release()

            message.ack()

            response = requests.post(
                BASE_URL+'/intrusion/video',
                json={'path_to_video': VIDEO_NAME,
                      'bucket_name': 'video-archive-es007',
                      'video_name': f'record{self.contador}.mp4'}
            )

            self.contador += 1
            return

        size = sys.getsizeof(body) - 33

        # jpeg-encoded byte array into numpy array
        np_array = np.frombuffer(body, dtype=np.uint8)
        np_array = np_array.reshape((size, 1))
        # decode jpeg-encoded numpy array
        image = cv2.imdecode(np_array, 1)

        self.receivedImages.append(image)
        message.ack()


def run():
    exchange = kombu.Exchange(RABBIT_MQ_EXCHANGE_NAME, type="direct")
    queues = [kombu.Queue(RABBIT_MQ_QUEUE_NAME, exchange, routing_key="video")]

    conn = kombu.Connection(rabbit_url, heartbeat=4, ssl=True)

    worker = Worker(conn, queues)
    worker.run()


if __name__ == "__main__":
    run()
