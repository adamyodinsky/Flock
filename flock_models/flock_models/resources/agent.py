"""Resource for vectorstore."""

from typing import Any
from flock_models.resources.base import Agent
from flock_models.schemes.agent import AgentSchema, AgentType
from langchain.agents import initialize_agent, Tool as ToolWarperLC
from flock_models.schemes.base import Kind


class AgentResource(Agent):
    """Class for self ask search agent."""
    VENDORS = AgentType

    def __init__(
        self,
        manifest: AgentSchema,
        dependencies: dict[str, Any],
        tools: list[ToolWarperLC],
    ):
        super().__init__(manifest, dependencies, tools)
        
        self.resource = initialize_agent(
            tools=tools,
            llm=self.dependencies[Kind.llm.value],
            agent=self.VENDORS[self.vendor].value,
            **self.options,
        )
