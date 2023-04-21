"""Test building resources from yaml files"""

import os
import flock_schemas as schemas
from flock_schemas import Kind
from flock_store.resources import ResourceStoreFactory

from flock_models import resources
from flock_models.builder import ResourceBuilder

PATH_TO_SCHEMAS = "tests/schemas"
RESOURCES_FILES = {
    "Splitter": "splitter.yaml",
    "Embedding": "embedding.yaml",
    "LLM": "llm.yaml",
    "VectorStore": "vectorstore.yaml",
    "VectorStoreQATool": "vectorstore_qa_tool.yaml",
    "SearchTool": "search_tool.yaml",
    "PromptTemplate": "prompt_template.yaml",
    "LLMTool": "llm_tool.yaml",
    "Agent": "agent.yaml",
    "Agent": "baby_agi_agent.yaml",
    "BabyAGI": "baby_agi.yaml",
}

# Setup
# pylint: disable=C0103
secret_store = None
home_dir = os.path.expanduser("~")
store_prefix = f"{home_dir}/.flock/resource_store"
resource_store = ResourceStoreFactory.get_resource_store(
    key_prefix=store_prefix, store_type="fs"
)

resource_builder = ResourceBuilder(
    resource_store=resource_store, secret_store=secret_store
)


def test_building_resources(kind, file):
    """Test building resources from yaml files"""

    print(f"{file} - ", end="", flush=True)

    if kind not in Kind.__members__:
        kind = Kind.Custom
    
    path = f"{PATH_TO_SCHEMAS}/{file}"
    schema = schemas.Schemas[kind]

    # test loading from yaml file
    manifest = resource_store.load_yaml(path, schema)
    if manifest.kind != kind and kind != Kind.Custom:
        raise AssertionError(f"kind is not {kind} as expected in the manifest")

    # test save and load from resource store
    key = f"default/{manifest.kind}/{manifest.metadata.name}"
    resource_store.put_model(key=key, val=manifest)
    manifest: schema = resource_store.get_model(key=key, schema=schema)

    resource = resource_builder.build_resource(manifest)

    print(f"{manifest.kind} - OK")
    return resource


def run_build_tests():
    """Run all tests"""
    for kind, file in RESOURCES_FILES.items():
        test_building_resources(kind, file)
    
    agent: resources.AgentResource = test_building_resources("Agent", "agent.yaml")
    baby_agi_agent: resources.AgentResource = test_building_resources("Agent", "baby_agi_agent.yaml")
    baby_agi = test_building_resources("BabyAGI", "baby_agi.yaml")

    try:
        agent.resource.run("Who is the current prime minister of israel?")
        baby_agi.run("Write a financial report for the last week")
    # pylint: disable=W0703
    except Exception as e:
        print("\nError:", str(e))


run_build_tests()
