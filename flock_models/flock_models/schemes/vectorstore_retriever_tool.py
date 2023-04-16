from typing import Optional
from pydantic import Field
from flock_models.schemes.base import FlockBaseSchema, Labels, BaseModelConfig


class Store(Labels):
    name: str = Field(..., description="Name of the store")


class LLM(Labels):
    name: str = Field(..., description="Name of the Language Model")


class VectorStoreRetrieverToolSpec(BaseModelConfig):
    llm: LLM
    store: Store
    options: Optional[dict] = Field(description="Options for the tool")


class VectorStoreRetrieverToolSchema(FlockBaseSchema):
    kind: str = Field("VectorStoreRetrieverTool", const=True)
    spec: VectorStoreRetrieverToolSpec
