"""Base class for task management store."""
import abc

# from flock_schemas.card import Ticket


class TaskManagementStore(metaclass=abc.ABCMeta):
    """Base class for task management store."""

    @abc.abstractmethod
    def save_ticket(self, ticket):
        """Save task to store, only if it doesn't exist. If it exists, do nothing.

        Args:
            task (Task): Task to save.

            Returns:
                bool: True if task was saved, False if it already exists.
        """
