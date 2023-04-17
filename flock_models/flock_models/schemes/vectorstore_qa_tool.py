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


class VectorStoreQAToolVendor(Enum):
    """Enum for vectorstore_qa_tool vendors."""

    RetrievalQAWithSourcesChain = "RetrievalQAWithSourcesChain"


class Store(Dependency):
    kind: str = Field(Kind.vectorstore.value, const=True)


class LLM(Dependency):
    kind: str = Field(Kind.llm.value, const=True)



class VectorStoreQAToolSpec(BaseModelConfig):
    vendor: VectorStoreQAToolVendor = Field(
        ..., description="The class of the tool, e.g. RetrievalQAWithSourcesChain, etc."
    )
    options: Optional[dict] = Field(description="Options for the tool")
    dependencies: tuple[Store, LLM] = Field(..., description="Tool dependencies")


class VectorStoreQAToolSchema(FlockBaseSchema):
    kind: str = Field(Kind.vectorstore_qa_tool.value, const=True)
    spec: VectorStoreQAToolSpec
