from typing import Optional, Tuple

from pymongo import MongoClient

from flock_resource_store.base import ResourceStore


class MongoResourceStore(ResourceStore):
    """MongoDB Resource Store"""

    _shared_state = {}

    def __init__(
        self,
        db_name: str,
        collection_name: str,
        host: str = "localhost",
        port: int = 27017,
        client: Optional[MongoClient] = None,
    ):
        # Implement the Borg design pattern
        self.__dict__ = self._shared_state

        if not self._shared_state:
            self.client = client or MongoClient(host, port)
            self.db = self.client[db_name]  # pylint: disable=invalid-name
            self.collection = self.db[collection_name]

    def put(self, key, val) -> None:
        namespace, kind, name = self.parse_key(key)
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
        namespace, kind, name = self.parse_key(key)
        result = self.collection.find_one(
            {
                "namespace": namespace,
                "kind": kind,
                "name": name,
            },
        )
        return result if result else None

    def delete(self, key):
        namespace, kind, name = self.parse_key(key)
        result = self.collection.delete_one(
            {
                "namespace": namespace,
                "kind": kind,
                "name": name,
            },
        )
        return result

    def parse_key(self, key: str) -> Tuple[str, str, str]:
        """Parsing key to namespace, kind, name"""

        keys = key.split("/")
        namespace = keys[0]
        kind = keys[1]
        name = keys[2]
        return namespace, kind, name
