"""Interface for LLM models."""

from typing import Any

from flock_schemas import LLMSchema
from flock_schemas.base import BaseFlockSchema
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseLanguageModel

from flock_models.resources.base import Resource


class LLMResource(Resource):
    """Class for LLM resources."""

    VENDORS = {
        "ChatOpenAI": ChatOpenAI,
    }

    def __init__(
        self,
        manifest: LLMSchema,
        dependencies: dict[str, Any] = None,
        tools: list[Any] = [],
    ):
        super().__init__(manifest)
        self.vendor_cls: BaseLanguageModel = self.VENDORS[self.vendor]
        self.resource = self.vendor_cls(**self.options)
