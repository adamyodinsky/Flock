"""Resource for vectorstore."""

from typing import Any
from flock_models.resources.base import Resource
from flock_models.resources.embedding import EmbeddingResource
from langchain.vectorstores.base import VectorStore
from langchain.embeddings.base import Embeddings as EmbeddingsLC
from flock_models.schemes.vectorstore import VectorStoreSchema, VectorStoreVendor
from flock_store.resources.base import ResourceStore
from flock_models.schemes.base import Kind
from langchain.vectorstores.chroma import Chroma as ChromaLC


class VectorStoreResource(Resource):
    """Class for vectorstore resources."""
    
    CHAINS_CLS = {
        "Chroma": ChromaLC
    }
    
    def __init__(
        self,
        options: dict[str, Any],
        dependencies: dict[str, Any],
        vendor: str
    ):
        embedding_function: EmbeddingsLC = dependencies[Kind.embedding.value]
        vendor_cls = self.CHAINS_CLS[VectorStoreVendor[vendor].value]
        
        self.resource: VectorStore = vendor_cls(
            **self.manifest.spec.store.options,
            embedding_function=embedding_function.resource,
        )

# apiVersion: flock/v1
# kind: VectorStore
# metadata:
#   name: documentation_vectorstore
#   description: documentation vector store
#   annotations:
#     source: github.com/floc/flock.html
# spec:
#   vendor: Chroma
#   options:
#     persist_directory: './.documentation_vectorstore'
#     collection_name: 'documentation'
#   dependencies:
#     - kind: Embedding
#       name: my-openai-embedding
#       namespace: default
