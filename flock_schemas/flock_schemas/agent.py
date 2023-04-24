from enum import Enum
from typing import List, Literal

from pydantic import Field

from flock_schemas.base import BaseFlockSchema, BaseOptions
from flock_schemas.dependencies import LLMDependency, ToolDependency


class AgentType(str, Enum):
    ZERO_SHOT_REACT_DESCRIPTION = "zero-shot-react-description"
    REACT_DOCSTORE = "react-docstore"
    SELF_ASK_WITH_SEARCH = "self-ask-with-search"
    CONVERSATIONAL_REACT_DESCRIPTION = "conversational-react-description"
    CHAT_ZERO_SHOT_REACT_DESCRIPTION = "chat-zero-shot-react-description"
    CHAT_CONVERSATIONAL_REACT_DESCRIPTION = "chat-conversational-react-description"


class AgentSpec(BaseOptions):
    vendor: AgentType = Field(..., description="Agent type")
    tools: List[ToolDependency] = Field(..., description="Agent tools")
    dependencies: tuple[LLMDependency] = Field(..., description="Agent dependencies")


class AgentSchema(BaseFlockSchema):
    kind: Literal["Agent"] = Field(..., description="The kind of the object")
    spec: AgentSpec
