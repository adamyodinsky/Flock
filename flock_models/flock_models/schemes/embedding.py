from enum import Enum
from typing import Optional

from pydantic import Field

from flock_models.schemes.base import BaseModelConfig, FlockBaseSchema, Kind


class EmbeddingVendor(str, Enum):
    """Enum for embedding vendors."""

    OpenAIEmbeddings = "OpenAIEmbeddings"


class EmbeddingSpec(BaseModelConfig):
    vendor: str = Field(..., description="Embedding vendor")
    options: Optional[dict] = Field(description="Embedding options")


class EmbeddingSchema(FlockBaseSchema):
    kind: str = Field(
        Kind.Embedding, const=True, description="The kind of the object"
    )
    spec: EmbeddingSpec
