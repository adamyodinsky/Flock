"""Interface for LLM models."""

from typing import List, Optional, cast

from langchain.base_language import BaseLanguageModel
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    BaseMessage,
    ChatGeneration,
    ChatMessage,
    ChatResult,
    HumanMessage,
    SystemMessage,
)

from flock_resources.base import Resource, ToolResource
from flock_schemas.llm_chat import LLMChatSchema


class LLMChatResource(Resource):
    """Class for LLM resources."""

    VENDORS = {"ChatOpenAI": ChatOpenAI, "OpenAICopyCat": ChatOpenAI}

    def __init__(
        self,
        manifest: LLMChatSchema,
        dependencies: Optional[dict[str, Resource]] = None,
        tools: Optional[List[ToolResource]] = None,
    ):
        super().__init__(manifest, dependencies, tools)
        self.vendor_cls: BaseLanguageModel = cast(
            BaseLanguageModel, self.VENDORS[self.vendor]
        )

        self.resource = self.vendor_cls(**self.options)  # type: ignore

    def one_shot(self, message: str) -> str:
        """Generate a response to a message."""

        response = self.resource([HumanMessage(content=message)])
        return response.content

    def chat(self, messages: List[BaseMessage]) -> ChatResult:
        """Generate a response to a message."""

        response = self.resource(messages)
        return response


export = {
    "LLMChat": LLMChatResource,
}
