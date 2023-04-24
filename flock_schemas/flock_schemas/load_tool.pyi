from enum import Enum
from flock_schemas.base import BaseFlockSchema as BaseFlockSchema, BaseOptions as BaseOptions
from flock_schemas.dependencies import LLMDependency as LLMDependency
from typing import Literal

class LoadToolVendor(str, Enum):
    python_repl: str
    requests: str
    requests_get: str
    requests_post: str
    requests_patch: str
    requests_put: str
    requests_delete: str
    terminal: str
    wolfram_alpha: str
    google_search: str
    google_search_results_json: str
    searx_search_results_json: str
    bing_search: str
    google_serper: str
    serpapi: str
    searx_search: str
    wikipedia: str
    human: str
    news_api: str
    tmdb_api: str
    podcast_api: str
    pal_math: str
    pal_colored_objects: str
    llm_math: str
    open_meteo_api: str

class LoadToolSpec(BaseOptions):
    vendor: LoadToolVendor
    dependencies: tuple[LLMDependency]

class LoadToolSchema(BaseFlockSchema):
    kind: Literal['LoadTool']
    spec: LoadToolSpec
