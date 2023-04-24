import json
import os

from flock_schemas import DependencySchema, MetaDataSchema
from flock_schemas import Schemas as resource_schemas

path = "openapi/pydantic_to_json/"

if not os.path.exists(path):
    os.makedirs(path)

meta_schemas = {"MetaData": MetaDataSchema, "Dependency": DependencySchema}


def write_schemas(schemas):
    for kind in schemas:
        print(f"Writing {kind} - OK")
        schema_json = schemas[kind].schema()

        # write to file
        with open(f"{path}/{kind}.json", "w") as json_file:
            json.dump(schema_json, json_file, indent=2)


write_schemas(resource_schemas)
write_schemas(meta_schemas)
