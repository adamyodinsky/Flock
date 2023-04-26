from typing import Optional

from pydantic import BaseModel
from pymongo import MongoClient

from flock_resource_store.base import ResourceStore


class MongoResourceStore(ResourceStore):
    def __init__(
        self,
        db_name: str,
        collection_name: str,
        host: str = "localhost",
        port: int = 27017,
    ):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def put(self, key, obj) -> None:
        self.collection.update_one({"_id": key}, {"$set": obj}, upsert=True)

    def get(self, key):
        result = self.collection.find_one({"_id": key})
        return result if result else None

    def get_model(self, key, schema: BaseModel) -> BaseModel:
        result = self.get(key)
        if result:
            return schema(**result)
        return None

    def put_model(self, key, val: BaseModel, ttl: Optional[int] = None):
        data = val.dict()
        if ttl:
            data["_ttl"] = {"$gt": datetime.utcnow() - timedelta(seconds=ttl)}
        self.put(key, data)
