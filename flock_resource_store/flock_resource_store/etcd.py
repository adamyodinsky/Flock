"""Etcd resource store class. This class is used to save and load resources to and from etcd.""" ""

import etcd
from pydantic import BaseModel

from flock_resource_store.base import ResourceStore


class EtcdResourceStore(ResourceStore):
    """Etcd resource store class. This class is used to save and load resources to and from etcd.""" ""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 4003,
        protocol: str = "http",
        version_prefix: str = "/v2",
    ):
        self.client = etcd.client(host=host, port=port, protocol=protocol, version_prefix=version_prefix)

    def get(self, key, schema: BaseModel) -> BaseModel:
        json_instance = self.client.get(key)
        if json_instance is not None:
            return schema.parse_raw(json_instance)
        return None
    
    def put(self, key, instance: BaseModel, ttl=None):
        json_instance = instance.json()
        self.client.set(key, json_instance, ttl=ttl)

