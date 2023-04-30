"""LoadTool schema."""
from enum import Enum
from typing import List, Literal

from pydantic import Field

from flock_schemas.base import BaseFlockSchema, BaseOptions, Category
from flock_schemas.dependencies import LLMDependency


class LoadToolVendor(str, Enum):
    """Enum for search_tool vendors."""

    python_repl = "python_repl"
    requests = "requests"
    requests_get = "requests_get"
    requests_post = "requests_post"
    requests_patch = "requests_patch"
    requests_put = "requests_put"
    requests_delete = "requests_delete"
    terminal = "terminal"
    wolfram_alpha = "wolfram-alpha"
    google_search = "google-search"
    google_search_results_json = "google-search-results-json"
    searx_search_results_json = "searx-search-results-json"
    bing_search = "bing-search"
    google_serper = "google-serper"
    serpapi = "serpapi"
    searx_search = "searx-search"
    wikipedia = "wikipedia"
    human = "human"
    news_api = "news-api"
    tmdb_api = "tmdb-api"
    podcast_api = "podcast-api"
    pal_math = "pal-math"
    pal_colored_objects = "pal-colored-objects"
    llm_math = "llm-math"
    open_meteo_api = "open-meteo-api"


class LoadToolSpec(BaseOptions):
    """LoadTool spec."""

    vendor: LoadToolVendor = Field(
        ...,
        description="The name of the search tool, e.g. serpapi, google-serper, etc.",
    )
    dependencies: tuple[LLMDependency] = Field(..., description="Tool dependencies")


class LoadToolSchema(BaseFlockSchema):
    """LoadTool schema."""

    kind: Literal["LoadTool"] = Field(..., description="The kind of the object")
    category: Category = Field(
        default=Category.TOOL, description="The resource category"
    )
    spec: LoadToolSpec


export = {
    "sub": {
        "LoadToolSpec": LoadToolSpec,
    },
    "main": {
        "LoadToolSchema": LoadToolSchema,
    },
}
