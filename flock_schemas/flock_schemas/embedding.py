"""Embedding schema."""

from enum import Enum
from typing import Dict, Literal, Optional

from pydantic import Field

from flock_schemas.base import BaseFlockSchema, BaseOptions


class EmbeddingVendor(str, Enum):
    """Enum for embedding vendors."""

    OpenAIEmbeddings = "OpenAIEmbeddings"


class EmbeddingSpec(BaseOptions):
    """Embedding spec."""

    vendor: EmbeddingVendor = Field(..., description="Embedding vendor")
    options: Optional[Dict] = Field(description="Embedding options")


class EmbeddingSchema(BaseFlockSchema):
    """Embedding schema."""

    kind: Literal["Embedding"] = Field(..., description="The kind of the object")
    spec: EmbeddingSpec


export = {
    "sub": {
        "EmbeddingSpec": EmbeddingSpec,
    },
    "main": {
        "EmbeddingSchema": EmbeddingSchema,
    },
}
