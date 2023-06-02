import json
import logging
from abc import ABC, abstractmethod

import pika


class QueueClient(ABC):
    """Interface for a queue client"""

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def produce(self, message_body):
        pass

    @abstractmethod
    def consume(self, callback):
        pass

    @abstractmethod
    def close(self):
        pass


class RabbitMQClient(QueueClient):
    """RabbitMQ queue client"""

    def __init__(
        self,
        queue_name="",
        host="localhost",
        port=5672,
        vhost="/",
        username="root",
        password="password",
    ):
        self.host = host
        self.port = port
        self.vhost = vhost
        self.username = username
        self.password = password
        self.queue_name = queue_name
        self.connection = NotImplemented
        self.channel = NotImplemented

        if not self.queue_name:
            logging.error("Must specify queue name")
            raise RuntimeError("Must specify queue name")

        logging.debug(
            "RabbitMQClient initialized with host=%s, port=%s, vhost=%s, username=%s, queue_name=%s",
            self.host,
            self.port,
            self.vhost,
            self.username,
            self.queue_name,
        )

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            self.host, self.port, self.vhost, credentials
        )
        try:
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name)
            self.channel.confirm_delivery()
            logging.info(
                "Connected to queue %s at %s:%s", self.queue_name, self.host, self.port
            )
        except pika.exceptions.AMQPConnectionError as err:
            logging.error("Error connecting to queue: %s", err)
            raise err
        except pika.exceptions.ChannelWrongStateError as err:
            logging.error("Error connecting to queue: %s", err)
            raise err

    def produce(self, message_body):
        while True:
            try:
                self.channel.basic_publish(
                    exchange="",
                    routing_key=self.queue_name,
                    body=json.dumps(message_body),
                    mandatory=True,
                )
                logging.debug(
                    "Message was sent to queue %s successfully.",
                    self.queue_name,
                )
                break  # exit the loop if everything was successful
            except pika.exceptions.ChannelWrongStateError as err:
                logging.error("Channel error: %s", err)
                self.connect()
            except pika.exceptions.StreamLostError as err:
                logging.error("Stream error: %s", err)
                self.connect()

        if self.connection is None or self.channel is None:
            logging.error("Must call connect before receiving a message.")
            raise RuntimeError("Must call connect before receiving a message.")
        self.channel.basic_publish(
            exchange="", routing_key=self.queue_name, body=json.dumps(message_body)
        )

    def consume(self, callback, auto_ack=True):
        if self.connection is None or self.channel is None:
            logging.error("Must call connect before receiving a message.")
            raise RuntimeError("Must call connect before receiving a message.")
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=callback, auto_ack=auto_ack
        )
        try:
            logging.info("Waiting for messages. on queue %s", self.queue_name)
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logging.info("Stopping consumer")
            self.channel.stop_consuming()

    def close(self):
        if self.connection is not None:
            logging.info("Closing connection to queue %s", self.queue_name)
            self.connection.close()


# factory class
class QueueClientFactory:
    """Factory class for queue clients"""

    @staticmethod
    def get_client(client_type, **kwargs) -> QueueClient:
        """Return a queue client"""

        client = NotImplemented
        if client_type == "rabbitmq":
            client = RabbitMQClient(**kwargs)
        else:
            logging.error("Invalid queue client specified %s", client_type)
            raise RuntimeError("Invalid queue client specified")

        logging.info("Using queue client %s", client_type)
        return client
