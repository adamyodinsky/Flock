import os
from typing import Optional, Tuple

from flock_common import check_env_vars
from pymongo import MongoClient

from flock_resource_store.base import ResourceStore


class MongoResourceStore(ResourceStore):
    """MongoDB Resource Store"""

    _shared_state = {}

    def __init__(
        self,
        db_name: str = "flock_db",
        collection_name: str = "flock_resources",
        host: str = "localhost",
        port: int = 27017,
        client: Optional[MongoClient] = None,
    ):
        # Implement the Borg design pattern
        self.__dict__ = self._shared_state

        # Check env vars
        required_vars = ["MONGO_USERNAME", "MONGO_PASSWORD"]
        optional_vars = ["COLLECTION_NAME", "DB_NAME", "HOST", "PORT"]
        check_env_vars(required_vars, optional_vars)

        # Initialize the client and db
        if not self._shared_state:
            self.client = client or MongoClient(
                host=host,
                port=port,
                username=os.environ.get("MONGO_USERNAME"),
                password=os.environ.get("MONGO_PASSWORD"),
            )
            self.db = self.client[  # pylint: disable=invalid-name
                os.environ.get("DB_NAME", db_name)
            ]
            self.collection = self.db[
                os.environ.get("COLLECTION_NAME", collection_name)
            ]

    def put(self, key, val) -> None:
        namespace, kind, name = self.parse3(key)
        self.collection.update_one(
            {
                "namespace": namespace,
                "kind": kind,
                "name": name,
            },
            {"$set": val},
            upsert=True,
        )

    def get(self, key):
        namespace, kind, name = self.parse3(key)
        result = self.collection.find_one(
            {
                "namespace": namespace,
                "kind": kind,
                "name": name,
            },
        )
        return result if result else None

    def get_many(self, key):
        """Get many resources with the same namespace and kind"""

        namespace, kind = self.parse2(key)
        result = self.collection.find(
            filter={
                "namespace": namespace,
                "kind": kind,
            },
            projection={
                "namespace": True,
                "kind": True,
                "metadata.name": True,
            },
        ).limit(100)
        return result if result else None

    def delete(self, key):
        """Delete a resource"""

        namespace, kind, name = self.parse3(key)
        result = self.collection.delete_one(
            {
                "namespace": namespace,
                "kind": kind,
                "name": name,
            },
        )
        return result

    def parse3(self, key: str) -> Tuple[str, str, str]:
        """Parsing key to namespace, kind, name"""

        keys = key.split("/")
        namespace = keys[0]
        kind = keys[1]
        name = keys[2]
        return namespace, kind, name

    def parse2(self, key: str) -> Tuple[str, str]:
        """Parsing key to namespace, kind, name"""

        keys = key.split("/")
        namespace = keys[0]
        kind = keys[1]
        return namespace, kind
