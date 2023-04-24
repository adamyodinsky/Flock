from enum import Enum
from typing import Literal, Optional

from pydantic import Field

from flock_schemas.base import BaseFlockSchema, BaseOptions
from flock_schemas.dependencies import LLMDependency, PromptTemplateDependency


class LLMToolVendor(str, Enum):
    """Enum for LLM tool vendors."""

    LLMChain = "LLMChain"


class LLMToolSpec(BaseOptions):
    vendor: LLMToolVendor = Field(
        ..., description="The class of the tool, e.g. LLMChain, etc."
    )
    options: Optional[dict] = Field({}, description="Options for the tool")
    dependencies: tuple[PromptTemplateDependency, LLMDependency] = Field(
        ..., description="Tool dependencies"
    )


class LLMToolSchema(BaseFlockSchema):
    kind: Literal["LLMTool"] = Field(..., description="The kind of the object")
    spec: LLMToolSpec
