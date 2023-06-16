"""Interface for LLM models."""

from typing import Dict, List, Optional, cast

from langchain import PromptTemplate

from flock_resources.base import Resource, ToolResource
from flock_schemas.prompt_template import PromptTemplateSchema


class PromptTemplateResource(Resource):
    """Class for PromptTemplate resources."""

    VENDORS = {
        "PromptTemplate": PromptTemplate,
    }

    def __init__(
        self,
        manifest: PromptTemplateSchema,
        dependencies: Optional[Dict[str, Resource]],
        tools: Optional[List[ToolResource]] = None,
        dry_run: bool = False,
    ):
        super().__init__(manifest, dependencies, tools)
        self.vendor_cls: PromptTemplate = cast(
            PromptTemplate, self.VENDORS[self.vendor]
        )
        self.resource = self.vendor_cls(**self.options)  # type: ignore


export = {
    "PromptTemplate": PromptTemplateResource,
}
