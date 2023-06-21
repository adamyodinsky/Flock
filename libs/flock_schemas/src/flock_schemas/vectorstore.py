"""Vectorstore schema."""

from enum import Enum
from typing import Literal

from flock_schemas.base import BaseOptions, BaseResourceSchema, Category
from flock_schemas.dependencies import EmbeddingDependency
from pydantic import Field


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


class VectorStoreSchema(BaseResourceSchema):
    """Vectorstore schema."""

    kind: Literal["VectorStore"] = Field(..., description="The kind of the object")
    category: Category = Field(
        default=Category.OTHER, description="The resource category"
    )
    spec: VectorStoreSpec


export = {
    "sub": {
        "VectorStoreSpec": VectorStoreSpec,
    },
    "main": {
        "VectorStore": VectorStoreSchema,
    },
}
