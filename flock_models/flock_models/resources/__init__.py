from flock_models.resources.embedding import EmbeddingResource
from flock_models.resources.llm import LLMResource
from flock_models.resources.splitter import SplitterResource
from flock_models.resources.vectorstore import VectorStoreResource
from flock_models.resources.vectorstore_qa_tool import VectorStoreQAToolResource
from flock_models.resources.agent import AgentResource
from flock_models.schemes.base import Kind
from flock_models.schemes.base import FlockBaseSchema
from flock_models.resources.base import Agent, Resource

Resources = {
    Kind.embedding: EmbeddingResource,
    Kind.llm: LLMResource,
    Kind.splitter: SplitterResource,
    Kind.vectorstore: VectorStoreResource,
    Kind.vectorstore_qa_tool: VectorStoreQAToolResource,
    Kind.agent: AgentResource,
}
