from flock_resource_store.base import ResourceStore
from flock_resource_store.fs import FSResourceStore
from flock_resource_store.mongo import MongoResourceStore


class ResourceStoreFactory:
    @staticmethod
    def get_resource_store(store_type: str, key_prefix: str, **kwargs) -> ResourceStore:
        if store_type == "fs":
            return FSResourceStore(key_prefix)
        elif store_type == "mongo":
            return MongoResourceStore(**kwargs)
        else:
            raise ValueError(f"Invalid resource store type: {store_type}")
