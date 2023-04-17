"""Resources store base class. This class is used to save and load entities."""
import abc
import os


class ResourceStore(metaclass=abc.ABCMeta):
    """Abstract base class for resource stores."""

    def __init__(
        self, key_prefix: str
    ) -> None:
        """Initialize the resource store."""

        # self.manifest_prefix = f"{self.key_prefix}/manifest"
        # self.data_prefix = f"{self.key_prefix}/data"
        self.key_prefix = key_prefix
        self.resource_prefix = f"{self.key_prefix}/resource"

    @abc.abstractmethod
    def put_resource(self, key, obj) -> None:
        pass

    @abc.abstractmethod
    def get_resource(self, key):
        pass
