from flock_deployer.config_store.base import ConfigStore
from flock_deployer.config_store.mongo import MongoConfigStore


class ConfigStoreFactory:
    """Factory class for config stores"""

    Stores = {"mongo": MongoConfigStore}

    @staticmethod
    def get_store(store_type: str = "mongo", **kwargs) -> ConfigStore:
        """Get a config store based on the store type"""

        store: ConfigStore = NotImplemented

        try:
            store = ConfigStoreFactory.Stores[store_type](**kwargs)
        except KeyError as error:
            raise ValueError(f"Invalid store type: {store_type}") from error

        return store
