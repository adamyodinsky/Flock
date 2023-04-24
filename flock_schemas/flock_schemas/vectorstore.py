from enum import Enum
from typing import Literal, Optional

from pydantic import Field

from flock_schemas.base import BaseFlockSchema, BaseOptions, Kind
from flock_schemas.dependencies import EmbeddingDependency


class VectorStoreVendor(str, Enum):
    """Enum for vectorstore vendors."""

    Chroma = "Chroma"


class VectorStoreSpec(BaseOptions):
    vendor: str = Field(
        ..., description="The vendor of the vector store, e.g. Chroma, Pinecone, etc."
    )
    dependencies: tuple[EmbeddingDependency] = Field(
        ..., description="Vectorstore dependencies"
    )


class VectorStoreSchema(BaseFlockSchema):
    kind: Literal["VectorStore"] = Field(..., description="The kind of the object")
    spec: VectorStoreSpec
