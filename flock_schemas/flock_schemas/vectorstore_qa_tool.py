from enum import Enum
from typing import Literal, Optional

from pydantic import Field

from flock_schemas.base import BaseFlockSchema, BaseOptions, Kind
from flock_schemas.dependencies import LLMDependency, StoreDependency


class VectorStoreQAToolVendor(str, Enum):
    """Enum for vectorstore_qa_tool vendors."""

    RetrievalQAWithSourcesChain = "RetrievalQAWithSourcesChain"


class VectorStoreQAToolSpec(BaseOptions):
    vendor: VectorStoreQAToolVendor = Field(
        ..., description="The class of the tool, e.g. RetrievalQAWithSourcesChain, etc."
    )
    options: Optional[dict] = Field({}, description="Options for the tool")
    dependencies: tuple[StoreDependency, LLMDependency] = Field(
        ..., description="Tool dependencies"
    )


class VectorStoreQAToolSchema(BaseFlockSchema):
    kind: Literal["VectorStoreQATool"] = Field(
        ..., description="The kind of the object"
    )
    spec: VectorStoreQAToolSpec
