"""Interface for embedding models."""

from typing import Any

from flock_models.resources.base import Resource
from langchain.embeddings.base import Embeddings
from langchain.embeddings.openai import OpenAIEmbeddings

class EmbeddingResource(Resource):
    """class for embedding resources."""

    VENDORS = {
        "OpenAIEmbeddings": OpenAIEmbeddings,
    }

    def __init__(
        self,
        vendor: str,
        options: dict[str, Any],
        dependencies: dict[str, Any] = None,
    ):
        embedding_cls = self.VENDORS[vendor]
        self.resource: Embeddings = embedding_cls(**options)
