from enum import Enum
from typing import Optional

from pydantic import Field

from flock_models.schemes.base import (
    BaseModelConfig,
    Dependency,
    FlockBaseSchema,
    Kind,
    Labels,
)


class VectorStoreVendor(str, Enum):
    """Enum for vectorstore vendors."""

    Chroma = "Chroma"


class Embedding(Dependency):
    kind: str = Field(Kind.Embedding.value, const=True)


class VectorStoreSpec(BaseModelConfig):
    vendor: str = Field(
        ..., description="The vendor of the vector store, e.g. Chroma, Pinecone, etc."
    )
    options: Optional[dict] = Field(description="Vectorstore options")
    dependencies: tuple[Embedding] = Field(..., description="Vectorstore dependencies")


class VectorStoreSchema(FlockBaseSchema):
    kind: str = Field(Kind.VectorStore, const=True)
    spec: VectorStoreSpec
