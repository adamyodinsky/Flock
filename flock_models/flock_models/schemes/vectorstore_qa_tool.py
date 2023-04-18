from enum import Enum
from typing import Optional

from pydantic import Field

from flock_models.schemes.base import (
    Dependency,
    FlockBaseSchema,
    Kind,
    Options
)


class VectorStoreQAToolVendor(str, Enum):
    """Enum for vectorstore_qa_tool vendors."""

    RetrievalQAWithSourcesChain = "RetrievalQAWithSourcesChain"


class Store(Dependency):
    kind: str = Field(Kind.VectorStore, const=True)


class LLM(Dependency):
    kind: str = Field(Kind.LLM, const=True)


class VectorStoreQAToolSpec(Options):
    vendor: VectorStoreQAToolVendor = Field(
        ..., description="The class of the tool, e.g. RetrievalQAWithSourcesChain, etc."
    )
    options: Optional[dict] = Field({}, description="Options for the tool")
    dependencies: tuple[Store, LLM] = Field(..., description="Tool dependencies")


class VectorStoreQAToolSchema(FlockBaseSchema):
    kind: str = Field(Kind.VectorStoreQATool, const=True)
    spec: VectorStoreQAToolSpec
