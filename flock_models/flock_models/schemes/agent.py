from pydantic import Field
from typing import List, Optional
from flock_models.schemes.base import FlockBaseSchema, BaseModelConfig, Kind, Dependency
from langchain.agents.agent_types import AgentType

class LLM(Dependency):
    kind: str = Field(Kind.llm.value, const=True)

class Tool(Dependency):
    kind: Kind = Field(description="Tool kind, e.g. SearchTool, VectorStoreQATool, etc.")

class AgentSpec(BaseModelConfig):
    vendor: str = Field(..., description="Agent class")
    agent_type: AgentType = Field(..., description="Agent type")
    options: Optional[dict] = Field(description="LLM options")
    tools: List[Tool] = Field(..., description="Agent tools")
    dependencies: tuple[LLM] = Field(..., description="Agent dependencies")

class AgentSchema(FlockBaseSchema):
    kind: str = Field(Kind.agent.value, const=True)
    spec: AgentSpec
