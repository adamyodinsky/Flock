"""Interface for embedding models."""

from typing import Any
from flock_models.schemes.embedding import EmbeddingSchema
from flock_models.entities.base import Entity
from langchain.embeddings.base import Embeddings
from langchain.embeddings.openai import OpenAIEmbeddings


class EmbeddingEntity(Entity):
    def __init__(self, manifest: dict[str, Any]):
        super().__init__(manifest, EmbeddingSchema)
        self.resource: Embeddings = None


class OpenAIEmbeddingEntity(EmbeddingEntity):
    def __init__(self, manifest: dict[str, Any]):
        super().__init__(manifest)
        self.resource = OpenAIEmbeddings(
            api_key=self.manifest.api_key,
            model=self.manifest.model,
            cache_dir=self.manifest.cache_dir,
        )

    def get_api_key(secret_name: str):
        return SecretStore.get_secret(secret_name)