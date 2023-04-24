from enum import Enum
from typing import Literal, Optional

from pydantic import Field

from flock_schemas.base import BaseFlockSchema, BaseOptions, Kind


class EmbeddingVendor(str, Enum):
    """Enum for embedding vendors."""

    OpenAIEmbeddings = "OpenAIEmbeddings"


class EmbeddingSpec(BaseOptions):
    vendor: EmbeddingVendor = Field(..., description="Embedding vendor")
    options: Optional[dict] = Field(description="Embedding options")


class EmbeddingSchema(BaseFlockSchema):
    kind: Literal["Embedding"] = Field(..., description="The kind of the object")
    spec: EmbeddingSpec
