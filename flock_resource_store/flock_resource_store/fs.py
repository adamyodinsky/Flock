"""Entity store class. This class is used to save and load resources to and from the file system."""

import json
import os

import yaml
from pydantic import BaseModel

from flock_resource_store.base import ResourceStore


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
            f.write(val)

    def get_model(self, key, schema: BaseModel) -> BaseModel:
        """Load a resource from the store."""

        key = f"{self.resource_prefix}/{key}"
        return schema.parse_file(key)

    def put_model(self, key, val: BaseModel, _=None):
        """Save a resource to the store."""

        key = f"{self.resource_prefix}/{key}"
        json_instance = val.json().encode("utf-8")

        if not os.path.exists(os.path.dirname(key)):
            os.makedirs(os.path.dirname(key))

        with open(file=key, mode="wb") as f:
            f.write(json_instance)

    def load_yaml(self, key, schema: BaseModel) -> BaseModel:
        """Load a resource from the store."""

        json_instance = self.yaml_to_json(key)
        return schema.parse_raw(json_instance, content_type="application/json")

    def yaml_to_json(self, file_path: str) -> str:
        """Convert yaml file to json string."""

        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            return json.dumps(data)
