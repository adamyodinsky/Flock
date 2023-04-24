"""Resource builder."""

from typing import Any, Union
import flock_schemas as schemas
from flock_schemas.base import ToolDependency as ToolDependencySchema
from flock_resource_store import ResourceStore

from flock_models.resources import Resource, AgentResource, ToolResource, Resources
from flock_models.builder.plugins_loader import load_plugins


class ResourceBuilder:
    """Class for building resources."""

    def __init__(self, resource_store: ResourceStore):
        self.resource_store = resource_store
        self.resources = Resources
        self.plugins = load_plugins("plugins")
        self.merged_resources = {**self.plugins, **self.resources}

    def __build_recursive(
        self, dependencies_section, dependencies: dict[str, Resource]
    ) -> None:
        """Build resource from manifest. recursively build dependencies."""

        for dependency in dependencies_section:
            dependency_key = (
                f"{dependency.namespace}/{dependency.kind}/{dependency.name}"
            )

            dependency_manifest = self.resource_store.get_model(
                dependency_key, schemas.Schemas[dependency.kind]
            )

            dependency_resource = self.build_resource(dependency_manifest)
            dependencies[dependency.kind] = dependency_resource

    def build_resource(self, manifest: schemas.BaseFlockSchema) -> Resource:
        """Build resource from manifest. recursively build dependencies."""

        dependencies_bucket: dict[str, Resource] = {}
        dependencies_section = getattr(manifest.spec, "dependencies", [])
        self.__build_recursive(dependencies_section, dependencies_bucket)

        tools_bucket: dict[str, Resource] = {}
        tools_section: ToolDependencySchema = getattr(manifest.spec, "tools", [])
        self.__build_recursive(tools_section, tools_bucket)

        resource = self.merged_resources[manifest.kind](
            manifest=manifest,
            dependencies=dependencies_bucket,
            tools=list(tools_bucket.values()),
        )
        return resource
