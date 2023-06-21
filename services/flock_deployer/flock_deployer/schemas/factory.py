import importlib
import os
from typing import Any, Type

from flock_deployer import schemas
from pydantic import BaseModel


class DeploymentSchemaFactory:
    """Factory class for schemas."""

    def __init__(self):
        self.schemas = self.load_schemas()
        self.sub_schemas = self.load_schemas("sub")

    def load_schemas(
        self,
        sub_path: str = "main",
        schemas_dir: str = "schemas",
    ) -> dict[str, Any]:
        """Load schemas from flock_schemas module."""

        schemas_map = {}

        module_dir = os.path.dirname(schemas.__file__)

        for file in os.listdir(module_dir):
            path = os.path.join(module_dir, file)

            if os.path.isfile(path):
                if file.endswith(".py") and file != "__init__.py":
                    module_name = file[:-3]
                    module = importlib.import_module(
                        f"flock_deployer.{schemas_dir}.{module_name}"
                    )

                    for key, value in module.export[sub_path].items():
                        schemas_map[key] = value

        return schemas_map

    def get_schema(self, kind: str) -> Type[BaseModel]:
        """Get a schema instance."""

        result = self.schemas.get(kind, None)
        if result is None:
            raise ValueError(f"Invalid kind: {kind}")

        return result

    def get_sub_schema(self, kind: str) -> Type[BaseModel]:
        """Get a schema instance."""

        result = self.sub_schemas.get(kind, None)
        if result is None:
            raise ValueError(f"Invalid kind: {kind}")

        return result


export = {
    "sub": {},
    "main": {},
}
