from flock_store.resources.base import ResourceStore
from flock_store.resources.etcd import EtcdResourceStore
from flock_store.resources.fs import FSResourceStore

class ResourceStoreFactory:
    @staticmethod
    def get_resource_store(store_type: str, key_prefix: str) -> ResourceStore:
        if store_type == "etcd":
            return EtcdResourceStore(key_prefix)
        elif store_type == "fs":
            return FSResourceStore(key_prefix)
        else:
            raise ValueError(f"Invalid resource store type: {store_type}")
