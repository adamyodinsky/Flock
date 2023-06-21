"""Interface for LLM models."""

from typing import Dict, List, Optional

from flock_resources.base import CustomSchema, Resource, ToolResource
from flock_schemas.base import Kind


class WebScraperResource(Resource):
    """Class for Splitter resources."""

    def __init__(
        self,
        manifest: CustomSchema,
        dependencies: Optional[Dict[str, Resource]],
        tools: Optional[List[ToolResource]] = None,
        dry_run: bool = False,
    ):
        super().__init__(manifest, dependencies, tools, dry_run)
        self.resource = None
        self.vectorstore = self.dependencies.get(Kind.VectorStore).resource  # type: ignore


export = {
    "WebScraper": WebScraperResource,
}
