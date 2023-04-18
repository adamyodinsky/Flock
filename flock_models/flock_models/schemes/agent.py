from typing import List, Optional

from langchain.agents.agent_types import AgentType
from pydantic import Field

from flock_models.schemes.base import BaseModelConfig, Dependency, FlockBaseSchema, Kind


class LLM(Dependency):
    kind: str = Field(Kind.LLM, const=True)


class AgentSpec(BaseModelConfig):
    vendor: AgentType = Field(..., description="Agent type")
    options: Optional[dict] = Field(description="LLM options")
    tools: List[Dependency] = Field(..., description="Agent tools")
    dependencies: tuple[LLM] = Field(..., description="Agent dependencies")


class AgentSchema(FlockBaseSchema):
    kind: str = Field(Kind.Agent, const=True)
    spec: AgentSpec
