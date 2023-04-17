"""Entity store class. This class is used to save and load resources to and from the file system."""

import pickle
from flock_store.resources.base import ResourceStore
import os


class ResourceStoreFS(ResourceStore):
    """Entity store class. This class is used to save and load resources to and from the file system."""

    def put_resource(self, key, obj) -> None:
        serialized_obj = pickle.dumps(obj)
        key = f"{self.resource_prefix}/{key}"

        if not os.path.exists(os.path.dirname(key)):
            os.makedirs(os.path.dirname(key))

        with open(file=key, mode="wb") as f:
            f.write(serialized_obj)

    def get_resource(self, key) -> object:
        key = f"{self.resource_prefix}/{key}"
        with open(file=key, mode="rb") as f:
            serialized_obj = f.read()
        obj = pickle.loads(serialized_obj)
        return obj
