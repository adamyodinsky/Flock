"""Resource for vectorstore."""

from typing import Dict, List, Optional

from flock_schemas import LoadToolSchema
from flock_schemas.base import Kind
from langchain.agents import load_tools as load_toolsLC
from langchain.base_language import BaseLanguageModel as LCBaseLanguageModel

from flock_models.resources.base import Resource, ToolResource


class LoadToolResource(ToolResource):
    """Class for vectorstore qa tool."""

    VENDORS = [
        "python_repl"
        "requests"
        "requests_get"
        "requests_post"
        "requests_patch"
        "requests_put"
        "requests_delete"
        "terminal"
        "wolfram-alpha"
        "google-search"
        "google-search-results-json"
        "searx-search-results-json"
        "bing-search"
        "google-serper"
        "serpapi"
        "searx-search"
        "wikipedia"
        "human"
        "news-api"
        "tmdb-api"
        "podcast-api"
        "pal-math"
        "pal-colored-objects"
        "llm-math"
        "open-meteo-api"
    ]

    def __init__(
        self,
        manifest: LoadToolSchema,
        dependencies: Optional[Dict[str, Resource]],
        tools: Optional[List[ToolResource]] = None,
    ):
        super().__init__(manifest, dependencies)

        if tools is None:
            tools = []

        llm = self.dependencies.get(Kind.LLM) or self.dependencies.get(Kind.LLMChat)
        self.llm: LCBaseLanguageModel = llm.resource

        self.tool_function = load_toolsLC(
            tool_names=[self.vendor],
            llm=self.llm,
            **self.options,  # type: ignore
        )[0]

        self.resource = self.tool_function
