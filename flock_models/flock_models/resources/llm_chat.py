"""Interface for LLM models."""

from typing import List, Optional, cast

from flock_schemas import LLMSchema
from langchain.base_language import BaseLanguageModel
from langchain.chat_models import ChatOpenAI

from flock_models.resources.base import Resource, ToolResource


class LLMChatResource(Resource):
    """Class for LLM resources."""

    VENDORS = {"ChatOpenAI": ChatOpenAI}

    def __init__(
        self,
        manifest: LLMSchema,
        dependencies: Optional[dict[str, Resource]] = None,
        tools: Optional[List[ToolResource]] = None,
    ):
        super().__init__(manifest)
        self.vendor_cls: BaseLanguageModel = cast(
            BaseLanguageModel, self.VENDORS[self.vendor]
        )

        self.resource = self.vendor_cls(**self.options)  # type: ignore
