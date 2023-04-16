"""Interface for embedding models."""

from typing import Any
from flock_models.schemes.embedding import EmbeddingSchema
from flock_models.entities.base import Entity
from langchain.embeddings.base import Embeddings
from flock_store.secrets.base import SecretStore


class EmbeddingEntity(Entity):
    """Base class for embedding entities."""

    def __init__(self, manifest: dict[str, Any], embedding: Embeddings):
        super().__init__(manifest, EmbeddingSchema)
        self.resource = embedding(**self.manifest.spec.options.dict())

    def set_api_token(self, key, secret_name: str, secret_store: SecretStore):
        self.resource[key] = secret_store.get(secret_name)
