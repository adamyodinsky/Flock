from typing import Optional
from pydantic import Field
from flock_models.schemes.base import FlockBaseSchema, BaseModelConfig


class SplitterSpec(BaseModelConfig):
    variant: str = Field(..., description="Type of splitter", alias="type")
    options: Optional[dict] = Field(description="Options for the splitter")


class SplitterSchema(FlockBaseSchema):
    kind: str = Field("Splitter", const=True, description="The kind of the object")
    spec: SplitterSpec
