"""This module will handle the building of the manifest file for the flock."""
from flock_models.schemes import Schemas, Kind, FlockBaseSchema, AgentSchema
from pydantic.schema import schema
import json

for kind in Schemas:
    print(f"Kind: {kind}")
    
    
# print(AgentSchema.schema_json())
