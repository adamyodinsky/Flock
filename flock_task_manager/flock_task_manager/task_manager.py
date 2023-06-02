import json
import logging

from flock_common.queue_client import QueueClient
from flock_schemas.card import Ticket
from flock_task_management_store import TaskManagementStore


class TaskManager:
    """Task manager"""

    def __init__(self, queue_client: QueueClient, db_client: TaskManagementStore):
        self.queue_client = queue_client
        self.db_client = db_client

    def save_ticket(self, message_body):
        """Save a message to the database only if not exists, check by id"""
        self.db_client.save_ticket(message_body)

    def callback(self, ch, method, properties, message_body):
        """Callback for receiving a message"""
        logging.info("Received message")
        ticket = json.loads(message_body)
        self.label(ticket)
        self._format(ticket)
        # send to db
        self.db_client.save_ticket(ticket)

    def close(self):
        """Close the queue connection"""
        self.queue_client.close()

    def label(self, message_body):
        """Label a message"""
        logging.debug("Labeling message")

    def _format(self, message_body):
        """Format a message"""
        logging.debug("Formatting message")

    def manage_tasks(self):
        """Manage tasks"""
        self.queue_client.consume(self.callback)
