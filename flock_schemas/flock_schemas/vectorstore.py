"""Vectorstore schema."""
from enum import Enum
from typing import Literal

from pydantic import Field

from flock_schemas.base import BaseFlockSchema, BaseOptions
from flock_schemas.dependencies import EmbeddingDependency


class VectorStoreVendor(str, Enum):
    """Enum for vectorstore vendors."""

    Chroma = "Chroma"


class VectorStoreSpec(BaseOptions):
    """Vectorstore spec."""

    vendor: str = Field(
        ..., description="The vendor of the vector store, e.g. Chroma, Pinecone, etc."
    )
    dependencies: tuple[EmbeddingDependency] = Field(
        ..., description="Vectorstore dependencies"
    )


class VectorStoreSchema(BaseFlockSchema):
    """Vectorstore schema."""

    kind: Literal["VectorStore"] = Field(..., description="The kind of the object")
    spec: VectorStoreSpec
