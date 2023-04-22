from flock_models.resources.agent import AgentResource
from flock_models.resources.base import Agent, Resource, ToolResource
from flock_models.resources.embedding import EmbeddingResource
from flock_models.resources.llm import LLMResource
from flock_models.resources.load_tool import LoadToolResource
from flock_models.resources.splitter import SplitterResource
from flock_models.resources.vectorstore import VectorStoreResource
from flock_models.resources.vectorstore_qa_tool import VectorStoreQAToolResource
from flock_models.resources.prompt_template import PromptTemplateResource
from flock_models.resources.llm_tool import LLMToolResource

Resources = {
    "Embedding": EmbeddingResource,
    "LLM": LLMResource,
    "LoadTool": LoadToolResource,
    "VectorStore": VectorStoreResource,
    "VectorStoreQATool": VectorStoreQAToolResource,
    "Agent": AgentResource,
    "Splitter": SplitterResource,
    "PromptTemplate": PromptTemplateResource,
    "LLMTool": LLMToolResource
}
