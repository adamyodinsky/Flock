"""Base class for all entities."""

import abc
from typing import Any
from flock_entity_store.base import EntityStore
from flock_models.schemes.base import FlockBaseSchema

class Entity(metaclass=abc.ABCMeta):
    """Base class for all entities."""

    def __init__(self, manifest: dict[str, Any], schema: FlockBaseSchema):
        self.manifest = schema(**manifest)
    
    def save(self, entity_store: EntityStore):
        key = f"{self.manifest.kind}/{self.manifest.metadata.name}"
        entity_store.save_data(key=key, obj=self)

    def load(self, entity_store: EntityStore):
        key = f"{self.manifest.kind}/{self.manifest.metadata.name}"
        entity_store.load_data(key=key)