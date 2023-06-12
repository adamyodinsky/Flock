"""Interface for LLM models."""

from typing import Dict, List, Optional

from flock_resources.base import CustomSchema, Resource, ToolResource


class WebScraperResource(Resource):
    """Class for Splitter resources."""

    def __init__(
        self,
        manifest: CustomSchema,
        dependencies: Optional[Dict[str, Resource]],
        tools: Optional[List[ToolResource]] = None,
    ):
        self.resource = None


export = {
    "WebScraper": WebScraperResource,
}
