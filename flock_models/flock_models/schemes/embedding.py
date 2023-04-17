from typing import Optional
from pydantic import Field
from flock_models.schemes.base import FlockBaseSchema, BaseModelConfig, Kind


class EmbeddingSpec(BaseModelConfig):
    vendor: str = Field(..., description="Vendor of the LLM")
    options: Optional[dict] = Field(description="Options for the LLM")


class EmbeddingSchema(FlockBaseSchema):
    kind: str = Field(Kind.embedding.value, const=True, description="The kind of the object")
    spec: EmbeddingSpec
