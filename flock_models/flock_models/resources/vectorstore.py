"""Resource for vectorstore."""

from typing import Any
from flock_models.resources.base import Resource
from flock_models.resources.embedding import EmbeddingResource
from langchain.vectorstores.base import VectorStore
from flock_models.schemes.vectorstore import VectorStoreSchema
from flock_store.resources.base import ResourceStore
from flock_models.schemes.base import Kind

class VectorStoreResource(Resource):
    """Class for vectorstore resources."""

    def __init__(
            self,
            manifest: dict[str, Any],
            vectorstore: VectorStore,
            resource_store: ResourceStore,
                ):
        self.manifest = VectorStoreSchema(**manifest)
        embedding_key = f"{Kind.embedding.value}/{self.manifest.spec.embedding.name}"
        embedding_function: EmbeddingResource = resource_store.get_resource(embedding_key)

        self.resource: VectorStore = vectorstore(
            **self.manifest.spec.store.options,
            embedding_function=embedding_function.resource,
            )



# apiVersion: flock/v1
# kind: VectorStore
# metadata:
#   name: documentation_vectorstore
#   description: documentation vector store
#   annotations:
#     source: github.com://flockml/flockml
#   labels:
#     app: my_app
# spec:
#   store:
#     vendor: chroma
#     options: 
#       type: local
#       path: /home/flock/store/
#   embedding:
#     name: my-openai-embedding
#     labels:
#       app: my_app