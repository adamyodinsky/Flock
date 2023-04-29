"""Entity store class. This class is used to save and load resources to and from the file system."""

import json
import os

from flock_common import check_env_vars

from flock_resource_store.base import ResourceStore


class FSResourceStore(ResourceStore):
    """Entity store class. This class is used to save and load resources to and from the file system."""

    _shared_state = {}

    def __init__(self, path: str = "/tmp/.flock/resource_store"):
        # Implement the Borg design pattern
        self.__dict__ = self._shared_state

        # Check env vars
        required_vars = []
        optional_vars = ["FLOCK_RESOURCE_STORE_PATH"]

        check_env_vars(required_vars, optional_vars)

        # Initialize the client and db
        if not self._shared_state:
            self.resource_prefix = os.environ.get("FLOCK_RESOURCE_STORE_PATH", path)

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
