from typing import Optional
from pydantic import Field
from flock_models.schemes.base import (
    FlockBaseSchema,
    Labels,
    BaseModelConfig,
    Kind,
    Dependency,
)

from enum import Enum

class VectorStoreVendor(Enum):
    """Enum for all kinds of resources."""
    Chroma = "Chroma"

class Embedding(Dependency):
    kind: str = Field(Kind.embedding.value, const=True)


class Dependencies(Labels):
    Embedding


class VectorStoreSpec(BaseModelConfig):
    vendor: str = Field(
        ..., description="The vendor of the vector store, e.g. chroma, pinecone, etc."
    )
    options: Optional[dict] = Field(description="Options for the vector store")
    dependencies: Dependencies = Field(
        ..., description="Dependencies for the vector store"
    )

class VectorStoreSchema(FlockBaseSchema):
    kind: str = Field(Kind.vectorstore.value, const=True)
    spec: VectorStoreSpec
