"""Resource for vectorstore."""

from typing import Any
from flock_models.schemes.llm import LLMSchema
from flock_models.resources.base import Resource
from langchain.vectorstores.base import VectorStore


class VectorStoreResource(Resource):
    """Base class for vectorestore."""

    def __init__(self, manifest: dict[str, Any], vectorstore: VectorStore):
        super().__init__(manifest, LLMSchema)
        self.resource = vectorstore(**self.manifest.spec.options.dict())



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