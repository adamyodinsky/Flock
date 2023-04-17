from pydantic import Field
from typing import List
from flock_models.schemes.base import FlockBaseSchema, BaseModelConfig, Labels
from langchain.agents.agent_types import AgentType


class Tool(Labels):
    kind: str
    name: str


class AgentLLM(Labels):
    name: str


class AgentSpec(BaseModelConfig):
    llm: AgentLLM
    agent_type: AgentType
    tools: List[Tool]


class AgentSchema(FlockBaseSchema):
    kind: str = Field("Agent", const=True)
    spec: AgentSpec
