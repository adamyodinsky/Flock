from flock_models.resources.embedding import EmbeddingResource
from flock_models.resources.llm import LLMResource
from flock_models.resources.splitter import SplitterResource
from flock_models.resources.search_tool import SearchToolResource
from flock_models.resources.vectorstore import VectorStoreResource
from flock_models.resources.vectorstore_qa_tool import VectorStoreQAToolResource
from flock_models.resources.agent import AgentResource
from flock_models.resources.base import Agent, Resource, ToolResource
from flock_models.schemes.base import Kind as __Kind

Resources = {
    __Kind.Embedding: EmbeddingResource,
    __Kind.LLM: LLMResource,
    __Kind.SearchTool: SearchToolResource,
    __Kind.VectorStore: VectorStoreResource,
    __Kind.VectorStoreQATool: VectorStoreQAToolResource,
    __Kind.Agent: AgentResource,
    __Kind.Splitter: SplitterResource
}
