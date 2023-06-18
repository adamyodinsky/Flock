"""Script to generate JSON schemas from pydantic models."""

import json
import os

from flock_deployer.schemas.factory import DeploymentSchemaFactory

PATH = "./assets/json_schemas/"

if not os.path.exists(PATH):
    os.makedirs(PATH)


def write_schemas(schemas):  # pylint: disable=missing-function-docstring
    if not os.path.exists(f"{PATH}"):
        os.makedirs(f"{PATH}")

    for name, schema in schemas.items():
        print(f"Writing {name} - OK")
        schema_json = schema.schema()

        # write to file
        with open(f"{PATH}/{name}.json", "w", encoding="utf-8") as json_file:
            json.dump(schema_json, json_file, indent=2)


def run_script():
    """Main function."""
    deployment_schema_factory = DeploymentSchemaFactory()
    schemas = deployment_schema_factory.schemas
    write_schemas(schemas)


if __name__ == "__main__":
    run_script()
