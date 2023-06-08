"""Interface for embedding models."""

from typing import Dict, List, Optional

from langchain.embeddings.base import Embeddings as EmbeddingsLC
from langchain.embeddings.openai import OpenAIEmbeddings as OpenAIEmbeddingsLC

from resources.base import Resource, ToolResource
from schemas.embedding import EmbeddingSchema


class EmbeddingResource(Resource):
    """class for embedding resources."""

    VENDORS = {"OpenAIEmbeddings": OpenAIEmbeddingsLC}

    def __init__(
        self,
        manifest: EmbeddingSchema,
        dependencies: Optional[Dict[str, Resource]],
        tools: Optional[List[ToolResource]] = None,
    ):
        super().__init__(manifest, dependencies, tools)
        self.vendor_cls = self.VENDORS[self.vendor]
        self.resource: EmbeddingsLC = self.vendor_cls(**self.options)  # type: ignore
        self.functions = {
            "embed_query": self.resource.embed_query,
            "embed_documents": self.resource.embed_documents,
        }


export = {
    "Embedding": EmbeddingResource,
}
