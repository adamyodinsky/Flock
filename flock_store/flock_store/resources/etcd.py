"""Entity store class. This class is used to save and load resources to and from etcd.""" ""

import json
import pickle

import etcd3

from flock_store.resources.base import ResourceStore


class EtcdStore(ResourceStore):
    """Entity store class. This class is used to save and load resources to and from the file system."""

    def __init__(
        self,
        key_prefix: str,
        host: str = "localhost",
        port: int = 2379,
    ):
        super().__init__(key_prefix)
        self.etcd_client = etcd3.client(host=host, port=port)

    def put(self, key, obj: object) -> None:
        key = f"{self.resource_prefix}/{key}"
        serialized_obj = pickle.dumps(obj)
        self.etcd_client.put(key, serialized_obj)

    def get(self, key) -> object:
        key = f"{self.resource_prefix}/{key}"
        serialized_obj, _ = self.etcd_client.get(key)
        obj: object = pickle.loads(serialized_obj)
        return obj
