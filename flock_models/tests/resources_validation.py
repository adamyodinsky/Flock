"""Test building resources from yaml files"""

import os
from typing import cast

from dotenv import find_dotenv, load_dotenv
from flock_common.env_checker import check_env_vars
from flock_resource_store import ResourceStoreFactory
from flock_schemas import SchemasFactory

from flock_models import resources
from flock_models.builder import ResourceBuilder
from plugins.baby_agi import BabyAGIAgent

PATH_TO_SCHEMAS = "tests/schemas"
RESOURCES_FILES = {
    "Splitter": "splitter.yaml",
    "Embedding": "embedding.yaml",
    "LLM": "llm.yaml",
    "VectorStore": "vectorstore.yaml",
    "VectorStoreQATool": "vectorstore_qa_tool.yaml",
    "LoadTool": "search_tool.yaml",
    "PromptTemplate": "prompt_template.yaml",
    "LLMTool": "llm_tool.yaml",
    "Agent": "baby_agi_agent.yaml",
}

# Setup
# pylint: disable=C0103
secret_store = None
required_vars = []
optional_vars = ["FLOCK_RESOURCE_STORE_TYPE"]

load_dotenv(find_dotenv())
check_env_vars(required_vars, optional_vars)

resource_store = ResourceStoreFactory.get_resource_store(
    store_type=os.getenv("FLOCK_RESOURCE_STORE_TYPE", "mongo")
)

resource_builder = ResourceBuilder(resource_store=resource_store)


def test_building_resources(file):
    """Test building resources from yaml files"""

    print(f"{file} - ", end="", flush=True)

    # test loading from yaml file
    path = f"{PATH_TO_SCHEMAS}/{file}"
    manifest = resource_store.load_file(path=path)  # type: ignore
    manifest_kind = manifest["kind"]

    # test schema validation
    schema_cls = SchemasFactory.get_schema(manifest_kind)
    schema_instance = schema_cls.validate(manifest)

    # asset schema kind
    if manifest_kind not in SchemasFactory.SCHEMAS_LIST:
        print(
            f"{schema_cls.__name__} Class as validator - ",
            end="",
            flush=True,
        )

    # test save and load from resource store
    key = f"default/{schema_instance.kind}/{schema_instance.metadata.name}"
    resource_store.put(key=key, val=manifest)
    manifest = resource_store.get(key=key)
    schema_instance = schema_cls.validate(manifest)

    # test building resource
    resource = resource_builder.build_resource(manifest)

    print(f"{schema_instance.kind} - OK")
    return resource


def run_build_tests():
    """Run all tests"""
    for _, file in RESOURCES_FILES.items():
        test_building_resources(file)

    agent: resources.AgentResource = cast(
        resources.AgentResource, test_building_resources("agent.yaml")
    )
    baby_agi = cast(BabyAGIAgent, test_building_resources("baby_agi.yaml"))

    try:
        agent.resource.run("Who is the current prime minister of israel?")
    # pylint: disable=W0703
    except Exception as e:
        print(str(e))

    try:
        baby_agi.run("Write a weather report for SF today")
    # pylint: disable=W0703
    except Exception as e:
        print(str(e))


run_build_tests()
