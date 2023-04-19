import json
import os
from flock_models.schemes import Schemas

path = "openapi/pydantic_to_json/"

if not os.path.exists(path):
    os.makedirs(path)

for kind in Schemas:
    print(f"Kind: {kind}")
    schema_json = Schemas[kind].schema()
    
    # write to file
    with open(f"{path}/{kind}.json", "w") as json_file:
        json.dump(schema_json, json_file, indent=2)
        
