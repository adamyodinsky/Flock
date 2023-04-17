"""Entity store class. This class is used to save and load resources to and from the file system."""

import pickle
import json
from flock_store.resources.base import ResourceStore


class EntityStoreFS(ResourceStore):
    """Entity store class. This class is used to save and load resources to and from the file system."""

    def get_manifest(self, key) -> dict:
        key = f"{self.manifest_prefix}/{key}"
        with open(key, "r") as f:
            manifest = json.load(f)
        return manifest

    def put_manifest(self, key, manifest) -> None:
        key = f"{self.manifest_prefix}/{key}"
        with open(key, "w") as f:
            json.dump(manifest, f)

    def put_data(self, key, obj) -> None:
        serialized_obj = pickle.dumps(obj)
        key = f"{self.data_prefix}/{key}"
        with open(key, "wb") as f:
            f.write(serialized_obj)

    def put_data(self, key) -> object:
        key = f"{self.data_prefix}/{key}"
        with open(key, "rb") as f:
            serialized_obj = f.read()
        obj: object = pickle.loads(serialized_obj)
        return obj

    def put_resource(self, key, obj) -> None:
        serialized_obj = pickle.dumps(obj)
        key = f"{self.resource_prefix}/{key}"
        with open(key, "wb") as f:
            f.write(serialized_obj)

    def get_resource(self, key) -> object:
        key = f"{self.resource_prefix}/{key}"
        with open(key, "rb") as f:
            serialized_obj = f.read()
        obj: object = pickle.loads(serialized_obj)
        return obj
