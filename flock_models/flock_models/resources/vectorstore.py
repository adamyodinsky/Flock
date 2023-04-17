"""Resource for vectorstore."""

from typing import Any
from flock_models.resources.base import Resource
from langchain.vectorstores.base import VectorStoreLC
from langchain.embeddings.base import Embeddings as EmbeddingsLC
from flock_models.schemes.base import FlockBaseSchema, Kind
from langchain.vectorstores.chroma import Chroma as ChromaLC


class VectorStoreResource(Resource):
    """Class for vectorstore resources."""

    VENDORS = {"Chroma": ChromaLC}

    def __init__(
        self,
        manifest: FlockBaseSchema,
        dependencies: dict[str, Any],
    ):
        super().__init__(manifest, dependencies)
        vendor_cls: VectorStoreLC = self.VENDORS[self.vendor]
        embedding_function: EmbeddingsLC = dependencies[Kind.embedding.value]

        self.resource = vendor_cls(
            **self.options,
            embedding_function=embedding_function.resource,
        )
