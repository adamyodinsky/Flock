"""Script to generate JSON schemas from pydantic models."""

import json
import os

from flock_deployer.schemas.factory import DeploymentSchemaFactory

PATH = "./assets/json_schemas/"

if not os.path.exists(PATH):
    os.makedirs(PATH)


def write_schemas(schemas, sub_path: str):
    if not os.path.exists(f"{PATH}/{sub_path}"):
        os.makedirs(f"{PATH}/{sub_path}")

    for name, schema in schemas.items():
        print(f"Writing {name} - ", end="", flush=True)
        schema_json = schema.schema()
        # write to file
        with open(f"{PATH}/{sub_path}/{name}.json", "w", encoding="utf-8") as json_file:
            json.dump(schema_json, json_file, indent=2)
        print("OK")


def run_script():
    """Main function."""
    deployment_schema_factory = DeploymentSchemaFactory()
    sub_schemas = deployment_schema_factory.sub_schemas
    schemas = deployment_schema_factory.schemas
    write_schemas(sub_schemas, "sub")
    write_schemas(schemas, "main")


if __name__ == "__main__":
    run_script()
