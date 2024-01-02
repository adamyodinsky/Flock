"""Agent schema."""

from enum import Enum
from typing import List, Literal

from pydantic import Field

from flock_schemas.base import (
    BaseResourceSchema,
    BaseToolDependency,
    Category,
    BaseSpec
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
    OPENAI_MULTI_FUNCTIONS = "openai-multi-functions"


class AgentSpec(BaseSpec):
    """Agent spec."""

    vendor: AgentVendor = Field(..., description="Agent type")
    tools: List[BaseToolDependency] = Field(..., description="Agent tools")
    dependencies: tuple[LLMChatDependency] = Field(
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
