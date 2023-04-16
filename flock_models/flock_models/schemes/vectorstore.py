from typing import Optional
from pydantic import Field
from flock_models.schemes.base import FlockBaseSchema, Labels, BaseModelConfig


class Embedding(Labels):
    name: str = Field(..., description="Name of the embedding")


class Store(BaseModelConfig):
    vendor: str = Field(
        ..., description="The vendor of the vector store, e.g. chroma, pinecone, etc."
    )
    options: Optional[dict] = Field(description="Options for the vector store")

class VectorStoreSpec(BaseModelConfig):
    store: Store
    embedding: Embedding


class VectorStoreSchema(FlockBaseSchema):
    kind: str = Field("VectorStore", const=True)
    spec: VectorStoreSpec
