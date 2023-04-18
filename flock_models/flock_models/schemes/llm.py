from enum import Enum
from typing import Optional

from pydantic import Field

from flock_models.schemes.base import Options, FlockBaseSchema, Kind


class LLMVendor(str, Enum):
    """Enum for llm vendors."""

    ChatOpenAI = "ChatOpenAI"


class LLMSpec(Options):
    vendor: LLMVendor = Field(..., description="LLM vendor")


class LLMSchema(FlockBaseSchema):
    kind: str = Field(Kind.LLM, const=True, description="The kind of the object")
    spec: LLMSpec
