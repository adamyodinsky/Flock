import logging
import queue
from datetime import datetime, timedelta
from typing import Optional

import pymongo

# from flock_schemas.card import Ticket
from pymongo import MongoClient

from flock_task_management_store.base import TaskManagementStore


class MongoTaskManagementStore(TaskManagementStore):
    """MongoDB Resource Store

    Args:
        db_name (str): Name of the database to use.
        tickets_table_name (str): Name of the tickets table.
        locks_table_name (str): Name of the locks table.
        host (str, optional): Hostname of the MongoDB server. Defaults to "localhost".
        port (int, optional): Port of the MongoDB server. Defaults to 27017.
        username (Optional[str], optional): Username to use for authentication. Defaults to "".
        password (Optional[str], optional): Password to use for authentication. Defaults to "".
        client (Optional[MongoClient], optional): MongoClient instance to use. Defaults to NotImplemented.
    """

    _shared_state = {}

    def __init__(
        self,
        db_name: str = "flock_db",
        tickets_table_name: str = "tickets",
        locks_table_name: str = "tickets_locks",
        host: str = "localhost",
        port: int = 27017,
        username: str = "root",
        password: str = "password",
        client: Optional[MongoClient] = None,
    ):
        # Implement the Borg design pattern
        self.__dict__ = self._shared_state

        # Initialize the client and db
        if not self._shared_state:
            self.client = client or MongoClient(
                host=host,
                port=port,
                username=username,
                password=password,
            )

            self.db = self.client[db_name]  # pylint: disable=invalid-name
            self.tickets_table = self.db[tickets_table_name]
            self.locks_table = self.db[locks_table_name]
            self.locks_table.create_index(
                [("expireAt", pymongo.ASCENDING)], expireAfterSeconds=0
            )

            logging.debug(
                "Initialized MongoTaskManagementStore with db_name: %s, host: %s, port: %s",
                db_name,
                host,
                port,
            )

    def save_ticket(self, ticket):
        """Save task to store, only if it doesn't exist. If it exists, do nothing.

        Args:
            task (Task): Task to save.

            Returns:
                bool: True if task was saved, False if it already exists.
        """
        saved = (
            self.tickets_table.update_one(
                {"_id": ticket["id"]}, {"$setOnInsert": ticket}, upsert=True
            ).upserted_id
            is not None
        )

        if saved:
            logging.info("Saved ticket: %s", ticket["id"])
        else:
            logging.debug("Ticket already exists: %s", ticket["id"])

    def acquire_lock(self, ticket):
        """Acquire lock on task."""

        lock = {
            "_id": ticket["id"],
            "boardId": ticket["idBoard"],
            "expireAt": datetime.utcnow() + timedelta(minutes=60),
        }
        acquired = (
            self.locks_table.update_one(
                lock, {"$setOnInsert": ticket}, upsert=True
            ).upserted_id
            is not None
        )

        if acquired:
            logging.info("Acquired lock on ticket: %s", ticket["id"])
        else:
            logging.debug("Lock already exists: %s", ticket["id"])
        return acquired

    def free_lock(self, ticket):
        """Free lock on task."""

        lock = {
            "_id": ticket["id"],
            "boardId": ticket["idBoard"],
        }

        self.locks_table.delete_one(lock)
        logging.info("Freed lock on ticket: %s", ticket["id"])

    # where ticket.list == todo)
    # with(watch stream for "insert" on collection "tickets" in the db):

    def query(self, query):
        """Query tasks from store.


        Returns:
            list: List of tasks.
        """

        return self.tickets_table.find_one(query)

    def watch_on_insert(self, result_box: queue.Queue = None):
        """Watch for changes to tasks in store.

        Returns:
            pymongo.cursor.Cursor: Cursor to iterate over changes.
        """

        with self.tickets_table.watch(
            [{"$match": {"operationType": "insert"}}]
        ) as stream:
            for insert_change in stream:
                logging.debug("Change: %s", insert_change)
                if insert_change.fullDocument["idList"] == "todo":
                    if result_box:
                        result_box.put(insert_change.fullDocument)
                    return insert_change.fullDocument
