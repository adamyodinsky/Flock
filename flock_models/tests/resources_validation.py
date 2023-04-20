"""Test building resources from yaml files"""

import flock_schemas as schemas
from flock_schemas import Kind
from flock_store.resources import ResourceStoreFS

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
}

# Setup
# pylint: disable=C0103
secret_store = None
resource_store = ResourceStoreFS(".resource_store")
resource_builder = ResourceBuilder(
    resource_store=resource_store, secret_store=secret_store
)


def test_building_resources(kind, file):
    """Test building resources from yaml files"""

    assert kind in Kind.__members__, f"{kind} is not a valid member of Kind enum"

    path = f"{PATH_TO_SCHEMAS}/{file}"
    schema = schemas.Schemas[kind]

    # test loading from yaml file
    manifest: schema = resource_store.load_yaml(path, schema)
    assert manifest.kind == kind, f"kind is not {kind} as expected in the manifest"

    # test save and load from resource store
    key = f"default/{manifest.kind}/{manifest.metadata.name}"
    resource_store.put_model(key=key, val=manifest)
    manifest: schema = resource_store.get_model(key=key, schema=schema)

    resource = resource_builder.build_resource(manifest)

    print(f"{manifest.kind} - OK")
    return resource


def test_building_agent(kind, file):
    """Test building agent from yaml files"""

    assert kind in Kind.__members__, f"{kind} is not a valid member of Kind enum"

    path = f"{PATH_TO_SCHEMAS}/{file}"
    schema = schemas.Schemas[kind]

    # test loading from yaml file
    manifest: schema = resource_store.load_yaml(path, schema)
    assert manifest.kind == kind, f"kind is not {kind} as expected in the manifest"

    # test save and load from resource store
    key = f"default/{manifest.kind}/{manifest.metadata.name}"
    resource_store.put_model(key=key, val=manifest)
    manifest: schema = resource_store.get_model(key=key, schema=schema)

    resource = resource_builder.build_agent(manifest)

    print(f"{manifest.kind} - OK")
    return resource


def run_build_tests():
    """Run all tests"""
    for kind, file in RESOURCES_FILES.items():
        test_building_resources(kind, file)

    agent: resources.AgentResource = test_building_agent("Agent", "agent.yaml")
    try:
        agent.resource.run("What is langchain?")
    # pylint: disable=W0703
    except Exception as e:
        print("\nError:", str(e))


run_build_tests()
