from _typeshed import Incomplete
from flock_schemas.agent import AgentSchema as AgentSchema
from flock_schemas.base import BaseFlockSchema as BaseFlockSchema, Kind as Kind
from flock_schemas.custom import CustomSchema as CustomSchema
from flock_schemas.embedding import EmbeddingSchema as EmbeddingSchema
from flock_schemas.llm import LLMSchema as LLMSchema
from flock_schemas.llm_tool import LLMToolSchema as LLMToolSchema
from flock_schemas.load_tool import LoadToolSchema as LoadToolSchema
from flock_schemas.prompt_template import PromptTemplateSchema as PromptTemplateSchema
from flock_schemas.splitter import SplitterSchema as SplitterSchema
from flock_schemas.vectorstore import VectorStoreSchema as VectorStoreSchema
from flock_schemas.vectorstore_qa_tool import VectorStoreQAToolSchema as VectorStoreQAToolSchema

Schemas: Incomplete

class SchemasFactory:
    @staticmethod
    def get_schema(kind: Kind) -> BaseFlockSchema: ...
