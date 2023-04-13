from pydantic import Field
from typing import List
from flock_schemas.base import FlockBaseModel, BaseModelConfig, Labels

class Tool(Labels):
    kind: str
    name: str

class AgentLLM(Labels):
    name: str

class AgentSpec(BaseModelConfig):
    llm: AgentLLM
    tools: List[Tool]

class Agent(FlockBaseModel):
    kind: str = Field("Agent", const=True)
    spec: AgentSpec
