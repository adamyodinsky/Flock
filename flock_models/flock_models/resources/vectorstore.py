"""Resource for vectorstore."""

from typing import Any

from langchain.embeddings.base import Embeddings as EmbeddingsLC
from langchain.vectorstores.base import VectorStore as VectorStoreLC
from langchain.vectorstores.chroma import Chroma as ChromaLC

from flock_models.resources.base import Resource
from flock_models.schemes.base import BaseFlockSchema, Kind


class VectorStoreResource(Resource):
    """Class for vectorstore resources."""

    VENDORS = {"Chroma": ChromaLC}

    def __init__(
        self,
        manifest: BaseFlockSchema,
        dependencies: dict[str, Any],
    ):
        super().__init__(manifest, dependencies)
        self.vendor_cls: VectorStoreLC = self.VENDORS[self.vendor]
        self.embedding_function: EmbeddingsLC = dependencies[Kind.Embedding]

        self.resource = self.vendor_cls(
            **self.options,
            embedding_function=self.embedding_function,
        )
