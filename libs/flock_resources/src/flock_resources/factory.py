import importlib
import os
from typing import Type

import flock_resources
from flock_resources.base import Resource


class ResourceFactory:
    """Factory class for resources."""

    def __init__(self):
        self.resources = self.load_resources()

    def get_resource(self, manifest):
        """Get resource."""
        resource_kind = manifest.get("kind")
        if resource_kind is None:
            raise ValueError("Resource type is not specified")
        resource_cls = self.resources.get(resource_kind)
        if resource_cls is None:
            raise ValueError(f"Resource type {resource_kind} is not supported")
        return resource_cls(manifest, None)

    def load_resources(
        self, resources_dir: str = "flock_resources"
    ) -> dict[str, Type[Resource]]:
        """Load resources from resources module."""

        resources_map = {}

        module_dir = os.path.dirname(flock_resources.__file__)

        for file in os.listdir(module_dir):
            path = os.path.join(module_dir, file)

            if os.path.isfile(path):
                if file.endswith(".py") and file != "__init__.py":
                    module_name = file[:-3]
                    module = importlib.import_module(f"{resources_dir}.{module_name}")

                    for key, value in module.export.items():
                        resources_map[key] = value

        return resources_map


export = {}
