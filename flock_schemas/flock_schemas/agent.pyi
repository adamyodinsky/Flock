from enum import Enum
from flock_schemas.base import BaseFlockSchema as BaseFlockSchema, BaseOptions as BaseOptions
from flock_schemas.dependencies import LLMDependency as LLMDependency, ToolDependency as ToolDependency
from typing import List, Literal

class AgentVendor(str, Enum):
    ZERO_SHOT_REACT_DESCRIPTION: str
    REACT_DOCSTORE: str
    SELF_ASK_WITH_SEARCH: str
    CONVERSATIONAL_REACT_DESCRIPTION: str
    CHAT_ZERO_SHOT_REACT_DESCRIPTION: str
    CHAT_CONVERSATIONAL_REACT_DESCRIPTION: str

class AgentSpec(BaseOptions):
    vendor: AgentVendor
    tools: List[ToolDependency]
    dependencies: tuple[LLMDependency]

class AgentSchema(BaseFlockSchema):
    kind: Literal['Agent']
    spec: AgentSpec
