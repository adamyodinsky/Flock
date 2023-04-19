from enum import Enum
from typing import Optional

from pydantic import Field

from flock_models.schemes.base import (
    BaseFlockSchema,
    Kind,
    BaseOptions
)

from flock_models.schemes.dependencies import EmbeddingDependency

class VectorStoreVendor(str, Enum):
    """Enum for vectorstore vendors."""

    Chroma = "Chroma"



class VectorStoreSpec(BaseOptions):
    vendor: str = Field(
        ..., description="The vendor of the vector store, e.g. Chroma, Pinecone, etc."
    )
    dependencies: tuple[EmbeddingDependency] = Field(..., description="Vectorstore dependencies")


class VectorStoreSchema(BaseFlockSchema):
    kind: str = Field(Kind.VectorStore, const=True)
    spec: VectorStoreSpec
