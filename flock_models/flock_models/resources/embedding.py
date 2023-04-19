"""Interface for embedding models."""

from typing import Any
from langchain.embeddings.base import Embeddings as EmbeddingsLC
from langchain.embeddings.openai import OpenAIEmbeddings as OpenAIEmbeddingsLC

from flock_models.resources.base import Resource
from flock_schemas.embedding import EmbeddingSchema


class EmbeddingResource(Resource):
    """class for embedding resources."""

    VENDORS = {
        "OpenAIEmbeddings": OpenAIEmbeddingsLC,
    }

    def __init__(
        self,
        manifest: EmbeddingSchema,
        dependencies: dict[str, Any] = None,
    ):
        super().__init__(manifest)
        self.vendor_cls = self.VENDORS[self.vendor]
        self.resource: EmbeddingsLC = self.vendor_cls(**self.options)
