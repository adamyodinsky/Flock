from typing import List

import yaml
from pydantic import ValidationError
from flock_models.schemes.agent import AgentSchema
from flock_models.schemes.embedding import EmbeddingSchema
from flock_models.schemes.vector_store import VectorStoreSchema
from flock_models.schemes.llm import LLMSchema
from flock_models.schemes.vectorstore_retriever_tool import (
    VectorStoreRetrieverToolSchema,
)
from flock_models.schemes.splitter import SplitterSchema

from flock_models.schemes.search_tool import SearchToolSchema


def validate_crds(crds: List[dict]):
    for crd in crds:
        kind = crd["kind"]
        try:
            if kind == "Agent":
                AgentSchema(**crd)
            elif crd["kind"] == "VectorStoreRetrieverTool":
                VectorStoreRetrieverToolSchema(**crd)
            elif crd["kind"] == "LLM":
                LLMSchema(**crd)
            elif crd["kind"] == "SearchTool":
                SearchToolSchema(**crd)
            elif crd["kind"] == "VectorStore":
                VectorStoreSchema(**crd)
            elif crd["kind"] == "Embedding":
                EmbeddingSchema(**crd)
            elif crd["kind"] == "Splitter":
                SplitterSchema(**crd)
            else:
                raise ValueError(f"Unknown kind {crd['kind']}")
        except ValidationError as e:
            print(f"Error validating {kind}:")
            print(e.json())
        print(f"Validating {kind} - OK")


files = [
    "agent.yaml",
    "vectorstore_retriever_tool.yaml",
    "llm.yaml",
    "search_tool.yaml",
    "vector_store.yaml",
    "embedding.yaml",
    "splitter.yaml",
]

for file in files:
    with open(f"tests/schemas/{file}") as f:
        crds = list(yaml.load_all(f, Loader=yaml.FullLoader))
        validate_crds(crds)
