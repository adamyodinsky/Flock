"""Entity store class. This class is used to save and load resources to and from the file system."""

import os
import pickle
from pydantic import BaseModel

from flock_store.resources.base import ResourceStore


class FSResourceStore(ResourceStore):
    """Entity store class. This class is used to save and load resources to and from the file system."""

    def __init__(self, resource_prefix: str):
        self.resource_prefix = resource_prefix

    def get(self, key) -> str:
        key = f"{self.resource_prefix}/{key}"

        with open(file=key, mode="r") as f:
            return f.read()
        
    def put(self, key, val: str):
        key = f"{self.resource_prefix}/{key}"
        if not os.path.exists(os.path.dirname(key)):
            os.makedirs(os.path.dirname(key))
        
        with open(file=key, mode="w") as f:
            f.write(value)

    def get_model(self, key, schema: BaseModel) -> BaseModel:
        key = f"{self.resource_prefix}/{key}"
        return schema.parse_file(key)
        
    def put_model(self, key, val: BaseModel, _=None):
        key = f"{self.resource_prefix}/{key}"
        json_instance = val.json().encode("utf-8")

        if not os.path.exists(os.path.dirname(key)):
            os.makedirs(os.path.dirname(key))
        
        with open(file=key, mode="wb") as f:
            f.write(json_instance)
    
    def load_yaml(self, key, schema: BaseModel) -> BaseModel:
        json_instance = self.yaml_to_json(key)
        return schema.parse_raw(json_instance, content_type="application/json")
    
