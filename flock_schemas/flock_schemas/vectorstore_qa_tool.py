"""VectorStoreQATool schema."""

from enum import Enum
from typing import Dict, Literal, Optional, Union

from pydantic import Field

from flock_schemas.base import BaseFlockSchema, BaseOptions, Category
from flock_schemas.dependencies import LLMChatDependency, LLMDependency, StoreDependency


class VectorStoreQAToolVendor(str, Enum):
    """Enum for vectorstore_qa_tool vendors."""

    RetrievalQAWithSourcesChain = "RetrievalQAWithSourcesChain"


class VectorStoreQAToolSpec(BaseOptions):
    """VectorStoreQATool spec."""

    vendor: VectorStoreQAToolVendor = Field(
        ..., description="The class of the tool, e.g. RetrievalQAWithSourcesChain, etc."
    )
    options: Optional[Dict] = Field({}, description="Options for the tool")
    dependencies: tuple[
        StoreDependency, Union[LLMChatDependency, LLMDependency]
    ] = Field(..., description="Tool dependencies")


class VectorStoreQAToolSchema(BaseFlockSchema):
    """VectorStoreQATool schema."""

    kind: Literal["VectorStoreQATool"] = Field(
        ..., description="The kind of the object"
    )
    category: Category = Field(
        default=Category.OTHER, description="The resource category"
    )
    spec: VectorStoreQAToolSpec


export = {
    "sub": {
        "VectorStoreQAToolSpec": VectorStoreQAToolSpec,
    },
    "main": {
        "VectorStoreQAToolSchema": VectorStoreQAToolSchema,
    },
}
