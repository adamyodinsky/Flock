"""Resource for vectorstore."""

from typing import Any

from flock_schemas import VectorStoreSchema
from flock_schemas.base import Kind
from langchain.embeddings.base import Embeddings as EmbeddingsLC
from langchain.vectorstores.base import VectorStore as VectorStoreLC
from langchain.vectorstores.chroma import Chroma as ChromaLC


from flock_models.resources.base import Resource


class VectorStoreResource(Resource):
    """Class for vectorstore resources."""

    VENDORS = {"Chroma": ChromaLC}

    def __init__(
        self,
        manifest: VectorStoreSchema,
        dependencies: dict[str, Any],
        tools: list[Any] = [],
    ):
        super().__init__(manifest, dependencies)
        self.vendor_cls: VectorStoreLC = self.VENDORS[self.vendor]
        self.embedding_function: EmbeddingsLC = dependencies[Kind.Embedding].resource

        self.resource = self.vendor_cls(
            **self.options,
            embedding_function=self.embedding_function,
        )
