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

    def get_many(self, key):
        """Get many resources with the same namespace and kind"""
