"""Resource for vectorstore."""

import logging
from typing import Dict, List, Optional, cast

import faiss
from flock_schemas.base import Kind
from flock_schemas.vectorstore import VectorStoreSchema
from langchain.docstore import InMemoryDocstore
from langchain.embeddings.base import Embeddings as EmbeddingsLC
from langchain.vectorstores import FAISS
from langchain.vectorstores.base import VectorStore as VectorStoreLC
from langchain.vectorstores.chroma import Chroma as ChromaLC

from flock_resources.base import Resource, ToolResource
from flock_resources.embedding import EmbeddingResource


class VectorStoreResource(Resource):
    """Class for vectorstore resources."""

    VENDORS = {"Chroma": ChromaLC}

    def __init__(
        self,
        manifest: VectorStoreSchema,
        dependencies: Optional[Dict[str, Resource]],
        tools: Optional[List[ToolResource]] = None,
        dry_run: bool = False,
    ):
        logging.debug(f"Initializing vectorstore resource: {manifest.metadata.name}")
        super().__init__(manifest, dependencies, tools, dry_run)
        self.vendor_cls: VectorStoreLC = cast(VectorStoreLC, self.VENDORS[self.vendor])
        self.embedding: EmbeddingResource = self.dependencies[Kind.Embedding]

        if self.dry_run:
            if "persist_directory" in self.options:  # type: ignore
                del self.options["persist_directory"]  # type: ignore

        self.resource = self.vendor_cls(  # type: ignore
            **self.options, embedding_function=self.embedding.resource
        )
        logging.debug(f"Initialized vectorstore resource: {manifest.metadata.name}")
        logging.debug(f"Vectorstore options: {self.options}")
        logging.debug(f"Vectorstore embedding: {self.embedding.manifest.metadata.name}")


class InMemVectorStoreResource(Resource):
    """Class for vectorstore resources."""

    VENDORS = {"Chroma": ChromaLC}
    DEFAULT_EMBEDDING_SIZE = 1536

    def __init__(
        self,
        manifest: VectorStoreSchema,
        dependencies: Optional[Dict[str, Resource]],
        tools: Optional[List[ToolResource]] = None,
        dry_run: bool = False,
    ):
        logging.debug(
            f"Initializing vectorstore in memory resource: {manifest.metadata.name}"
        )
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

        logging.debug(
            f"Initialized vectorstore in memory resource: {manifest.metadata.name}"
        )
        logging.debug(f"Vectorstore options: {self.options}")
        logging.debug(f"Vectorstore embedding: {self.embedding_function}")


export = {
    "InMemVectorStore": InMemVectorStoreResource,
    "VectorStore": VectorStoreResource,
}
