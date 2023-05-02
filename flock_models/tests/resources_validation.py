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


def test_building_resource(manifest):
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


def single_test(file_path, prompt="Who is the current prime minister of israel?"):
    """Test building resources from yaml files"""

    manifest = resource_store.load_file(file_path)
    agent: resources.AgentResource = cast(
        resources.AgentResource, test_building_resource(manifest)
    )

    try:
        agent.resource.run(prompt)
    # pylint: disable=W0703
    except Exception as e:
        print(str(e))


def run_build_tests():
    """Run all tests"""
    validation_iterator(
        dir_path="../schemas_core",
        validation_function=test_building_resource,
    )

    single_test("../schemas_core/3/agent.yaml")
    # single_test("../schemas_core/4/baby_agi.yaml")


run_build_tests()
