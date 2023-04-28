"""Resources store base class. This class is used to save and load entities."""
import abc


class ResourceStore(metaclass=abc.ABCMeta):
    """Abstract base class for resource stores."""

    @abc.abstractmethod
    def put(self, key, val) -> None:
        """Save a resource to the store."""

    @abc.abstractmethod
    def get(self, key) -> dict:
        """Load a resource from the store."""

    @abc.abstractmethod
    def get_many(self, key):
        """Get many resources with the same namespace and kind"""

    @abc.abstractmethod
    def load_file(self, path, file_type="yaml") -> dict:
        """Load a file from the file system."""
