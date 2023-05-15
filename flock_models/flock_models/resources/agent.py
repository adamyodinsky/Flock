"""Resource for vectorstore."""

from typing import Dict, List, Optional

from flock_schemas import AgentSchema
from flock_schemas.base import Kind
from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory

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

        memory = {}

        if self.vendor.value == AgentType.CONVERSATIONAL_REACT_DESCRIPTION.value:
            memory = {"memory": ConversationBufferMemory(memory_key="chat_history")}
        elif self.vendor.value == AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION.value:
            memory = {
                "memory": ConversationBufferMemory(
                    memory_key="chat_history", return_messages=True
                )
            }
        llm = self.dependencies.get(Kind.LLM) or self.dependencies.get(Kind.LLMChat)
        self.llm = llm.resource

        self.resource = initialize_agent(
            tools=self.agent_tools,
            llm=self.llm,
            agent=self.vendor,
            **self.options,  # type: ignore
            **memory,
        )

        self.run = self.resource.run
        self.arun = self.resource.arun
