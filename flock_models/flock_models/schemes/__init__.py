from flock_models.schemes.embedding import EmbeddingSchema
from flock_models.schemes.llm import LLMSchema
from flock_models.schemes.splitter import SplitterSchema
from flock_models.schemes.vectorstore import VectorStoreSchema
from flock_models.schemes.vectorstore_qa_tool import VectorStoreQAToolSchema
from flock_models.schemes.agent import AgentSchema
from flock_models.schemes.base import Kind, FlockBaseSchema, Dependency as DependencySchema

Schemas = {
    Kind.embedding: EmbeddingSchema,
    Kind.llm: LLMSchema,
    Kind.splitter: SplitterSchema,
    Kind.vectorstore: VectorStoreSchema,
    Kind.vectorstore_qa_tool: VectorStoreQAToolSchema,
    Kind.agent: AgentSchema,
}
