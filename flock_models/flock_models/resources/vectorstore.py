"""Resource for vectorstore."""

from typing import Any

from langchain.embeddings.base import Embeddings as EmbeddingsLC
from langchain.vectorstores.base import VectorStore as VectorStoreLC
from langchain.vectorstores.chroma import Chroma as ChromaLC

from flock_models.resources.base import Resource
from flock_models.schemes.base import FlockBaseSchema, Kind


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
        embedding_function: EmbeddingsLC = dependencies[Kind.embedding]

        self.resource = vendor_cls(
            **self.options,
            embedding_function=embedding_function.resource,
        )
