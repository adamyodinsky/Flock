"""Resources store base class. This class is used to save and load entities."""
import abc
import yaml
import json
from pydantic import BaseModel


class ResourceStore(metaclass=abc.ABCMeta):
    """Abstract base class for resource stores."""

    @abc.abstractmethod
    def put(self, key, obj) -> None:
        pass


    @abc.abstractmethod
    def get(self, key):
        pass

    
    @abc.abstractmethod
    def get_model(self, key, schema: BaseModel) -> BaseModel:
        pass


    @abc.abstractmethod
    def put_model(self, key, val: BaseModel, ttl=None):
        pass


    def yaml_to_json(self, file_path: str) -> str:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return json.dumps(data)
