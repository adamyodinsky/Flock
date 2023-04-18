from typing import List

import yaml
from pydantic import ValidationError
from flock_models.schemes import Schemas

SCHEMA_FILES = [
    "vectorstore.yaml",
    "vectorstore_qa_tool.yaml",
    "search_tool.yaml",
    "splitter.yaml",
    "embedding.yaml",
    "llm.yaml",
    "agent.yaml",
]

def validate_crds(crds: List[dict]):
    for crd in crds:
        kind = crd["kind"]
        try:
            scheme = Schemas[kind]
            scheme(**crd)
        except ValidationError as e:
            print(f"Error validating {kind}:")
            print(e.json())
        print(f"Validating {kind} - OK")

# Validate all schemas
for file in SCHEMA_FILES:
    with open(f"tests/schemas/{file}") as f:
        crds = list(yaml.load_all(f, Loader=yaml.FullLoader))
        validate_crds(crds)
