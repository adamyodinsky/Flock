from enum import Enum
from typing import Optional

from pydantic import Field

from flock_models.schemes.base import BaseOptions, BaseFlockSchema, Kind


class LLMVendor(str, Enum):
    """Enum for llm vendors."""

    ChatOpenAI = "ChatOpenAI"


class LLMSpec(BaseOptions):
    vendor: LLMVendor = Field(..., description="LLM vendor")


class LLMSchema(BaseFlockSchema):
    kind: str = Field(Kind.LLM, const=True, description="The kind of the object")
    spec: LLMSpec
