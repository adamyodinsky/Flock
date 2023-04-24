"""Resource for vectorstore."""

from typing import Any, List, Optional, cast

from flock_schemas import AgentSchema
from flock_schemas.agent import AgentSchema
from flock_schemas.base import BaseFlockSchema
from flock_schemas.base import BaseOptions as BaseOptionsSchema
from flock_schemas.base import Kind
from langchain.agents import Tool as ToolWarperLC
from langchain.agents import initialize_agent

from flock_models.resources.base import Agent, Resource, ToolResource


class AgentResource(Agent):
    """Class for self ask search agent."""

    def __init__(
        self,
        manifest: AgentSchema,
        dependencies: Optional[dict[str, ToolResource]] = None,
        tools: Optional[list[ToolResource]] = None,
    ):
        super().__init__(manifest, dependencies, tools)
        self.resource = initialize_agent(
            tools=self.agent_tools,
            llm=self.dependencies[Kind.LLM].resource,
            agent=self.vendor,
            **self.options,
        )
        self.run = self.resource.run
