"""Resource for vectorstore."""

from typing import Dict, List, Optional, cast

import faiss
from langchain.docstore import InMemoryDocstore
from langchain.embeddings.base import Embeddings as EmbeddingsLC
from langchain.vectorstores import FAISS
from langchain.vectorstores.base import VectorStore as VectorStoreLC
from langchain.vectorstores.chroma import Chroma as ChromaLC

from resources.base import Resource, ToolResource
from schemas.vectorstore import VectorStoreSchema
from schemas.base import Kind


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


class InMemVectorStoreResource(Resource):
    """Class for vectorstore resources."""

    VENDORS = {"Chroma": ChromaLC}
    DEFAULT_EMBEDDING_SIZE = 1536

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

        # Initialize the vectorstore as empty
        embedding_size = getattr(
            self.manifest.spec.options, "embedding_size", self.DEFAULT_EMBEDDING_SIZE
        )
        index = faiss.IndexFlatL2(embedding_size)
        vectorstore = FAISS(
            self.embedding_function.embed_query, index, InMemoryDocstore({}), {}
        )

        self.resource = vectorstore
        self.memory = vectorstore.as_retriever()


export = {
    "InMemVectorStore": InMemVectorStoreResource,
    "VectorStore": VectorStoreResource,
}
