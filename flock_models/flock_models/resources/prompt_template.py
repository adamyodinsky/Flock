"""Interface for LLM models."""

from typing import Any

from flock_schemas import PromptTemplateSchema
from langchain import PromptTemplate

from flock_models.resources.base import Resource


class PromptTemplateResource(Resource):
    """Class for PromptTemplate resources."""

    VENDORS = {
        "PromptTemplate": PromptTemplate,
    }

    def __init__(
        self,
        manifest: PromptTemplateSchema,
        dependencies: dict[str, Any] = None,
    ):
        super().__init__(manifest)
        self.vendor_cls: PromptTemplate = self.VENDORS[self.vendor]
        self.resource = self.vendor_cls(**self.options)
