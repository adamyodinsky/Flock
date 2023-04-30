import os

from flock_common.env_checker import check_env_vars

from flock_resource_store.base import ResourceStore
from flock_resource_store.mongo import MongoResourceStore


class ResourceStoreFactory:
    """Factory class for resource stores"""

    Stores = {"mongo": MongoResourceStore}

    @staticmethod
    def get_resource_store(store_type: str = "fs", **kwargs) -> ResourceStore:
        """Get a resource store based on the store type"""

        # Check env vars
        required_vars = []
        optional_vars = ["FLOCK_RESOURCE_STORE_TYPE"]
        check_env_vars(required_vars, optional_vars)
        store: ResourceStore = NotImplemented

        try:
            store = ResourceStoreFactory.Stores[
                os.environ.get("FLOCK_RESOURCE_STORE_TYPE", store_type)
            ](**kwargs)
        except KeyError as error:
            raise ValueError(f"Invalid store type: {store_type}") from error

        return store
