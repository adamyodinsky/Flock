"""Base class for task management store."""
import abc

# from flock_schemas.card import Ticket
from typing import Optional


class TaskManagementStore(metaclass=abc.ABCMeta):
    """Base class for task management store."""

    def __init__(
        self,
        db_name: str = "flock_db",
        tickets_table_name: str = "tickets",
        locks_table_name: str = "tickets_locks",
        host: str = "localhost",
        port: int = 27017,
        username: str = "root",
        password: str = "password",
        client=None,
    ):
        pass

    @abc.abstractmethod
    def save_ticket(self, ticket):
        """Save task to store, only if it doesn't exist. If it exists, do nothing.

        Args:
            task (Task): Task to save.

            Returns:
                bool: True if task was saved, False if it already exists.
        """

    @abc.abstractmethod
    def acquire_lock(self, ticket):
        pass

    @abc.abstractmethod
    def query(self, query):
        pass

    @abc.abstractmethod
    def watch_on_insert(self, result_box=None):
        pass
