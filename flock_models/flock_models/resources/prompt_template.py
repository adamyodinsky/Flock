"""Interface for LLM models."""

from typing import Dict, List, Optional, cast

from flock_schemas import PromptTemplateSchema
from langchain import PromptTemplate

from flock_models.resources.base import Resource, ToolResource


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
    ):
        super().__init__(manifest, dependencies, tools)
        self.vendor_cls: PromptTemplate = cast(
            PromptTemplate, self.VENDORS[self.vendor]
        )
        self.resource = self.vendor_cls(**self.options)  # type: ignore
