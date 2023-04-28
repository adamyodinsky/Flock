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

    def get(self, key) -> dict:
        val = None
        key = f"{self.resource_prefix}/{key}"

        with open(file=key, mode="r", encoding="utf-8") as f:
            val = f.read()
            val = json.loads(val)

        return val

    def put(self, key, val: dict):
        key = f"{self.resource_prefix}/{key}"
        if not os.path.exists(os.path.dirname(key)):
            os.makedirs(os.path.dirname(key))

        with open(file=key, mode="w", encoding="utf-8") as f:
            json.dump(val, f, indent=2)

    # def get_model(self, key, schema: BaseModel) -> BaseModel:
    #     """Load a resource from the store."""

    #     key = f"{self.resource_prefix}/{key}"
    #     return schema.parse_file(key)

    # def put_model(self, key, val: BaseModel, _=None):
    #     """Save a resource to the store."""

    #     key = f"{self.resource_prefix}/{key}"
    #     json_instance = val.json().encode("utf-8")

    #     if not os.path.exists(os.path.dirname(key)):
    #         os.makedirs(os.path.dirname(key))

    #     with open(file=key, mode="wb") as f:
    #         f.write(json_instance)

    def load_file(self, path, file_type="yaml") -> dict:
        """Load a resource from the store."""

        val = None

        with open(file=path, mode="r", encoding="utf-8") as f:
            val = f.read()

        if file_type == "yaml" or file_type == "yml":
            val = yaml.load(val, Loader=yaml.FullLoader)
        elif file_type == "json":
            val = json.loads(val)
        else:
            raise ValueError(
                f"Invalid file type. Expected [yaml, yml, json], got {file_type}"
            )

        return val

    def get_many(self, key):
        """Get many resources with the same namespace and kind"""
