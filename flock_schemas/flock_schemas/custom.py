from typing import List, Optional

from pydantic import Extra, Field

from flock_schemas.base import (
    BaseDependency,
    BaseFlockSchema,
    BaseOptions,
    ToolDependency,
)


class CustomSpec(BaseOptions):
    vendor: Optional[str] = Field(description="The resource class")
    dependencies: Optional[List[BaseDependency]] = Field(
        [], description="Dependencies for the object"
    )
    tools: Optional[List[ToolDependency]] = Field(
        [], description="Tools for the object"
    )

    class Config:
        extra = Extra.allow


class CustomSchema(BaseFlockSchema):
    kind: str = Field(..., description="The kind of the custom object")
    spec: CustomSpec
