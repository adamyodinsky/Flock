from typing import Optional
from pydantic import Field
from flock_models.schemes.base import FlockBaseSchema, BaseModelConfig

class EmbeddingSpec(BaseModelConfig):
    vendor: str = Field(..., description="Vendor of the LLM")
    model: str = Field(..., description="Name of the LLM model")
    token_limit: int = Field(..., description="Token limit for the LLM")
    embedding_ctx_length: Optional[int] = Field(description="Embedding context length")
    chunk_size: Optional[int] = Field(description="Chunk size")
    
class EmbeddingSchema(FlockBaseSchema):
    kind: str = Field("Embedding", const=True, description="The kind of the object")
    spec: EmbeddingSpec
