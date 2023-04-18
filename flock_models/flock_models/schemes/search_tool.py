from ast import List
from enum import Enum
from typing import Optional

from pydantic import Field

from flock_models.schemes.base import (
    BaseModelConfig,
    Dependency,
    FlockBaseSchema,
    Kind,
    Options
)


class SearchToolVendor(str, Enum):
    """Enum for search_tool vendors."""

    google_serper = "google-serper"
    google_search = "google-search"
    serpapi = "serpapi"
    google_search_results_json = "google-search-results-json"
    searx_search_results_json = "searx-search-results-json"
    

class LLM(Dependency):
    kind: str = Field(Kind.LLM, const=True)


class SearchToolSpec(Options):
    vendor: SearchToolVendor = Field(
        ...,
        description="The name of the search tool, e.g. serpapi, google-serper, etc.",
    )
    dependencies: tuple[LLM] = Field(..., description="Tool dependencies")


class SearchToolSchema(FlockBaseSchema):
    kind: str = Field(Kind.SearchTool, const=True)
    spec: SearchToolSpec
