"""Custom object schemas for Flock."""


from typing import Optional

from pydantic import Field

from flock_schemas.base import BaseResourceSchema, Category


class CustomSchema(BaseResourceSchema):
    """Custom object schema."""

    kind: str = Field(..., description="The kind of the custom object")
    vendor: Optional[str] = Field(default="v1", description="")
    category: Category = Field(
        default=Category.OTHER, description="The resource category"
    )


export = {
    "sub": {},
    "main": {
        "Custom": CustomSchema,
    },
}
