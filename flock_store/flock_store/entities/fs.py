"""Entity store class. This class is used to save and load entities to and from the file system."""

import pickle
import json
from flock_store.entities.base import EntityStore
from flock_models.entities.base import Entity


class EntityStoreFS(EntityStore):
    """Entity store class. This class is used to save and load entities to and from the file system."""

    def put(self, key, obj: Entity, manifest) -> None:
        data_key = f"{self.data_prefix}/{key}"
        manifest_key = f"{self.manifest_prefix}/{key}"
        serialized_obj = pickle.dumps(obj)

        with open(data_key, "wb") as f:
            f.write(serialized_obj)
        with open(manifest_key, "w") as f:
            json.dump(manifest, f)

    def get(self, key) -> tuple:
        data_key = f"{self.data_prefix}/{key}"
        manifest_key = f"{self.manifest_prefix}/{key}"

        with open(data_key, "rb") as f:
            serialized_obj = f.read()
        obj = pickle.loads(serialized_obj)
        with open(manifest_key, "r") as f:
            manifest = json.load(f)
        return obj, manifest

    def get_manifest(self, key) -> dict:
        with open(f"{self.manifest_prefix}/{key}", "r") as f:
            manifest = json.load(f)
        return manifest

    def put_manifest(self, key, manifest) -> None:
        with open(f"{self.manifest_prefix}/{key}", "w") as f:
            json.dump(manifest, f)

    def put_data(self, key, obj) -> None:
        serialized_obj = pickle.dumps(obj)
        with open(f"{self.data_prefix}/{key}", "wb") as f:
            f.write(serialized_obj)

    def put_data(self, key) -> Entity:
        with open(f"{self.data_prefix}/{key}", "rb") as f:
            serialized_obj = f.read()
        obj: Entity = pickle.loads(serialized_obj)
        return obj
