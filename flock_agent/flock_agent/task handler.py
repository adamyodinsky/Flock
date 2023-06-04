from flock_common.queue_client import QueueClient
from flock_task_management_store.mongo import (
    MongoTaskManagementStore,
    TaskManagementStore,
)


class TaskHandler:
    def __init__(self, queue_client: QueueClient, db_client: MongoTaskManagementStore):
        self.queue_client = queue_client
        self.db_client = db_client

    def handle_task(self):
        """
        Handle the task

        """

        while True:
            ticket = self.db_client.query({"idList": "todo"})
            if ticket:
                if self.db_client.acquire_lock(ticket):
                    result = self.agent(ticket)
                    self.queue_client.put(result)
            else:
                ticket = self.db_client.watch_ticket()
                if ticket:
                    if self.db_client.acquire_lock(ticket):
                        result = self.agent(ticket)
                        self.queue_client.put(result)
