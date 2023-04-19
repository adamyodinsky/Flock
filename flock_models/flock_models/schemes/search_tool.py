from ast import List
from enum import Enum
from typing import Optional

from pydantic import Field

from flock_models.schemes.base import (
    BaseFlockSchema,
    Kind,
    BaseOptions
)

from flock_models.schemes.dependencies import LLMDependency

class SearchToolVendor(str, Enum):
    """Enum for search_tool vendors."""

    google_serper = "google-serper"
    google_search = "google-search"
    serpapi = "serpapi"
    google_search_results_json = "google-search-results-json"
    searx_search_results_json = "searx-search-results-json"
    

class SearchToolSpec(BaseOptions):
    vendor: SearchToolVendor = Field(
        ...,
        description="The name of the search tool, e.g. serpapi, google-serper, etc.",
    )
    dependencies: tuple[LLMDependency] = Field(..., description="Tool dependencies")


class SearchToolSchema(BaseFlockSchema):
    kind: str = Field(Kind.SearchTool, const=True)
    spec: SearchToolSpec
