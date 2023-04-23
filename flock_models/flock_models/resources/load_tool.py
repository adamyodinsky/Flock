"""Resource for vectorstore."""

from typing import Any

from flock_schemas import LoadToolSchema
from flock_schemas.base import Kind
from langchain.agents import load_tools as load_toolsLC
from langchain.schema import BaseLanguageModel as LCBaseLanguageModel
from langchain.tools.base import BaseTool

from flock_models.resources.base import ToolResource


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
        dependencies: dict[str, Any],
        tools: list[Any] = [],
    ):
        super().__init__(manifest, dependencies)
        self.vendor_cls: BaseTool = self.vendor
        self.llm: LCBaseLanguageModel = self.dependencies[Kind.LLM].resource

        self.tool_function = load_toolsLC(
            tool_names=[self.vendor],
            llm=self.llm,
            **self.options,
        )[0]

        self.resource = self.tool_function
