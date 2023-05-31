import json
import os
from abc import ABC, abstractmethod

import pika
from dotenv import find_dotenv, load_dotenv

from flock_common import check_env_vars


class QueueClient(ABC):
    """Interface for a queue client"""

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def send(self, message_body):
        pass

    @abstractmethod
    def receive(self, callback):
        pass

    @abstractmethod
    def close(self):
        pass


class RabbitMQClient(QueueClient):
    """RabbitMQ queue client"""

    def __init__(
        self,
        queue_name=None,
        host="localhost",
        port=5672,
        vhost="/",
        username="root",
        password="password",
    ):
        # Check env vars
        required_vars = []
        optional_vars = [
            "FLOCK_QUEUE_HOST",
            "FLOCK_QUEUE_PORT",
            "FLOCK_QUEUE_VHOST",
            "FLOCK_QUEUE_USERNAME",
            "FLOCK_QUEUE_PASSWORD",
            "FLOCK_QUEUE_NAME",
        ]
        load_dotenv(find_dotenv(os.environ.get("FLOCK_ENV_FILE", ".env")))
        check_env_vars(required_vars, optional_vars)

        self.host = os.environ.get("FLOCK_QUEUE_HOST", host)
        self.port = os.environ.get("FLOCK_QUEUE_PORT", port)
        self.vhost = os.environ.get("FLOCK_QUEUE_VHOST", vhost)
        self.username = os.environ.get("FLOCK_QUEUE_USERNAME", username)
        self.password = os.environ.get("FLOCK_QUEUE_PASSWORD", password)
        self.queue_name = os.environ.get("FLOCK_QUEUE_NAME", queue_name)
        self.connection = None
        self.channel = None

        if self.queue_name is None:
            raise RuntimeError("Must specify queue name")

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            self.host, self.port, self.vhost, credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def send(self, message_body):
        if self.connection is None or self.channel is None:
            raise RuntimeError("Must call connect before receiving a message.")
        self.channel.basic_publish(
            exchange="", routing_key=self.queue_name, body=json.dumps(message_body)
        )

    def receive(self, callback):
        if self.connection is None or self.channel is None:
            raise RuntimeError("Must call connect before receiving a message.")
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=callback, auto_ack=True
        )

    def close(self):
        if self.connection is not None:
            self.connection.close()


# factory class
class QueueClientFactory:
    """Factory class for queue clients"""

    @staticmethod
    def get_queue_client(client_type) -> type(QueueClient):
        if client_type == "rabbitmq":
            return RabbitMQClient
        else:
            raise RuntimeError("Invalid queue client specified")
