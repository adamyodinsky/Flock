"""Resource for vectorstore."""

from typing import Any
from flock_models.resources.base import Agent, Resource, ToolResource
from flock_store.resources.base import ResourceStore
from flock_models.schemes.agent import AgentSchema, AgentType, Tool as ToolSchema
from flock_models.resources.llm import LLMResource
from langchain.agents import initialize_agent, Tool as LCToolWarper
from flock_models.schemes.base import Kind


class AgentResource(Agent):
    """Class for self ask search agent."""

    def __init__(
        self,
        manifest: dict[str, Any],
        resource_store: ResourceStore,
        agent_type: AgentType,
    ):
        self.agent_type = agent_type
        self.manifest = AgentSchema(**manifest)
        llm_key = f"{Kind.llm.value}/{self.manifest.spec.llm.name}"
        llm_resource: LLMResource = resource_store.get_data(llm_key)

        tools = []

        for tool in self.manifest.spec.tools:
            tool = ToolSchema(**tool)
            tool_key = f"{tool.kind}/{tool.name}"
            tool_resource: ToolResource = resource_store.get_resource(tool_key)

            wrapped_tool = LCToolWarper(
                name=tool_resource.get_name(),
                description=tool_resource.get_description(),
                func=tool_resource.get_func(),
            )

            tools.append(wrapped_tool)

        self.resource = initialize_agent(
            tools=tools, llm=llm_resource.resource, agent=agent_type, verbose=True
        )


# Tool(
#       name="langchain_git",
#       description="LangChain Git Repository. LangChain is a framework for developing applications powered by language models.",
#       func=git_vectorstore_retriever
# )


#  agent = initialize_agent(
#         tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
#     )


# initialize_agent(
#     tools: Sequence[BaseTool],
#     llm: BaseLanguageModel,
#     agent: Optional[AgentType] = None,
#     callback_manager: Optional[BaseCallbackManager] = None,
#     agent_path: Optional[str] = None,
#     agent_kwargs: Optional[dict] = None,


# apiVersion: flock/v1
# kind: Agent
# metadata:
#   name: my-qa-agent
#   description: a Q&A agent for internal projects
#   labels:
#     app: my_app
# spec:
#   type:
#   llm:
#     name: openai
#     labels:
#       app: my_app
#   tools:
#     - kind: VectorStoreQATool
#       name: langchain-docs
#       description: LangChain documentation
#     - kind: SearchTool
#       name: my-google-search
#       labels:
#         location:  us-west-1
