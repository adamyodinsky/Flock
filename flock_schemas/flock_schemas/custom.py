"""Custom object schemas for Flock."""

from pydantic import Field

from flock_schemas.base import BaseFlockSchema


class CustomSchema(BaseFlockSchema):
    """Custom object schema."""

    kind: str = Field(..., description="The kind of the custom object")


export = {
    "sub": {},
    "main": {
        "CustomSchema": CustomSchema,
    },
}
