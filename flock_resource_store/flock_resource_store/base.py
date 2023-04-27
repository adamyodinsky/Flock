"""Resources store base class. This class is used to save and load entities."""
import abc


class ResourceStore(metaclass=abc.ABCMeta):
    """Abstract base class for resource stores."""

    @abc.abstractmethod
    def put(self, key, val) -> None:
        """Save a resource to the store."""

    @abc.abstractmethod
    def get(self, key):
        """Load a resource from the store."""
