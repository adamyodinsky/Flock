from typing import Optional

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from .base import SchemaStore


class MongoSchemaStore(SchemaStore):
    """MongoDB Config Store"""

    _shared_state = {}

    def __init__(
        self,
        username: str = "root",
        password: str = "password",
        db_name: str = "flock_db",
        table_name: str = "flock_schema",
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
            {"kind": val["kind"]},
            {"$set": val},
            upsert=True,
        )

    def get(
        self,
        kind: str = "",
    ):
        query_filter = MongoSchemaStore.create_filter(
            kind=kind,
        )

        result = self.table.find_one(filter=query_filter)

        result["id"] = str(result.get("_id"))
        del result["_id"]

        return result

    def get_many(
        self,
        page: int = 1,
        page_size: int = 50,
    ):
        """Get many resources with the same kind"""

        skip_count = (page - 1) * page_size

        result = self.table.find(filter={}).skip(skip_count).limit(page_size)

        result = list(result)

        for data in result:
            data["id"] = str(data.get("_id"))
            del data["_id"]

        return list(result)

    def delete(
        self,
        kind: str = "",
    ):
        """Delete a resource"""

        query_filter = MongoSchemaStore.create_filter(
            kind=kind,
        )

        result = self.table.delete_one(
            filter=query_filter,
        )
        return result

    def delete_many(
        self,
    ):
        """Delete a resource"""

        result = self.table.delete_many(filter={})
        return result

    def get_kinds(self) -> list:
        """Get all the kinds of schemas in the store as a list"""
        kinds = self.table.distinct("kind")
        return list(kinds)

    def health_check(self) -> bool:
        """Check if the resource store is healthy."""

        try:
            self.client.admin.command("ismaster")
            return True
        except ConnectionFailure:
            return False

    @staticmethod
    def create_filter(
        kind: str = "",
    ) -> dict:
        """Create a filter query"""

        filter_query = dict()
        if kind:
            filter_query["kind"] = kind

        return filter_query
