from enum import Enum
from typing import Literal, Union

from pydantic import Field

from flock_schemas.base import BaseOptions, BaseResourceSchema, BaseSpec, Category
from flock_schemas.dependencies import LLMChatDependency, LLMDependency


class CSVToolSpec(BaseSpec):
    """CSVTool spec."""

    dependencies: tuple[Union[LLMDependency, LLMChatDependency]] = Field(
        ..., description="Tool dependencies"
    )


class CSVToolSchema(BaseResourceSchema):
    """CSVTool schema."""

    kind: Literal["CSVTool"] = Field(..., description="The kind of the object")
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
