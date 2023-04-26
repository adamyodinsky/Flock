from flock_resource_store.base import ResourceStore
from flock_resource_store.fs import FSResourceStore


class ResourceStoreFactory:
    @staticmethod
    def get_resource_store(store_type: str, key_prefix: str) -> ResourceStore:
        if store_type == "fs":
            return FSResourceStore(key_prefix)
        else:
            raise ValueError(f"Invalid resource store type: {store_type}")
