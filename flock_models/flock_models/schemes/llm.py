from typing import Optional
from pydantic import Field
from flock_models.schemes.base import FlockBaseSchema, BaseModelConfig, Kind
from enum import Enum

class LLMVendor(Enum):
    """Enum for all kinds of resources."""
    openai = "openai"


class LLMSpec(BaseModelConfig):
    vendor: LLMVendor = Field(..., description="Vendor of the LLM")
    options: Optional[dict] = Field(description="Options for the LLM")


class LLMSchema(FlockBaseSchema):
    kind: str = Field(Kind.llm.value, const=True, description="The kind of the object")
    spec: LLMSpec
