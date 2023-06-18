"""Script to generate JSON schemas from pydantic models."""

import json
import os

from flock_schema_store import SchemaStoreFactory
from flock_schemas import SchemaFactory

PATH = "../../assets/json_schemas/"

if not os.path.exists(PATH):
    os.makedirs(PATH)

schema_store = SchemaStoreFactory.get_store("mongo")


def write_schemas(schemas, sub_path: str):  # pylint: disable=missing-function-docstring
    if not os.path.exists(f"{PATH}/{sub_path}"):
        os.makedirs(f"{PATH}/{sub_path}")

    for name, schema in schemas.items():
        print(f"Writing {name} - ", end="", flush=True)
        schema_json = schema.schema()
        # write to file
        with open(f"{PATH}/{sub_path}/{name}.json", "w", encoding="utf-8") as json_file:
            json.dump(schema_json, json_file, indent=2)
        print("OK - ", flush=True, end="")

        upload_schema(name, schema_json)


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


def run_script():
    """Main function."""

    schema_factory = SchemaFactory()
    main_schemas_map = schema_factory.load_schemas()
    write_schemas(main_schemas_map, "main")


if __name__ == "__main__":
    run_script()
