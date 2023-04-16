"""Entity store base class."""
import abc
import os

class EntityStore(metaclass=abc.ABCMeta):
    """Abstract base class for entity stores."""
    def __init__(self, app_name: str = "flock", key_prefix: str = "", is_fs: bool = True) -> None:
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
            home_dir = os.path.expanduser('~')
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
    def save(self, key, obj, manifest):
        pass

    @abc.abstractmethod
    def load(self, key):
        pass

    @abc.abstractmethod
    def save_manifest(self, key, manifest):
        pass

    @abc.abstractmethod
    def load_manifest(self, key):
        pass

    @abc.abstractmethod
    def save_data(self, key, obj):
        pass

    @abc.abstractmethod
    def load_data(self, key):
        pass
