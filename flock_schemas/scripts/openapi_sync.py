"""Script to generate JSON schemas from pydantic models."""

import importlib
import json
import os
from typing import Tuple

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


def load_schemas(schemas_dir: str = "flock_schemas") -> Tuple[dict, dict]:
    """Load schemas from flock_schemas directory."""

    sub_schemas_map = {}
    main_schemas_map = {}

    # if plugin_directory not exist return empty dict
    if not os.path.isdir(schemas_dir):
        return sub_schemas_map, main_schemas_map

    for file in os.listdir(schemas_dir):
        if file.endswith(".py") and file != "__init__.py":
            module_name = file[:-3]
            module = importlib.import_module(f"{schemas_dir}.{module_name}")

            for key, value in module.export["sub"].items():
                sub_schemas_map[key] = value

            for key, value in module.export["main"].items():
                main_schemas_map[key] = value
    return sub_schemas_map, main_schemas_map


def run_script():
    """Main function."""

    sub_schemas_map, main_schemas_map = load_schemas()
    write_schemas(sub_schemas_map, "sub")
    write_schemas(main_schemas_map, "main")


if __name__ == "__main__":
    run_script()
