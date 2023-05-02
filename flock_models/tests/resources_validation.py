"""Test building resources from yaml files"""

import os
from typing import cast

from dotenv import find_dotenv, load_dotenv
from flock_common.env_checker import check_env_vars
from flock_common.validation import validation_iterator
from flock_resource_store import ResourceStoreFactory
from flock_schemas import SchemasFactory

from flock_models import resources
from flock_models.builder import ResourceBuilder
from plugins.baby_agi import BabyAGIAgent

PATH_TO_SCHEMAS = "tests/schemas"
RESOURCES_FILES = [
    "splitter.yaml",
    "embedding.yaml",
    "llm_chat.yaml",
    "vectorstore.yaml",
    "vectorstore_qa_tool.yaml",
    "search_tool.yaml",
    "prompt_template.yaml",
    "llm_tool.yaml",
    "gpt4all.yaml",
    "agent.yaml",
    "agent_conversational.yaml",
    "baby_agi_agent.yaml",
]

# Setup
# pylint: disable=C0103
secret_store = None
required_vars = []
optional_vars = ["FLOCK_RESOURCE_STORE_TYPE"]

load_dotenv(find_dotenv(os.environ.get("FLOCK_ENV_FILE", ".env")))
check_env_vars(required_vars, optional_vars)

resource_store = ResourceStoreFactory.get_resource_store(
    store_type=os.getenv("FLOCK_RESOURCE_STORE_TYPE", "mongo")
)

resource_builder = ResourceBuilder(resource_store=resource_store)


def test_building_resources(manifest):
    """Test building resources from yaml files"""

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
    resource_store.put(val=manifest)
    manifest = resource_store.get(
        namespace=schema_instance.namespace,
        kind=schema_instance.kind,
        name=schema_instance.metadata.name,
    )
    schema_instance = schema_cls.validate(manifest)

    # test building resource
    resource = resource_builder.build_resource(manifest)

    return resource


def run_build_tests():
    """Run all tests"""
    validation_iterator(
        dir_path="../schemas_core",
        validation_function=test_building_resources,
    )

    # agent: resources.AgentResource = cast(
    #     resources.AgentResource, test_building_resources("agent.yaml")
    # )
    # agent_c: resources.AgentResource = cast(
    #     resources.AgentResource, test_building_resources("agent_conversational.yaml")
    # )
    # baby_agi = cast(BabyAGIAgent, test_building_resources("baby_agi.yaml"))

    # try:
    #     agent.resource.run("Who is the current prime minister of israel?")
    # # pylint: disable=W0703
    # except Exception as e:
    #     print(str(e))

    # try:
    #     agent_c.resource.run("Who is the current prime minister of israel?")
    # # pylint: disable=W0703
    # except Exception as e:
    #     print(str(e))

    # try:
    # baby_agi.run("Write a weather report for SF today")
    # # pylint: disable=W0703
    # except Exception as e:
    #     print(str(e))

    # try:
    #     for i in range(10):
    #         input_str = input("User: ")
    #         agent_c.resource.run(input_str)
    # # pylint: disable=W0703
    # except Exception as e:
    #     print(str(e))


run_build_tests()
