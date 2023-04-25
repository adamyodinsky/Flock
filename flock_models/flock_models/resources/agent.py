"""Resource for vectorstore."""

from typing import List, Optional, Dict

from flock_schemas import AgentSchema
from flock_schemas.base import Kind
from langchain.agents import initialize_agent

from flock_models.resources.base import Agent, Resource, ToolResource


class AgentResource(Agent):
    """Class for self ask search agent."""

    def __init__(
        self,
        manifest: AgentSchema,
        dependencies: Optional[Dict[str, Resource]],
        tools: Optional[List[ToolResource]] = None,
    ):
        super().__init__(manifest, dependencies, tools)
        self.resource = initialize_agent(
            tools=self.agent_tools,
            llm=self.dependencies[Kind.LLM].resource,
            agent=self.vendor,
            **self.options,  # type: ignore
        )
        self.run = self.resource.run
