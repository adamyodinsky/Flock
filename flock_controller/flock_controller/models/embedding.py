"""Interface for embedding models."""

from typing import Any
from flock_schemas.embedding import Embedding as EmbeddingSchema
from flock_controller.models.base import Entity
from langchain.embeddings.base import Embeddings


class EmbeddingEntity(Entity):  
    def __init__(self, manifest: dict[str, Any]):
        super().__init__(manifest, EmbeddingSchema)
        self.resource: Embeddings = None
        
    def save(self, entity_store):
        key = f"{self.manifest.kind}/{self.manifest.metadata.name}"
        entity_store.save_data(key=key, obj=self)
    
    def load(self, entity_store):
        key = f"{self.manifest.kind}/{self.manifest.metadata.name}"
        entity_store.load_data(key=key)
