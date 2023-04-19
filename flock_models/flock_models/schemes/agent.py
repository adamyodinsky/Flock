from typing import List, Optional

from langchain.agents.agent_types import AgentType
from pydantic import Field

from flock_models.schemes.base import BaseOptions, BaseDependency, BaseFlockSchema, Kind
from flock_models.schemes.dependencies import LLMDependency

class AgentTool(BaseDependency):
    description: Optional[str] = Field(description="Tool description")
    

class AgentSpec(BaseOptions):
    vendor: AgentType = Field(..., description="Agent type")
    tools: List[AgentTool] = Field(..., description="Agent tools")
    dependencies: tuple[LLMDependency] = Field(..., description="Agent dependencies")


class AgentSchema(BaseFlockSchema):
    kind: str = Field(Kind.Agent, const=True)
    spec: AgentSpec
