"""Script to generate JSON schemas from pydantic models."""

import os

from flock_schema_store import SchemaStoreFactory
from flock_schemas import SchemaFactory

PATH = "../../assets/json_schemas/"

if not os.path.exists(PATH):
    os.makedirs(PATH)

schema_store = SchemaStoreFactory.get_store("mongo")


def upload_json_schema(name, schema: dict):
    """Upload a schema to the schema store."""

    print(f"Uploading {name} - ", end="", flush=True)
    schema_store.put(
        {
            "kind": name,
            "schema": schema,
        }
    )

    print("OK")


def upload_reduced_schema(kind_name, schema):
    """Upload a schema to the schema store."""

    vendors_list = []
    dependencies_list = []

    print(f"Uploading {kind_name} - ", end="", flush=True)

    # Get spec
    spec_name = (
        schema.get("properties", {}).get("spec", {}).get("$ref", "").split("/")[-1]
    )
    spec = schema.get("definitions", {}).get(spec_name, {})

    # Get Vendor list
    vendor_name = (
        spec.get("properties", {})
        .get("vendor", {})
        .get("allOf", [{}])[0]
        .get("$ref", "")
        .split("/")[-1]
    )

    if vendor_name:
        vendors_list = (
            schema.get("definitions", {}).get(vendor_name, []).get("enum", [])
        )

    # Get dependencies list
    dependencies = spec.get("properties", {}).get("dependencies", {}).get("items", [])
    for dependency in dependencies:
        dependency_name = dependency["$ref"].split("/")[-1]
        dependency_name = (
            schema.get("definitions", {})
            .get(dependency_name, [])
            .get("properties", {})
            .get("kind", {})
            .get("const", "")
        )

        if dependency_name:
            dependencies_list.append(dependency_name)

    schema_store.put(
        {
            "kind": kind_name,
            "vendor": vendors_list,
            "dependencies": dependencies_list,
        }
    )

    print("OK")


def upload_schemas(schemas):
    for name, schema in schemas.items():
        schema_json = schema.schema()
        # upload_json_schema(name, schema_json)
        upload_reduced_schema(name, schema_json)


def run_script():
    """Main function."""

    schema_factory = SchemaFactory()
    # sub_schemas_map = schema_factory.load_schemas("sub")
    main_schemas_map = schema_factory.load_schemas()
    # upload_schemas(sub_schemas_map)
    upload_schemas(main_schemas_map)


if __name__ == "__main__":
    run_script()
