import os

from flock_common.env_checker import check_env_vars

from flock_deployer.config_store.base import ConfigStore
from flock_deployer.config_store.mongo import MongoConfigStore


class ConfigStoreFactory:
    """Factory class for config stores"""

    Stores = {"mongo": MongoConfigStore}

    @staticmethod
    def get_resource_store(store_type: str = "mongo", **kwargs) -> ConfigStore:
        """Get a resource store based on the store type"""

        # Check env vars
        required_vars = []
        optional_vars = ["STORE_TYPE"]
        check_env_vars(required_vars, optional_vars)
        store: ConfigStore = NotImplemented

        try:
            store = ConfigStoreFactory.Stores[os.environ.get("STORE_TYPE", store_type)](
                **kwargs
            )
        except KeyError as error:
            raise ValueError(f"Invalid store type: {store_type}") from error

        return store
