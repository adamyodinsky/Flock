from enum import Enum
from typing import Optional

from pydantic import Field

from flock_models.schemes.base import (
    BaseFlockSchema,
    Kind,
    BaseOptions
)

from flock_models.schemes.dependencies import StoreDependency, LLMDependency

class VectorStoreQAToolVendor(str, Enum):
    """Enum for vectorstore_qa_tool vendors."""

    RetrievalQAWithSourcesChain = "RetrievalQAWithSourcesChain"


class VectorStoreQAToolSpec(BaseOptions):
    vendor: VectorStoreQAToolVendor = Field(
        ..., description="The class of the tool, e.g. RetrievalQAWithSourcesChain, etc."
    )
    options: Optional[dict] = Field({}, description="Options for the tool")
    dependencies: tuple[StoreDependency, LLMDependency] = Field(..., description="Tool dependencies")


class VectorStoreQAToolSchema(BaseFlockSchema):
    kind: str = Field(Kind.VectorStoreQATool, const=True)
    spec: VectorStoreQAToolSpec
