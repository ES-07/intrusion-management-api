import cv2
import numpy as np
import sys
import time

from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin


broker_username = "myuser"
broker_password = "mypassword"
broker_url = "localhost:5672"

connection_string = f"amqp://{broker_username}:{broker_password}" \
            f"@{broker_url}/"


class Worker(ConsumerMixin):

    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues



    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,callbacks=[self.on_message],accept=['image/jpeg'])]

    def on_message(self, body, message):
        # get the original jpeg byte array size
        size = sys.getsizeof(body.tobytes()) - 33
        # jpeg-encoded byte array into numpy array
        np_array = np.frombuffer(body.tobytes(), dtype=np.uint8)
        np_array = np_array.reshape((size, 1))
        # decode jpeg-encoded numpy array 
        image = cv2.imdecode(np_array, 1)

        # show image
        cv2.imshow("image", image)
        cv2.waitKey(1)

        # send message ack
        message.ack()

def run():
    exchange = Exchange("video-exchange", type="direct")
    queues = [Queue("video-queue", exchange, routing_key="video")]
    with Connection(connection_string, heartbeat=4) as conn:
            worker = Worker(conn, queues)
            worker.run()

if __name__ == "__main__":
    run()