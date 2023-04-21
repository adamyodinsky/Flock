"""Resource for vectorstore."""

from typing import Any

from flock_schemas import SearchToolSchema
from flock_schemas.base import Kind
from langchain.agents import load_tools as load_toolsLC
from langchain.schema import BaseLanguageModel as LCBaseLanguageModel
from langchain.tools.base import BaseTool

from flock_models.resources.base import ToolResource


class SearchToolResource(ToolResource):
    """Class for vectorstore qa tool."""

    VENDORS = [
        "google-search-results-json"
        "searx-search-results-json"
        "google-search"
        "google-serper"
        "serpapi"
    ]

    def __init__(
        self,
        manifest: SearchToolSchema,
        dependencies: dict[str, Any],
    ):
        super().__init__(manifest, dependencies)
        self.vendor_cls: BaseTool = self.vendor
        self.llm: LCBaseLanguageModel = self.dependencies[Kind.LLM]

        self.tool_function = load_toolsLC(
            tool_names=[self.vendor],
            llm=self.llm,
            **self.options,
        )[0]

        self.resource = self.tool_function
