from flock_models.resources.embedding import EmbeddingResource
from flock_models.resources.llm import LLMResource
from flock_models.resources.splitter import SplitterResource
from flock_models.resources.vectorstore import VectorStoreResource
from flock_models.resources.vectorstore_qa_tool import VectorStoreQAToolResource
from flock_models.resources.agent import AgentResource
from flock_models.resources.base import Agent, Resource
from flock_models.schemes.base import Kind as __Kind

Resources = {
    __Kind.embedding: EmbeddingResource,
    __Kind.llm: LLMResource,
    __Kind.splitter: SplitterResource,
    __Kind.vectorstore: VectorStoreResource,
    __Kind.vectorstore_qa_tool: VectorStoreQAToolResource,
    __Kind.agent: AgentResource,
}
