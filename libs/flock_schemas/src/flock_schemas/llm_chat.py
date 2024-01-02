"""LLMChat schema."""

from enum import Enum
from typing import Literal

from pydantic import Field

from flock_schemas.base import BaseSpec, BaseResourceSchema, Category


class LLMChatVendor(str, Enum):
    """Enum for llm vendors."""

    ChatOpenAI = "ChatOpenAI"
    OpenAICopyCat = "OpenAICopyCat"


class LLMChatSpec(BaseSpec):
    """LLMChat spec."""

    vendor: LLMChatVendor = Field(..., description="LLMChat vendor")


class LLMChatSchema(BaseResourceSchema):
    """LLMChat schema."""

    kind: Literal["LLMChat"] = Field(..., description="The kind of the object")
    category: Category = Field(
        default=Category.MODEL, description="The resource category"
    )
    spec: LLMChatSpec


export = {
    "sub": {
        "LLMChatSpec": LLMChatSpec,
    },
    "main": {
        "LLMChat": LLMChatSchema,
    },
}
