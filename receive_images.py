import kombu
import json

class ReceiveImages:
    
    def __init__(self) -> None:
        pass

    def process_message(self, body, message):
        print(json.loads(body))
        message.ack()

    def process_messages(self, broker_url, broker_username,
                         broker_password, exchange_name, queue_name):
        
        # Create Connection String
        connection_string = f"amqp://{broker_username}:{broker_password}" \
            f"@{broker_url}/"

        # Kombu Exchange
        self.kombu_exchange = kombu.Exchange(
            name=exchange_name,
            type="direct",
        )

        # Kombu Queues
        self.queue = kombu.Queue(
                name=queue_name,
                exchange=self.kombu_exchange,
                routing_key=queue_name
                )
        

        # Kombu Connection
        self.kombu_connection = kombu.Connection(
            connection_string
        )

        with kombu.Consumer(self.kombu_connection, queues=self.queue, callbacks=[self.process_message],
                accept=["text/plain"]):
            while True:
                self.kombu_connection.drain_events()


if __name__ == "__main__":
    RABBIT_MQ_URL = "localhost:5672"
    RABBIT_MQ_USERNAME = "myuser"
    RABBIT_MQ_PASSWORD = "mypassword"
    RABBIT_MQ_EXCHANGE_NAME = "human-detection-exchange"
    RABBIT_MQ_QUEUE_NAME = "intrusion-api-queue"


    receive_images = ReceiveImages()
    receive_images.process_messages(
        broker_url=RABBIT_MQ_URL,
        broker_username=RABBIT_MQ_USERNAME,
        broker_password=RABBIT_MQ_PASSWORD,
        exchange_name=RABBIT_MQ_EXCHANGE_NAME,
        queue_name=RABBIT_MQ_QUEUE_NAME
    )

    
