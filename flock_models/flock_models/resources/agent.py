"""Resource for vectorstore."""

from typing import Any

from langchain.agents import Tool as ToolWarperLC
from langchain.agents import initialize_agent

from flock_models.resources.base import Agent
from flock_models.schemes.agent import AgentSchema, AgentType
from flock_models.schemes.base import Kind


class AgentResource(Agent):
    """Class for self ask search agent."""

    def __init__(
        self,
        manifest: AgentSchema,
        dependencies: dict[str, Any],
        tools: list[ToolWarperLC],
    ):
        super().__init__(manifest, dependencies, tools)
        self.resource = initialize_agent(
            tools=self.tools,
            llm=self.dependencies[Kind.LLM],
            agent=self.vendor,
            **self.options,
        )
