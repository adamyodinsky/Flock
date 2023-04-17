"""Entity store class. This class is used to save and load resources to and from etcd.""" ""

import etcd3
import pickle
import json
from flock_store.resources.base import ResourceStore


class EtcdStore(ResourceStore):
    """Entity store class. This class is used to save and load resources to and from the file system."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 2379,
        app_name: str = "flock",
        key_prefix: str = "",
    ):
        super().__init__(app_name=app_name, key_prefix=key_prefix, is_fs=False)

        self.etcd_client = etcd3.client(host=host, port=port)

    def put_manifest(self, key, manifest) -> None:
        key = f"{self.manifest_prefix}/{key}"
        self.etcd_client.put(key, json.dumps(manifest))

    def get_manifest(self, key) -> dict:
        key = f"{self.manifest_prefix}/{key}"
        manifest_str, _ = self.etcd_client.get(key)
        manifest: dict = json.loads(manifest_str)
        return manifest

    def put_data(self, key, obj: object) -> None:
        key = f"{self.data_prefix}/{key}"
        serialized_obj = pickle.dumps(obj)
        self.etcd_client.put(key, serialized_obj)

    def get_data(self, key) -> object:
        key = f"{self.data_prefix}/{key}"
        serialized_obj, _ = self.etcd_client.get(key)
        obj: object = pickle.loads(serialized_obj)
        return obj

    def put_resource(self, key, obj: object) -> None:
        key = f"{self.resource_prefix}/{key}"
        serialized_obj = pickle.dumps(obj)
        self.etcd_client.put(key, serialized_obj)

    def get_resource(self, key) -> object:
        key = f"{self.resource_prefix}/{key}"
        serialized_obj, _ = self.etcd_client.get(key)
        obj: object = pickle.loads(serialized_obj)
        return obj