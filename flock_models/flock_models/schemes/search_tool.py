from ast import List
from typing import Optional
from pydantic import Field
from flock_models.schemes.base import (
    FlockBaseSchema,
    Labels,
    BaseModelConfig,
    Kind,
    Dependency,
)

from enum import Enum

class SearchToolVendor(Enum):
    """Enum for search_tool vendors."""
    google_serper = "google-serper"
    serpapi = "serpapi"


class LLM(Dependency):
    kind: str = Field(Kind.llm.value, const=True)


class SearchToolSpec(BaseModelConfig):
    vendor: SearchToolVendor = Field(
        ..., description="The name of the search tool, e.g. serpapi, google-serper, etc."
    )
    options: Optional[dict] = Field(description="Tool options")
    dependencies: tuple[LLM] = Field(..., description="Tool dependencies")


class SearchToolSchema(FlockBaseSchema):
    kind: str = Field(Kind.search_tool.value, const=True)
    spec: SearchToolSpec
