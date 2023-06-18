from typing import Optional

from pymongo import MongoClient

from .base import ConfigStore


class MongoConfigStore(ConfigStore):
    """MongoDB Config Store"""

    _shared_state = {}

    def __init__(
        self,
        username: str = "root",
        password: str = "password",
        db_name: str = "flock_db",
        table_name: str = "flock_config",
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
            self.table = self.db[table_name]

    def put(self, val: dict) -> None:
        self.table.update_one(
            {
                "kind": val["kind"],
                "metadata.name": val["metadata"]["name"],
            },
            {"$set": val},
            upsert=True,
        )

    def get(
        self,
        category: str = "",
        name: str = "",
        kind: str = "",
    ):
        query_filter = MongoConfigStore.create_filter(
            category=category,
            name=name,
            kind=kind,
        )

        result = self.table.find_one(
            filter=query_filter,
            projection={
                "_id": False,
            },
        )
        return result

    def get_many(
        self,
        category: str = "",
        name: str = "",
        kind: str = "",
        page: int = 1,
        page_size: int = 50,
    ):
        """Get many resources with the same kind"""

        skip_count = (page - 1) * page_size
        filter_query = {}
        if category:
            filter_query["category"] = category
        if kind:
            filter_query["kind"] = kind
        if name:
            filter_query["metadata.name"] = name

        result = (
            self.table.find(
                filter=filter_query,
                projection={
                    "name": "$metadata.name",
                    "description": "$metadata.description",
                    "kind": True,
                    "category": True,
                },
            )
            .skip(skip_count)
            .limit(page_size)
        )
        return result

    def delete(
        self,
        category: str = "",
        name: str = "",
        kind: str = "",
    ):
        """Delete a resource"""

        query_filter = MongoConfigStore.create_filter(
            category=category,
            name=name,
            kind=kind,
        )

        result = self.table.delete_one(
            filter=query_filter,
        )
        return result

    def delete_many(
        self,
        category: str = "",
        name: str = "",
        kind: str = "",
    ):
        """Delete a resource"""

        query_filter = MongoConfigStore.create_filter(
            category=category,
            name=name,
            kind=kind,
        )

        result = self.table.delete_many(
            filter=query_filter,
        )
        return result

    @staticmethod
    def create_filter(
        category: str = "",
        name: str = "",
        kind: str = "",
    ) -> dict:
        """Create a filter query"""

        filter_query = {}
        if category:
            filter_query["category"] = category
        if kind:
            filter_query["kind"] = kind
        if name:
            filter_query["metadata.name"] = name

        return filter_query
