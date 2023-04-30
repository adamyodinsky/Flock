"""LLM schema."""

from enum import Enum
from typing import List, Literal

from pydantic import Field

from flock_schemas.base import BaseFlockSchema, BaseOptions, Category


class LLMVendor(str, Enum):
    """Enum for llm vendors."""

    ChatOpenAI = "ChatOpenAI"


class LLMSpec(BaseOptions):
    """LLM spec."""

    vendor: LLMVendor = Field(..., description="LLM vendor")


class LLMSchema(BaseFlockSchema):
    """LLM schema."""

    kind: Literal["LLM"] = Field(..., description="The kind of the object")
    categories: List[Category] = Field(
        default=[Category.MODEL], description="The resource category"
    )
    spec: LLMSpec


export = {
    "sub": {
        "LLMSpec": LLMSpec,
    },
    "main": {
        "LLMSchema": LLMSchema,
    },
}
