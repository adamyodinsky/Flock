from pydantic import Field
from flock_schemas.base import FlockBaseModel, Labels, BaseModelConfig


class Store(Labels):
    name: str = Field(..., description="Name of the store")

class LlmSpec(Labels):
    name: str = Field(..., description="Name of the Language Model")

class VectorStoreRetrieverToolSpec(BaseModelConfig):
    llm: LlmSpec
    store: Store
    chain_type: str = Field(..., description="The type of chain to be used")

class VectorStoreRetrieverTool(FlockBaseModel):
    kind: str = Field("VectorStoreRetrieverTool", const=True)
    spec: VectorStoreRetrieverToolSpec

