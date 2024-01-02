"""LLM schema."""

from enum import Enum
from typing import Literal

from flock_schemas.base import BaseSpec, BaseResourceSchema, Category
from pydantic import Field


class LLMVendor(str, Enum):
    """Enum for llm vendors."""

    GPT4All = "GPT4All"


class LLMSpec(BaseSpec):
    """LLM spec."""

    vendor: LLMVendor = Field(..., description="LLM vendor")


class LLMSchema(BaseResourceSchema):
    """LLM schema."""

    kind: Literal["LLM"] = Field(..., description="The kind of the object")
    category: Category = Field(
        default=Category.MODEL, description="The resource category"
    )
    spec: LLMSpec


export = {
    "sub": {
        "LLMSpec": LLMSpec,
    },
    "main": {
        "LLM": LLMSchema,
    },
}
