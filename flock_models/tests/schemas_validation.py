"""Validate all schemas in the schemas folder."""

from typing import List

import yaml
from flock_schemas import Schemas
from pydantic import ValidationError

SCHEMA_FILES = [
    "vectorstore.yaml",
    "vectorstore_qa_tool.yaml",
    "search_tool.yaml",
    "splitter.yaml",
    "embedding.yaml",
    "llm.yaml",
    "agent.yaml",
]


def validate_crds(_crds: List[dict]):
    """Validate all schemas in the schemas folder."""
    for crd in _crds:
        kind = crd["kind"]
        try:
            scheme = Schemas[kind]
            scheme(**crd)
        except ValidationError as error:
            print(f"Error validating {kind}:")
            print(error.json())
        print(f"Validating {kind} - OK")


# Validate all schemas
for file in SCHEMA_FILES:
    with open(f"tests/schemas/{file}", encoding='utf-8') as f:
        crds = list(yaml.load_all(f, Loader=yaml.FullLoader))
        validate_crds(crds)
