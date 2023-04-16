from typing import Optional
from pydantic import Field
from flock_models.schemes.base import FlockBaseSchema, BaseModelConfig


class EmbeddingSpec(BaseModelConfig):
    vendor: str = Field(..., description="Vendor of the LLM")
    options: Optional[dict] = Field(description="Options for the LLM")


class EmbeddingSchema(FlockBaseSchema):
    kind: str = Field("Embedding", const=True, description="The kind of the object")
    spec: EmbeddingSpec
