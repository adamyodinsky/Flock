"""Resource for vectorstore."""

from typing import Dict, List, Optional

from langchain.agents import load_tools as load_toolsLC

from flock_resources.base import Resource, ToolResource
from flock_schemas.load_tool import LoadToolSchema
from flock_schemas.base import Kind


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
        dry_run: bool = False,
    ):
        super().__init__(manifest, dependencies)

        if tools is None:
            tools = []

        self.llm = self.dependencies.get(Kind.LLM) or self.dependencies.get(
            Kind.LLMChat
        )

        self.tool_function = load_toolsLC(
            tool_names=[self.vendor],
            llm=self.llm.resource,  # type: ignore
            **self.options,  # type: ignore
        )[0]

        self.resource = self.tool_function


export = {
    "LoadTool": LoadToolResource,
}
