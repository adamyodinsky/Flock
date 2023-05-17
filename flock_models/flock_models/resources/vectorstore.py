"""Resource for vectorstore."""

from typing import Dict, List, Optional, cast

from flock_models.resources.base import Resource, ToolResource
from flock_schemas import VectorStoreSchema
from flock_schemas.base import Kind
from langchain.embeddings.base import Embeddings as EmbeddingsLC
from langchain.vectorstores.base import VectorStore as VectorStoreLC
from langchain.vectorstores.chroma import Chroma as ChromaLC


class VectorStoreResource(Resource):
    """Class for vectorstore resources."""

    VENDORS = {"Chroma": ChromaLC}

    def __init__(
        self,
        manifest: VectorStoreSchema,
        dependencies: Optional[Dict[str, Resource]],
        tools: Optional[List[ToolResource]] = None,
    ):
        super().__init__(manifest, dependencies, tools)
        self.vendor_cls: VectorStoreLC = cast(VectorStoreLC, self.VENDORS[self.vendor])
        self.embedding_function: EmbeddingsLC = cast(
            EmbeddingsLC, self.dependencies[Kind.Embedding].resource
        )

        self.resource = self.vendor_cls(  # type: ignore
            **self.options,
            embedding_function=self.embedding_function,
        )
