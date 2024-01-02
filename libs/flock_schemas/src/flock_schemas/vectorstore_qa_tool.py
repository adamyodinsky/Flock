"""VectorStoreQATool schema."""

from enum import Enum
from typing import Dict, Literal, Optional, Union

from pydantic import Field

from flock_schemas.base import BaseSpec, BaseResourceSchema, Category
from flock_schemas.dependencies import (
    LLMChatDependency,
    LLMDependency,
    VectorStoreDependency,
)


class VectorStoreQAToolVendor(str, Enum):
    """Enum for vectorstore_qa_tool vendors."""

    RetrievalQAWithSourcesChain = "RetrievalQAWithSourcesChain"
    VectorDBQAWithSourcesChain = "VectorDBQAWithSourcesChain"


class VectorStoreQAToolSpec(BaseSpec):
    """VectorStoreQATool spec."""

    vendor: VectorStoreQAToolVendor = Field(
        ..., description="The class of the tool, e.g. RetrievalQAWithSourcesChain, etc."
    )
    options: Optional[Dict] = Field({}, description="Options for the tool")
    dependencies: tuple[VectorStoreDependency, LLMChatDependency] = Field(
        ..., description="Tool dependencies"
    )


class VectorStoreQAToolSchema(BaseResourceSchema):
    """VectorStoreQATool schema."""

    kind: Literal["VectorStoreQATool"] = Field(
        ..., description="The kind of the object"
    )
    tool: bool = Field(default=True, description="")
    category: Category = Field(
        default=Category.TOOL, description="The resource category"
    )
    spec: VectorStoreQAToolSpec


export = {
    "sub": {
        "VectorStoreQAToolSpec": VectorStoreQAToolSpec,
    },
    "main": {
        "VectorStoreQATool": VectorStoreQAToolSchema,
    },
}
