"""Test building resources from yaml files"""

import os
import readline

from flock_common.validation import validation_iterator

from flock_builder import ResourceBuilder
from flock_resources.embeddings_loader import EmbeddingsLoaderResource
from flock_schemas import SchemaFactory
from flock_resource_store import ResourceStoreFactory

# Setup
# pylint: disable=C0103
secret_store = None
required_vars = []
optional_vars = ["STORE_TYPE"]


resource_store = ResourceStoreFactory.get_resource_store(
    store_type=os.getenv("STORE_TYPE", "mongo")
)

resource_builder = ResourceBuilder(resource_store=resource_store)
schema_factory = SchemaFactory()


def test_building_resource(manifest):
    """Test building resources from yaml files"""

    manifest_kind = manifest["kind"]

    # test schema validation
    schema_cls = schema_factory.get_schema(manifest_kind)
    schema_instance = schema_cls.validate(manifest)

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


def single_test(file_path, prompt):
    """Test building resources from yaml files"""

    manifest = resource_store.load_file(file_path)
    agent = test_building_resource(manifest)

    agent.run(prompt)  # type: ignore
    # pylint: disable=W0703


def run_build_tests():
    """Run all tests"""
    validation_iterator(
        dir_path="assets/schemas",
        validation_function=test_building_resource,
    )

    embeddings_loader: EmbeddingsLoaderResource = test_building_resource(  # type: ignore
        resource_store.load_file("assets/schemas/2/embeddings_loader.yaml")
    )

    embeddings_loader.load_files_to_vectorstore()

    # OBJECTIVE = "Write a weather report for SF today"
    # single_test(
    #     file_path="../schemas_core/3/agent.yaml",
    #     prompt="Who is the current prime minister of israel?",
    # )

    # single_test(
    #     file_path="../schemas_core/3/agent_with_memory.yaml",
    #     prompt="Who is the current prime minister of israel?",
    # )

    # single_test(
    #     file_path="../schemas_core/4/baby_agi.yaml", prompt={"objective": OBJECTIVE}
    # )

    # gpt4all = test_building_resource(
    #     resource_store.load_file("../schemas_core/0/lllm_openai_gpt4all.yaml")
    # )

    # while True:
    #     user_input = input("User: ")
    #     answer = gpt4all.resource(user_input)
    #     print(f"Agent: {answer}")


run_build_tests()
