Sure, let's start by creating a Python interface for a generic queue. Python doesn't have explicit interface declarations like some other languages (e.g., Java or C#), but we can simulate them using abstract base classes. Let's define some methods that you'll likely need for interacting with a queue.

```python
from abc import ABC, abstractmethod

class QueueInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def send(self, queue_name, message_body):
        pass

    @abstractmethod
    def receive(self, queue_name, callback):
        pass

    @abstractmethod
    def close(self):
        pass
```

Now, let's implement the `QueueInterface` for RabbitMQ using Pika:

```python
import pika

class RabbitMQQueue(QueueInterface):
    def __init__(self, host):
        self.host = host
        self.connection = None
        self.channel = None

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()

    def send(self, queue_name, message_body):
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_publish(exchange='', routing_key=queue_name, body=message_body)

    def receive(self, queue_name, callback):
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    def close(self):
        self.connection.close()
```

To work with Kafka, we can use a Python library called `confluent_kafka`. Here is an implementation for Kafka:

```python
from confluent_kafka import Producer, Consumer, KafkaError

class KafkaQueue(QueueInterface):
    def __init__(self, config):
        self.config = config
        self.producer = None
        self.consumer = None

    def connect(self):
        self.producer = Producer(self.config)
        self.consumer = Consumer(self.config)

    def send(self, queue_name, message_body):
        self.producer.produce(queue_name, message_body)
        self.producer.flush()

    def receive(self, queue_name, callback):
        self.consumer.subscribe([queue_name])

        while True:
            message = self.consumer.poll(1.0)

            if message is None:
                continue
            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    break

            callback(None, None, None, message.value())

    def close(self):
        self.consumer.close()
        self.producer.flush()
```

The above `KafkaQueue` class sets up a Kafka consumer to continuously poll for new messages. If a new message is found, it calls the provided callback function. 

Please note: In both classes, I've simplified the connection setup and error handling for clarity. In a production environment, you'd want to have error checking, reconnection logic, and possibly more complex setup (e.g., SSL, authentication, etc.). 

Also, for Kafka, you would need to provide a configuration dict (`config`) when creating an instance of `KafkaQueue`. This configuration will contain at least the `bootstrap.servers` key to specify your Kafka cluster address. It may also include other configurations like `group.id`, `client.id`, `security.protocol`, etc., depending on your setup.