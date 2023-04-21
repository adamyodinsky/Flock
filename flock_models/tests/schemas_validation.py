"""Validate all schemas in the schemas folder."""
from typing import List

import yaml
from pydantic import ValidationError

from flock_schemas import Schemas

SCHEMA_FILES = {
    "VectorStore": "vectorstore.yaml",
    "VectorStoreQATool": "vectorstore_qa_tool.yaml",
    "SearchTool": "search_tool.yaml",
    "Splitter": "splitter.yaml",
    "Embedding": "embedding.yaml",
    "LLM": "llm.yaml",
    "Agent": "agent.yaml",
    "PromptTemplate": "prompt_template.yaml",
    "LLMTool": "llm_tool.yaml",
    "Agent": "baby_agi_agent.yaml",
    "Custom": "baby_agi.yaml",
}


def validate_crd(_kind, _crd: List[dict]):
    """Validate all CRDs in a file."""
    
    try:
        scheme = Schemas[_kind]
        scheme(**_crd)
    except ValidationError as error:
        print(f"Error validating {_kind}:")
        print(error.json())
    print(f"{_kind} - OK")


# Validate all yaml schemas
for file_kind, file_name in SCHEMA_FILES.items():
    print(f"Validating {file_name} - ", end="", flush=True)
    with open(f"tests/schemas/{file_name}", encoding="utf-8") as f:
        crd = yaml.load(f, Loader=yaml.FullLoader)
        validate_crd(file_kind, crd)
    
    