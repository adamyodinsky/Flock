import os

from flock_schema_store.base import SchemaStore
from flock_schema_store.mongo import MongoSchemaStore


class SchemaStoreFactory:
    """Factory class for schema stores"""

    Stores = {"mongo": MongoSchemaStore}

    @staticmethod
    def get_store(store_type: str = "mongo", **kwargs) -> SchemaStore:
        """Get a schema store based on the store type"""

        store: SchemaStore = NotImplemented

        try:
            store = SchemaStoreFactory.Stores[store_type](**kwargs)
        except KeyError as error:
            raise ValueError(f"Invalid store type: {store_type}") from error

        return store
