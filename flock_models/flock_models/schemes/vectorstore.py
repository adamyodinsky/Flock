from enum import Enum
from typing import Optional

from pydantic import Field

from flock_models.schemes.base import (
    BaseModelConfig,
    Dependency,
    FlockBaseSchema,
    Kind,
    Options
)


class VectorStoreVendor(str, Enum):
    """Enum for vectorstore vendors."""

    Chroma = "Chroma"


class Embedding(Dependency):
    kind: str = Field(Kind.Embedding.value, const=True)


class VectorStoreSpec(Options):
    vendor: str = Field(
        ..., description="The vendor of the vector store, e.g. Chroma, Pinecone, etc."
    )
    dependencies: tuple[Embedding] = Field(..., description="Vectorstore dependencies")


class VectorStoreSchema(FlockBaseSchema):
    kind: str = Field(Kind.VectorStore, const=True)
    spec: VectorStoreSpec
