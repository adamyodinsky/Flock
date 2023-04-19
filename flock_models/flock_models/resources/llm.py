"""Interface for LLM models."""

from typing import Any
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseLanguageModel

from flock_models.resources.base import Resource
from flock_models.schemes.base import BaseFlockSchema


class LLMResource(Resource):
    """Class for LLM resources."""

    VENDORS = {
        "ChatOpenAI": ChatOpenAI,
    }

    def __init__(
        self,
        manifest: BaseFlockSchema,
        dependencies: dict[str, Any] = None,
    ):
        super().__init__(manifest)
        self.vendor_cls: BaseLanguageModel = self.VENDORS[self.vendor]
        self.resource = self.vendor_cls(**self.options)
