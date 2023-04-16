"""Base class for all resources."""

from typing import Any
from flock_store.resources.base import ResourceStore
from flock_models.schemes.base import FlockBaseSchema


class Resource:
    """Base class for all resources."""

    def __init__(self, manifest: dict[str, Any], schema: FlockBaseSchema):
        self.manifest = schema(**manifest)

    def put(self, resource_store: ResourceStore):
        key = f"{self.manifest.kind}/{self.manifest.metadata.name}"
        resource_store.put_data(key=key, obj=self)

    def get(self, resource_store: ResourceStore):
        key = f"{self.manifest.kind}/{self.manifest.metadata.name}"
        resource_store.get_data(key=key)


class Tool(Resource):
    """Base class for all tools."""

    def __init__(self, manifest: dict[str, Any], schema: FlockBaseSchema):
        super().__init__(manifest, schema)