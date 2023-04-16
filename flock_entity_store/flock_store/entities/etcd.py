"""Entity store class. This class is used to save and load entities to and from etcd."""""

import etcd3
import pickle
import json
from flock_store.entities.base import EntityStore
from flock_models.entities.base import Entity


class EtcdStore(EntityStore):
    """Entity store class. This class is used to save and load entities to and from the file system."""

    def __init__(self, host: str ='localhost', port: int = 2379, app_name: str = "flock", key_prefix: str = ""):
        super().__init__(
            app_name=app_name,
            key_prefix=key_prefix,
            is_fs=False
            )
        
        self.etcd_client = etcd3.client(host=host, port=port)


    def put(self, key, obj: Entity, manifest) -> None:
        data_key = f"{self.data_prefix}/{key}"
        manifest_key = f"{self.manifest_prefix}/{key}"

        serialized_obj = pickle.dumps(obj)
        self.etcd_client.put(data_key, serialized_obj)
        self.etcd_client.put(manifest_key, json.dumps(manifest))

    def get(self, key) -> tuple:
        data_key = f"{self.data_prefix}/{key}"
        manifest_key = f"{self.manifest_prefix}/{key}"

        serialized_obj, _ = self.etcd_client.get(data_key)
        manifest_str, _ = self.etcd_client.get(manifest_key)

        obj: Entity = pickle.loads(serialized_obj)
        manifest: dict = json.loads(manifest_str)
        return obj, manifest
    
    def put_manifest(self, key, manifest) -> None:
        self.etcd_client.put(f"{self.manifest_prefix}/{key}", json.dumps(manifest))

    def get_manifest(self, key) -> dict:
        manifest_str, _ = self.etcd_client.get(f"{self.manifest_prefix}/{key}")
        manifest: dict = json.loads(manifest_str)
        return manifest
    
    def put_data(self, key, obj: Entity) -> None:
        serialized_obj = pickle.dumps(obj)
        key = f"{self.data_prefix}/{key}"
        self.etcd_client.put(key, serialized_obj)

    def get_data(self, key) -> Entity:
        serialized_obj, _ = self.etcd_client.get(key)
        obj: Entity = pickle.loads(serialized_obj)
        return obj
    
    