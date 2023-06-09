"""Resource builder."""


from typing import List

from resources import Resource, ResourceFactory
from schemas import SchemaFactory
from store import ResourceStore


class ResourceBuilder:
    """Class for building resources."""

    def __init__(self, resource_store: ResourceStore):
        """Initialize the class."""
        self.resource_store = resource_store
        self.resources = ResourceFactory().resources
        self.schema_factory = SchemaFactory()

    def __build_dependencies_recursively(
        self, dependencies_section, dependencies_bucket: dict[str, Resource]
    ) -> None:
        """Build resource from manifest. recursively build dependencies."""

        for dependency in dependencies_section:
            dependency_manifest = self.resource_store.get(
                namespace=dependency["namespace"],
                kind=dependency["kind"],
                name=dependency["name"],
            )
            dependency_resource = self.build_resource(dependency_manifest)
            dependencies_bucket[dependency["kind"]] = dependency_resource

    def __build_tools_recursively(
        self, dependencies_section, tools_bucket: List[Resource]
    ) -> None:
        """Build resource from manifest. recursively build dependencies."""

        for dependency in dependencies_section:
            dependency_manifest = self.resource_store.get(
                namespace=dependency["namespace"],
                kind=dependency["kind"],
                name=dependency["name"],
            )
            dependency_resource = self.build_resource(dependency_manifest)
            tools_bucket.append(dependency_resource)

    def build_resource(self, manifest: dict) -> Resource:
        """Build resource from manifest. recursively build dependencies."""

        manifest_kind = manifest["kind"]
        dependencies_bucket: dict[str, Resource] = {}
        dependencies_section = manifest["spec"].get("dependencies", [])

        self.__build_dependencies_recursively(dependencies_section, dependencies_bucket)

        tools_bucket: List[Resource] = []
        tools_section = manifest["spec"].get("tools", [])

        self.__build_tools_recursively(tools_section, tools_bucket)

        schema_cls = self.schema_factory.get_schema(manifest_kind)
        schema_instance = schema_cls.validate(manifest)

        resource = self.resources[manifest_kind](
            manifest=schema_instance,
            dependencies=dependencies_bucket,
            tools=tools_bucket,
        )
        return resource
