"""Custom object schemas for Flock."""


from pydantic import Field

from schemas.base import BaseFlockSchema, Category


class CustomSchema(BaseFlockSchema):
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
