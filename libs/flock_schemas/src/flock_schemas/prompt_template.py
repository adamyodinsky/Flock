"""PromptTemplate schema."""
from enum import Enum
from typing import Literal

from flock_schemas.base import BaseSpec, BaseResourceSchema, Category
from pydantic import Field


class PromptTemplateVendor(str, Enum):
    """Enum for prompt template vendors."""

    PromptTemplate = "PromptTemplate"


class PromptTemplateSpec(BaseSpec):
    """PromptTemplate spec."""

    vendor: PromptTemplateVendor = Field(..., description="PromptTemplate vendor")


class PromptTemplateSchema(BaseResourceSchema):
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
        "PromptTemplate": PromptTemplateSchema,
    },
}
