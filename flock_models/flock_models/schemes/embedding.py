from typing import Optional
from pydantic import Field
from flock_models.schemes.base import FlockBaseSchema, BaseModelConfig, Kind
from enum import Enum

class EmbeddingVendor(Enum):
    """Enum for embedding vendors."""

    OpenAIEmbeddings = "OpenAIEmbeddings"

class EmbeddingSpec(BaseModelConfig):
    vendor: str = Field(..., description="Embedding vendor")
    options: Optional[dict] = Field(description="Embedding options")


class EmbeddingSchema(FlockBaseSchema):
    kind: str = Field(
        Kind.embedding.value, const=True, description="The kind of the object"
    )
    spec: EmbeddingSpec
