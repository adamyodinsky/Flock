"""Entity store base class. This class is used to save and load entities."""
import abc
import os
from flock_models.entities.base import Entity


class EntityStore(metaclass=abc.ABCMeta):
    """Abstract base class for entity stores."""

    def __init__(
        self, app_name: str = "flock", key_prefix: str = "", is_fs: bool = True
    ) -> None:
        """Initialize the entity store."""
        self.app_name = app_name

        if is_fs:
            self.init_fs(app_name, key_prefix)
        else:
            self.init_db(app_name, key_prefix)

        self.manifest_prefix = f"{self.key_prefix}/manifest"
        self.data_prefix = f"{self.key_prefix}/data"

    def init_fs(self, key_prefix: str = ""):
        if key_prefix is None:
            home_dir = os.path.expanduser("~")
            key_prefix = f"{home_dir}/.{self.app_name}"
        if not os.path.exists(key_prefix):
            os.makedirs(key_prefix)

        self.key_prefix = key_prefix

    def init_db(self, key_prefix: str = ""):
        if not key_prefix:
            self.key_prefix = f"/{self.app_name}"
        else:
            self.key_prefix = key_prefix

    @abc.abstractmethod
    def put(self, key, obj: Entity, manifest) -> None:
        pass

    @abc.abstractmethod
    def get(self, key) -> tuple:
        pass

    @abc.abstractmethod
    def put_manifest(self, key, manifest) -> None:
        pass

    @abc.abstractmethod
    def get_manifest(self, key) -> dict:
        pass

    @abc.abstractmethod
    def put_data(self, key, obj: Entity) -> None:
        pass

    @abc.abstractmethod
    def get_data(self, key) -> Entity:
        pass
