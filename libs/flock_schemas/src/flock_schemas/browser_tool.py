from typing import Literal, Optional, Union

from pydantic import Field

from flock_schemas.base import BaseResourceSchema, BaseSpec, Category
from flock_schemas.dependencies import LLMChatDependency, LLMDependency


class BrowserToolSpec(BaseSpec):
    """BrowserTool spec."""

    dependencies: tuple[LLMChatDependency] = Field(..., description="Tool dependencies")


class BrowserToolSchema(BaseResourceSchema):
    """BrowserTool schema."""

    kind: Literal["BrowserTool"] = Field(..., description="The kind of the object")
    tool: bool = Field(default=True, description="")
    vendor: Optional[str] = Field(default="v1", description="")
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
