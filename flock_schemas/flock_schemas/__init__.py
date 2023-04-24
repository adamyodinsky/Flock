from flock_schemas.agent import AgentSchema
from flock_schemas.base import BaseDependency as DependencySchema
from flock_schemas.base import BaseFlockSchema
from flock_schemas.base import BaseMetaData as MetaDataSchema
from flock_schemas.base import Kind
from flock_schemas.custom import CustomSchema
from flock_schemas.embedding import EmbeddingSchema
from flock_schemas.llm import LLMSchema
from flock_schemas.llm_tool import LLMToolSchema
from flock_schemas.prompt_template import PromptTemplateSchema
from flock_schemas.load_tool import LoadToolSchema
from flock_schemas.splitter import SplitterSchema
from flock_schemas.vectorstore import VectorStoreSchema
from flock_schemas.vectorstore_qa_tool import VectorStoreQAToolSchema

Schemas = {
    Kind.Embedding: EmbeddingSchema,
    Kind.LLM: LLMSchema,
    Kind.Splitter: SplitterSchema,
    Kind.VectorStore: VectorStoreSchema,
    Kind.VectorStoreQATool: VectorStoreQAToolSchema,
    Kind.Agent: AgentSchema,
    Kind.LoadTool: LoadToolSchema,
    Kind.Splitter: SplitterSchema,
    Kind.PromptTemplate: PromptTemplateSchema,
    Kind.LLMTool: LLMToolSchema,
    Kind.Custom: CustomSchema,
}


class SchemasFactory:
    """Class for schemas factory."""

    @staticmethod
    def get_schema(kind: Kind) -> BaseFlockSchema:
        """Get schema by kind."""
        return Schemas[kind]
