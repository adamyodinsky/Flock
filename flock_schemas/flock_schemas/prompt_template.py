"""PromptTemplate schema."""
from enum import Enum
from typing import Literal

from pydantic import Field

from flock_schemas.base import BaseFlockSchema, BaseOptions, Category


class PromptTemplateVendor(str, Enum):
    """Enum for prompt template vendors."""

    PromptTemplate = "PromptTemplate"


class PromptTemplateSpec(BaseOptions):
    """PromptTemplate spec."""

    vendor: PromptTemplateVendor = Field(..., description="PromptTemplate vendor")


class PromptTemplateSchema(BaseFlockSchema):
    """PromptTemplate schema."""

    kind: Literal["PromptTemplate"] = Field(..., description="The kind of the object")
    category: Category = Field(
        default=Category.OTHER, description="The resource category"
    )
    spec: PromptTemplateSpec


export = {
    "sub": {
        "PromptTemplateSpec": PromptTemplateSpec,
    },
    "main": {
        "PromptTemplateSchema": PromptTemplateSchema,
    },
}
