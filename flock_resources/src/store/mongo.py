from typing import Optional

from pymongo import MongoClient

from store.base import ResourceStore


class MongoResourceStore(ResourceStore):
    """MongoDB Resource Store"""

    _shared_state = {}

    def __init__(
        self,
        username: str = "root",
        password: str = "password",
        db_name: str = "flock_db",
        collection_name: str = "flock_resources",
        host: str = "localhost",
        port: int = 27017,
        client: Optional[MongoClient] = None,
    ):
        # Implement the Borg design pattern
        self.__dict__ = self._shared_state

        # Initialize the client and db
        if not self._shared_state:
            self.client = client or MongoClient(
                host=host,
                port=port,
                username=username,
                password=password,
            )
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]

    def put(self, val: dict) -> None:
        self.collection.update_one(
            {
                "namespace": val["namespace"],
                "kind": val["kind"],
                "metadata.name": val["metadata"]["name"],
            },
            {"$set": val},
            upsert=True,
        )

    def get(
        self,
        category: str = "",
        namespace: str = "",
        name: str = "",
        kind: str = "",
    ):
        query_filter = MongoResourceStore.create_filter(
            category=category,
            namespace=namespace,
            name=name,
            kind=kind,
        )

        result = self.collection.find_one(
            filter=query_filter,
            projection={
                "_id": False,
            },
        )
        return result

    def get_many(
        self,
        category: str = "",
        namespace: str = "",
        name: str = "",
        kind: str = "",
        page: int = 1,
        page_size: int = 50,
    ):
        """Get many resources with the same namespace and kind"""

        skip_count = (page - 1) * page_size
        filter_query = {}
        if namespace:
            filter_query["namespace"] = namespace
        if category:
            filter_query["category"] = category
        if kind:
            filter_query["kind"] = kind
        if name:
            filter_query["metadata.name"] = name

        result = (
            self.collection.find(
                filter=filter_query,
                projection={
                    "name": "$metadata.name",
                    "description": "$metadata.description",
                    "kind": True,
                    "category": True,
                    "namespace": True,
                },
            )
            .skip(skip_count)
            .limit(page_size)
        )
        return result

    def delete(
        self,
        category: str = "",
        namespace: str = "",
        name: str = "",
        kind: str = "",
    ):
        """Delete a resource"""

        query_filter = MongoResourceStore.create_filter(
            category=category,
            namespace=namespace,
            name=name,
            kind=kind,
        )

        result = self.collection.delete_one(
            filter=query_filter,
        )
        return result

    def delete_many(
        self,
        category: str = "",
        namespace: str = "",
        name: str = "",
        kind: str = "",
    ):
        """Delete a resource"""

        query_filter = MongoResourceStore.create_filter(
            category=category,
            namespace=namespace,
            name=name,
            kind=kind,
        )

        result = self.collection.delete_many(
            filter=query_filter,
        )
        return result

    @staticmethod
    def create_filter(
        category: str = "",
        namespace: str = "",
        name: str = "",
        kind: str = "",
    ) -> dict:
        """Create a filter query"""

        filter_query = {}
        if namespace:
            filter_query["namespace"] = namespace
        if category:
            filter_query["category"] = category
        if kind:
            filter_query["kind"] = kind
        if name:
            filter_query["metadata.name"] = name

        return filter_query
