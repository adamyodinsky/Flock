"""Interface for embedding models."""

from typing import Any
from flock_models.schemes.embedding import EmbeddingSchema
from flock_models.resources.base import Resource
from langchain.embeddings.base import Embeddings
from flock_store.secrets.base import SecretStore


class EmbeddingResource(Resource):
    """class for embedding resources."""

    def __init__(self, manifest: dict[str, Any], embedding: Embeddings):
        self.manifest = EmbeddingSchema(**manifest)
        self.resource: Embeddings = embedding(**self.manifest.spec.options)

    def set_api_token(self, key, secret_name: str, secret_store: SecretStore):
        self.resource[key] = secret_store.get(secret_name)
