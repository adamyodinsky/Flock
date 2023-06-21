"""Script to generate JSON schemas from pydantic models."""

import os

from flock_schema_store import SchemaStoreFactory
from flock_schemas import SchemaFactory

PATH = "../../assets/json_schemas/"

if not os.path.exists(PATH):
    os.makedirs(PATH)

schema_store = SchemaStoreFactory.get_store("mongo")


def upload_schema(name, schema: dict):
    """Upload a schema to the schema store."""

    print(f"Uploading {name} - ", end="", flush=True)
    schema_store.put(
        {
            "kind": name,
            "schema": schema,
        }
    )

    print("OK")


def upload_schemas(schemas):
    for name, schema in schemas.items():
        schema_json = schema.schema()
        upload_schema(name, schema_json)


def run_script():
    """Main function."""

    schema_factory = SchemaFactory()
    sub_schemas_map = schema_factory.load_schemas("sub")
    main_schemas_map = schema_factory.load_schemas()
    upload_schemas(sub_schemas_map)
    upload_schemas(main_schemas_map)


if __name__ == "__main__":
    run_script()
