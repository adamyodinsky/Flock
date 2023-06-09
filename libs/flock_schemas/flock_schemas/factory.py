import importlib
import os
from typing import Type

import flock_schemas
from flock_schemas.base import BaseFlockSchema
from flock_schemas.custom import CustomSchema


class SchemaFactory:
    """Factory class for schemas."""

    def __init__(self):
        self.schemas = self.load_schemas()

    def load_schemas(
        self, schemas_dir: str = "flock_schemas"
    ) -> dict[str, Type[BaseFlockSchema]]:
        """Load schemas from flock_schemas module."""

        schemas_map = {}

        module_dir = os.path.dirname(flock_schemas.__file__)

        for file in os.listdir(module_dir):
            path = os.path.join(module_dir, file)

            if os.path.isfile(path):
                if file.endswith(".py") and file != "__init__.py":
                    module_name = file[:-3]
                    module = importlib.import_module(f"{schemas_dir}.{module_name}")

                    for key, value in module.export["main"].items():
                        schemas_map[key] = value

        return schemas_map

    def get_schema(self, kind: str) -> Type[BaseFlockSchema]:
        """Get a schema instance."""

        result = self.schemas.get(kind, CustomSchema)
        return result


export = {
    "sub": {},
    "main": {},
}
