"""Agent schema."""

from enum import Enum
from typing import List, Literal

from pydantic import Field

from flock_schemas.base import BaseFlockSchema, BaseOptions, BaseToolDependency
from flock_schemas.dependencies import LLMDependency


class AgentType(str, Enum):
    """Enum for Agent types."""

    ZERO_SHOT_REACT_DESCRIPTION = "zero-shot-react-description"
    REACT_DOCSTORE = "react-docstore"
    SELF_ASK_WITH_SEARCH = "self-ask-with-search"
    CONVERSATIONAL_REACT_DESCRIPTION = "conversational-react-description"
    CHAT_ZERO_SHOT_REACT_DESCRIPTION = "chat-zero-shot-react-description"
    CHAT_CONVERSATIONAL_REACT_DESCRIPTION = "chat-conversational-react-description"


class AgentSpec(BaseOptions):
    """Agent spec."""

    vendor: AgentType = Field(..., description="Agent type")
    tools: List[BaseToolDependency] = Field(..., description="Agent tools")
    dependencies: tuple[LLMDependency] = Field(..., description="Agent dependencies")


class AgentSchema(BaseFlockSchema):
    """Agent schema."""

    kind: Literal["Agent"] = Field(..., description="The kind of the object")
    spec: AgentSpec


export = {
    "sub": {
        "AgentSpec": AgentSpec,
    },
    "main": {
        "AgentSchema": AgentSchema,
    },
}
