from typing import Optional
from pydantic import Field
from base import FlockBaseModel, BaseModelConfig

class EmbeddingSpec(BaseModelConfig):
    vendor: str = Field(..., description="Vendor of the LLM")
    model: str = Field(..., description="Name of the LLM model")
    token_limit: int = Field(..., description="Token limit for the LLM")
    embedding_ctx_length: Optional[int] = Field(description="Embedding context length")
    chunk_size: Optional[int] = Field(description="Chunk size")
    
class Embedding(FlockBaseModel):
    kind: str = Field("Embedding", const=True, description="The kind of the object")
    spec: EmbeddingSpec


# apiVersion: flock/v1
# kind: Embedding
# metadata:
#   name: my-openai-embedding
#   description: openai embedding
#   labels:
#     app: my_app
# spec:
#   vendor: openai
#   model: text-embedding-ada-002
#   token_limit: 1000
#   embedding_ctx_length: 4096
#   chunk_size: 1000
