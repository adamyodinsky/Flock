"""Resources store base class. This class is used to save and load entities."""
import abc
import json

import yaml


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
    def delete(self, key):
        """Delete a resource"""

    @staticmethod
    def load_file(path, file_type="yaml") -> dict:
        """Load a resource from the store."""

        val = None

        with open(file=path, mode="r", encoding="utf-8") as file:
            val = file.read()

        if file_type == "yaml" or file_type == "yml":
            val = yaml.load(val, Loader=yaml.FullLoader)
        elif file_type == "json":
            val = json.loads(val)
        else:
            raise ValueError(
                f"Invalid file type. Expected [yaml, yml, json], got {file_type}"
            )

        return val
