from flock_models.schemes.embedding import EmbeddingSchema
from flock_models.schemes.llm import LLMSchema
from flock_models.schemes.splitter import SplitterSchema
from flock_models.schemes.vectorstore import VectorStoreSchema
from flock_models.schemes.vectorstore_qa_tool import VectorStoreQAToolSchema
from flock_models.schemes.agent import AgentSchema
from flock_models.schemes.search_tool import SearchToolSchema
from flock_models.schemes.base import Kind, FlockBaseSchema, Dependency as DependencySchema

Schemas = {
    Kind.Embedding: EmbeddingSchema,
    Kind.LLM: LLMSchema,
    Kind.SearchTool: SplitterSchema,
    Kind.VectorStore: VectorStoreSchema,
    Kind.VectorStoreQATool: VectorStoreQAToolSchema,
    Kind.Agent: AgentSchema,
    Kind.SearchTool: SearchToolSchema,
    Kind.Splitter: SplitterSchema
}
