import importlib
import os
from typing import Tuple, cast

import flock_schemas
from flock_schemas.agent import AgentSchema
from flock_schemas.base import BaseDependency as DependencySchema
from flock_schemas.base import BaseFlockSchema
from flock_schemas.base import BaseMetaData as MetaDataSchema
from flock_schemas.base import Kind
from flock_schemas.custom import CustomSchema
from flock_schemas.embedding import EmbeddingSchema
from flock_schemas.llm import LLMSchema
from flock_schemas.llm_chat import LLMChatSchema
from flock_schemas.llm_tool import LLMToolSchema
from flock_schemas.load_tool import LoadToolSchema
from flock_schemas.prompt_template import PromptTemplateSchema
from flock_schemas.splitter import SplitterSchema
from flock_schemas.vectorstore import VectorStoreSchema
from flock_schemas.vectorstore_qa_tool import VectorStoreQAToolSchema


class SchemasFactory:
    """Class for schemas factory."""

    SCHEMAS_MAP = {
        "Embedding": EmbeddingSchema,
        "LLM": LLMSchema,
        "VectorStore": VectorStoreSchema,
        "VectorStoreQATool": VectorStoreQAToolSchema,
        "Agent": AgentSchema,
        "LoadTool": LoadToolSchema,
        "Splitter": SplitterSchema,
        "PromptTemplate": PromptTemplateSchema,
        "LLMTool": LLMToolSchema,
        "LLMChat": LLMChatSchema,
        "Custom": CustomSchema,
    }

    SCHEMAS_LIST = [
        "Embedding",
        "LLM",
        "LLMChat",
        "VectorStore",
        "VectorStoreQATool",
        "Agent",
        "LoadTool",
        "Splitter",
        "PromptTemplate",
        "LLMTool",
        "Custom",
    ]

    @staticmethod
    def get_schema(kind: str) -> BaseFlockSchema:
        """Get schema by kind."""
        if kind in SchemasFactory.SCHEMAS_LIST:
            return SchemasFactory.SCHEMAS_MAP[kind]
        else:
            print(
                f"- Unknown kind: {kind}, returning CustomSchema -", end=" ", flush=True
            )
            return cast(BaseFlockSchema, CustomSchema)

    @staticmethod
    def load_schemas(schemas_dir: str = "flock_schemas") -> Tuple[dict, dict]:
        """Load schemas from flock_schemas directory."""

        sub_schemas_map = {}
        main_schemas_map = {}

        module_dir = os.path.dirname(flock_schemas.__file__)

        for file in os.listdir(module_dir):
            path = os.path.join(module_dir, file)

            if os.path.isfile(path):
                if file.endswith(".py") and file != "__init__.py":
                    module_name = file[:-3]
                    module = importlib.import_module(f"{schemas_dir}.{module_name}")

                    for key, value in module.export["sub"].items():
                        sub_schemas_map[key] = value

                    for key, value in module.export["main"].items():
                        main_schemas_map[key] = value
        return sub_schemas_map, main_schemas_map
