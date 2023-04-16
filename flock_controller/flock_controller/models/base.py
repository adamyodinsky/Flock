import abc
from typing import Any
from flock_entity_store.corncrete import EntityStore
from flock_schemas.base import FlockBaseModel

class Entity(metaclass=abc.ABCMeta):
    """Base class for all entities."""

    def __init__(self, manifest: dict[str, Any], schema: FlockBaseModel):
        self.manifest = schema(**manifest)
    
    @abc.abstractmethod
    def save(self, entity_store: EntityStore):
        pass
        # key = f"{self.kind}/{self.metadata.name}"
        # entity_store.save_data(key=key, obj=self)

    @abc.abstractmethod
    def load(self, entity_store: EntityStore):
        pass
        # key = f"{self.kind}/{self.metadata.name}"
        # entity_store.load_data(key=key)
