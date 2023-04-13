from pydantic import Field
from flock_schemas.base import FlockBaseModel, Labels, BaseModelConfig

class Embedding(Labels):
    name: str = Field(..., description="Name of the embedding")

class Store(Labels):
    vendor: str = Field(..., description="The vendor of the vector store, e.g. chroma, pinecone, etc.")
    variant: str = Field(..., description="The type of the vector store", alias="type")
    path: str = Field(..., description="The path of the persistent vector store, can be a local path or a remote path")

class VectorStoreSpec(BaseModelConfig):
    store: Store
    embedding: Embedding

class VectorStore(FlockBaseModel):
    kind: str = Field("VectorStore", const=True)
    spec: VectorStoreSpec
