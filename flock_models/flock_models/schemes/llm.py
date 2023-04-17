from typing import Optional
from pydantic import Field
from flock_models.schemes.base import FlockBaseSchema, BaseModelConfig, Kind
from enum import Enum


class LLMVendor(Enum):
    """Enum for llm vendors."""

    ChatOpenAI = "ChatOpenAI"


class LLMSpec(BaseModelConfig):
    vendor: LLMVendor = Field(..., description="LLM vendor")
    options: Optional[dict] = Field(description="LLM options")


class LLMSchema(FlockBaseSchema):
    kind: str = Field(Kind.llm.value, const=True, description="The kind of the object")
    spec: LLMSpec
