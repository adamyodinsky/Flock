from typing import Literal, Optional, Union

from pydantic import Field

from flock_schemas.base import BaseResourceSchema, BaseSpec, Category
from flock_schemas.dependencies import LLMChatDependency, LLMDependency


class CSVToolSpec(BaseSpec):
    """CSVTool spec."""

    dependencies: tuple[LLMChatDependency] = Field(..., description="Tool dependencies")


class CSVToolSchema(BaseResourceSchema):
    """CSVTool schema."""

    kind: Literal["CSVTool"] = Field(..., description="The kind of the object")
    tool: bool = Field(default=True, description="")
    vendor: Optional[str] = Field(default="v1", description="")
    category: Category = Field(
        default=Category.TOOL, description="The resource category"
    )
    spec: CSVToolSpec


export = {
    "sub": {
        "CSVToolSpec": CSVToolSpec,
    },
    "main": {
        "CSVTool": CSVToolSchema,
    },
}
