"""Script to generate JSON schemas from pydantic models."""

import json
import os

from flock_schemas import SchemasFactory

PATH = "openapi/schemas/"

if not os.path.exists(PATH):
    os.makedirs(PATH)


def write_schemas(schemas, sub_path: str):  # pylint: disable=missing-function-docstring
    if not os.path.exists(f"{PATH}/{sub_path}"):
        os.makedirs(f"{PATH}/{sub_path}")

    for name, schema in schemas.items():
        print(f"Writing {name} - OK")
        schema_json = schema.schema()

        # write to file
        with open(f"{PATH}/{sub_path}/{name}.json", "w", encoding="utf-8") as json_file:
            json.dump(schema_json, json_file, indent=2)


def run_script():
    """Main function."""

    sub_schemas_map, main_schemas_map = SchemasFactory.load_schemas()
    write_schemas(sub_schemas_map, "sub")
    write_schemas(main_schemas_map, "main")


if __name__ == "__main__":
    run_script()
