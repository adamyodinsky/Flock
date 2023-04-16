from typing import Optional
from pydantic import Field
from flock_models.schemes.base import FlockBaseSchema, BaseModelConfig


class LLMSpec(BaseModelConfig):
    vendor: str = Field(..., description="Vendor of the LLM")
    options: Optional[dict] = Field(description="Options for the LLM")


class LLMSchema(FlockBaseSchema):
    kind: str = Field("LLM", const=True, description="The kind of the object")
    spec: LLMSpec
