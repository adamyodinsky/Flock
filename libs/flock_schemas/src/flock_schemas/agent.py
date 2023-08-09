"""Agent schema."""

from enum import Enum
from typing import List, Literal, Union

from pydantic import Field

from flock_schemas.base import (
    BaseOptions,
    BaseResourceSchema,
    BaseToolDependency,
    Category,
)
from flock_schemas.dependencies import LLMChatDependency, LLMDependency


class AgentVendor(str, Enum):
    """Enum for Agent types."""

    ZERO_SHOT_REACT_DESCRIPTION = "zero-shot-react-description"
    REACT_DOCSTORE = "react-docstore"
    SELF_ASK_WITH_SEARCH = "self-ask-with-search"
    CONVERSATIONAL_REACT_DESCRIPTION = "conversational-react-description"
    CHAT_ZERO_SHOT_REACT_DESCRIPTION = "chat-zero-shot-react-description"
    CHAT_CONVERSATIONAL_REACT_DESCRIPTION = "chat-conversational-react-description"
    STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION = (
        "structured-chat-zero-shot-react-description"
    )
    OPENAI_FUNCTIONS = "openai-functions"


class AgentSpec(BaseOptions):
    """Agent spec."""

    vendor: AgentType = Field(..., description="Agent type")
    tools: List[BaseToolDependency] = Field(..., description="Agent tools")
    dependencies: tuple[Union[LLMDependency, LLMChatDependency]] = Field(
        ..., description="Agent dependencies"
    )


class AgentSchema(BaseResourceSchema):
    """Agent schema."""

    kind: Literal["Agent"] = Field(..., description="The kind of the object")
    category: Category = Field(
        default=Category.AGENT, description="The resource category"
    )
    spec: AgentSpec


export = {
    "sub": {
        "AgentSpec": AgentSpec,
    },
    "main": {
        "Agent": AgentSchema,
    },
}
