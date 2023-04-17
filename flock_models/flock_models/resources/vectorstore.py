"""Resource for vectorstore."""

from typing import Any
from flock_models.resources.base import Resource
from langchain.vectorstores.base import VectorStoreLC
from langchain.embeddings.base import Embeddings as EmbeddingsLC
from flock_models.schemes.base import Kind
from langchain.vectorstores.chroma import Chroma as ChromaLC


class VectorStoreResource(Resource):
    """Class for vectorstore resources."""

    VENDORS = {"Chroma": ChromaLC}

    def __init__(
        self,
        vendor: str,
        options: dict[str, Any],
        dependencies: dict[str, Any],
    ):
        vendor_cls: VectorStoreLC = self.VENDORS[vendor]
        embedding_function: EmbeddingsLC = dependencies[Kind.embedding.value]

        self.resource: vendor_cls(
            **options,
            embedding_function=embedding_function.resource,
        )
