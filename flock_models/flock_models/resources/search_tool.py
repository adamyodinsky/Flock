"""Resource for vectorstore."""

from typing import Any

from langchain.agents import Tool as ToolWarperLC
from langchain.tools.base import BaseTool
from langchain.schema import BaseLanguageModel as LCBaseLanguageModel
from langchain.agents import load_tools as load_toolsLC

from flock_models.resources.base import ToolResource
from flock_models.schemes.base import FlockBaseSchema, Kind


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
            manifest: FlockBaseSchema,
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
