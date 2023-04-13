from typing import List

import yaml
from agent import Agent
from embedding import Embedding
from vector_store import VectorStore
from llm import LLM
from pydantic import ValidationError
from vectorstore_retriever_tool import VectorStoreRetrieverTool

from search_tool import SearchTool


def validate_crds(crds: List[dict]):
    for crd in crds:
        kind = crd['kind']
        try:
            if kind == 'Agent':
                Agent(**crd)
            elif crd['kind'] == 'VectorStoreRetrieverTool':
                VectorStoreRetrieverTool(**crd)
            elif crd['kind'] == 'LLM':
                LLM(**crd)
            elif crd['kind'] == 'SearchTool':
                SearchTool(**crd)
            elif crd['kind'] == 'VectorStore':
                VectorStore(**crd)
            elif crd['kind'] == 'Embedding':
                Embedding(**crd)
            else:
                raise ValueError(f"Unknown kind {crd['kind']}")
        except ValidationError as e:
            print(f"Error validating {kind}:")
            print(e.json())
        print(f"Validating {kind} - OK")
        


files = [
    'agent.yaml',
    'vectorstore_retriever_tool.yaml',
    'llm.yaml',
    'search_tool.yaml',
    "vector_store.yaml",
    "embedding.yaml",

]

for file in files:
    with open(f"tests/schemas/{file}") as f:
        crds = list(yaml.load_all(f, Loader=yaml.FullLoader))
        validate_crds(crds)