"""Interface for LLM models."""

from typing import Any
from flock_models.resources.base import Resource
from langchain.schema import BaseLanguageModel
from langchain.chat_models import ChatOpenAI


class LLMResource(Resource):
    """Class for LLM resources."""

    VENDORS = {
        "ChatOpenAI": ChatOpenAI,
    }

    def __init__(
        self,
        vendor: str,
        options: dict[str, Any],
        dependencies: dict[str, Any] = None,
    ):
        llm_cls: BaseLanguageModel = self.VENDORS[vendor]
        self.resource = llm_cls(**options)
