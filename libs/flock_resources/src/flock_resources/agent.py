"""Resource for vectorstore."""

import logging
from typing import Dict, List, Optional

from flock_schemas.agent import AgentSchema
from flock_schemas.base import Kind
from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory

from flock_resources.base import Agent, Resource, ToolResource


class AgentResource(Agent):
    """Class for self ask search agent.

    Attributes:
        llm: The llm resource.
        run: The run function of the agent.
        arun: The async run function of the agent.
    """

    def __init__(
        self,
        manifest: AgentSchema,
        dependencies: Optional[Dict[str, Resource]],
        tools: Optional[List[ToolResource]] = None,
        dry_run: bool = False,
    ):
        logging.debug(f"Initializing agent resource: {manifest.metadata.name}")
        super().__init__(manifest, dependencies, tools)
        memory = {}

        if self.vendor == AgentType.CONVERSATIONAL_REACT_DESCRIPTION.value:
            memory = {"memory": ConversationBufferMemory(memory_key="chat_history")}
        elif self.vendor == AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION.value:
            memory = {
                "memory": ConversationBufferMemory(
                    memory_key="chat_history", return_messages=True
                )
            }
        llm = self.dependencies.get(Kind.LLMChat)
        self.llm = llm

        self.resource = initialize_agent(
            tools=self.agent_tools,
            llm=self.llm.resource,
            agent=self.vendor,
            **self.options,  # type: ignore
            **memory,
        )

        self.run = self.resource.run
        self.arun = self.resource.arun

        logging.debug(f"Initialized agent resource: {manifest.metadata.name}")
        logging.debug(f"Agent options: {self.options}")
        logging.debug(f"Agent llm: {self.llm.manifest.metadata.name}")


export = {
    "Agent": AgentResource,
}
