"""LLM Tool schema."""

from enum import Enum
from typing import Dict, Literal, Optional, Union

from flock_schemas.base import BaseOptions, BaseResourceSchema, Category
from flock_schemas.dependencies import (
    LLMChatDependency,
    LLMDependency,
    PromptTemplateDependency,
)
from pydantic import Field


class LLMToolVendor(str, Enum):
    """Enum for LLM tool vendors."""

    LLMChain = "LLMChain"


class LLMToolSpec(BaseOptions):
    """LLM tool spec."""

    vendor: LLMToolVendor = Field(
        ..., description="The class of the tool, e.g. LLMChain, etc."
    )
    options: Optional[Dict] = Field({}, description="Options for the tool")
    dependencies: tuple[
        PromptTemplateDependency, Union[LLMDependency, LLMChatDependency]
    ] = Field(..., description="Tool dependencies")


class LLMToolSchema(BaseResourceSchema):
    """LLM tool schema."""

    kind: Literal["LLMTool"] = Field(..., description="The kind of the object")
    category: Category = Field(
        default=Category.TOOL, description="The resource category"
    )
    spec: LLMToolSpec


export = {
    "sub": {
        "LLMToolSpec": LLMToolSpec,
    },
    "main": {
        "LLMTool": LLMToolSchema,
    },
}
