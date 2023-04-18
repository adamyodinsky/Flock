from typing import List, Optional

from langchain.agents.agent_types import AgentType
from pydantic import Field

from flock_models.schemes.base import Options, Dependency, FlockBaseSchema, Kind


class LLM(Dependency):
    kind: str = Field(Kind.LLM, const=True)

class Tool(Dependency):
    description: Optional[str] = Field(description="Tool description")
    

class AgentSpec(Options):
    vendor: AgentType = Field(..., description="Agent type")
    tools: List[Tool] = Field(..., description="Agent tools")
    dependencies: tuple[LLM] = Field(..., description="Agent dependencies")


class AgentSchema(FlockBaseSchema):
    kind: str = Field(Kind.Agent, const=True)
    spec: AgentSpec
