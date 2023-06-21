"""Custom object schemas for Flock."""


from flock_schemas.base import BaseResourceSchema, Category
from pydantic import Field


class CustomSchema(BaseResourceSchema):
    """Custom object schema."""

    kind: str = Field(..., description="The kind of the custom object")
    category: Category = Field(
        default=Category.OTHER, description="The resource category"
    )


export = {
    "sub": {},
    "main": {
        "Custom": CustomSchema,
    },
}
