import logging
from typing import Optional

# from flock_schemas.card import Ticket
from pymongo import MongoClient

from flock_task_management_store.base import TaskManagementStore


class MongoTaskManagementStore(TaskManagementStore):
    """MongoDB Resource Store

    Args:
        db_name (str): Name of the database to use.
        collection_name (str): Name of the collection to use.
        host (str, optional): Hostname of the MongoDB server. Defaults to "localhost".
        port (int, optional): Port of the MongoDB server. Defaults to 27017.
        username (Optional[str], optional): Username to use for authentication. Defaults to "".
        password (Optional[str], optional): Password to use for authentication. Defaults to "".
        client (Optional[MongoClient], optional): MongoClient instance to use. Defaults to NotImplemented.
    """

    _shared_state = {}

    def __init__(
        self,
        db_name: str,
        collection_name: str,
        host: str = "localhost",
        port: int = 27017,
        username: Optional[str] = "",
        password: Optional[str] = "",
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
            self.collection = self.db[collection_name]
            logging.debug(
                "Initialized MongoTaskManagementStore with db_name: %s, collection_name: %s, host: %s, port: %s",
                db_name,
                collection_name,
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
            self.collection.update_one(
                {"_id": ticket["id"]}, {"$setOnInsert": ticket}, upsert=True
            ).upserted_id
            is not None
        )

        if saved:
            logging.info("Saved ticket: %s", ticket["id"])
        else:
            logging.debug("Ticket already exists: %s", ticket["id"])
