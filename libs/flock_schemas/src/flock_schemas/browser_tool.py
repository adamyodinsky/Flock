from typing import Literal, Union

from pydantic import Field

from flock_schemas.base import BaseResourceSchema, BaseSpec, Category
from flock_schemas.dependencies import LLMChatDependency, LLMDependency


class BrowserToolSpec(BaseSpec):
    """BrowserTool spec."""

    dependencies: tuple[Union[LLMDependency, LLMChatDependency]] = Field(
        ..., description="Tool dependencies"
    )


class BrowserToolSchema(BaseResourceSchema):
    """BrowserTool schema."""

    kind: Literal["BrowserTool"] = Field(..., description="The kind of the object")
    category: Category = Field(
        default=Category.TOOL, description="The resource category"
    )
    spec: BrowserToolSpec


export = {
    "sub": {
        "BrowserToolSpec": BrowserToolSpec,
    },
    "main": {
        "BrowserTool": BrowserToolSchema,
    },
}
