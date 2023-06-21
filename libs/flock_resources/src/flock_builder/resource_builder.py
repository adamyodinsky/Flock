"""Resource builder."""


from typing import List

from flock_resource_store import ResourceStore
from flock_schemas import SchemaFactory

from flock_resources import Resource, ResourceFactory


class ResourceBuilder:
    """Class for building resources."""

    def __init__(self, resource_store: ResourceStore):
        """Initialize the class."""
        self.resource_store = resource_store
        self.resources = ResourceFactory().resources
        self.schema_factory = SchemaFactory()

    def __build_dependencies_recursively(
        self,
        dependencies_section,
        dependencies_bucket: dict[str, Resource],
        dry_run: bool,
    ) -> None:
        """Build resource from manifest. recursively build dependencies."""

        for dependency in dependencies_section:
            dependency_manifest = self.resource_store.get(
                namespace=dependency["namespace"],
                kind=dependency["kind"],
                name=dependency["name"],
            )
            dependency_resource = self.build_resource(dependency_manifest, dry_run)
            dependencies_bucket[dependency["kind"]] = dependency_resource

    def __build_tools_recursively(
        self, dependencies_section, tools_bucket: List[Resource], dry_run: bool
    ) -> None:
        """Build resource from manifest. recursively build dependencies."""

        for dependency in dependencies_section:
            dependency_manifest = self.resource_store.get(
                namespace=dependency["namespace"],
                kind=dependency["kind"],
                name=dependency["name"],
            )
            dependency_resource = self.build_resource(dependency_manifest, dry_run)
            tools_bucket.append(dependency_resource)

    def build_resource(self, manifest: dict, dry_run: bool = False) -> Resource:
        """Build resource from manifest. recursively build dependencies."""

        manifest_kind = manifest["kind"]
        dependencies_bucket: dict[str, Resource] = {}
        dependencies_section = manifest["spec"].get("dependencies", [])

        self.__build_dependencies_recursively(
            dependencies_section, dependencies_bucket, dry_run
        )

        tools_bucket: List[Resource] = []
        tools_section = manifest["spec"].get("tools", [])

        self.__build_tools_recursively(tools_section, tools_bucket, dry_run)

        schema_cls = self.schema_factory.get_schema(manifest_kind)
        schema_instance = schema_cls.validate(manifest)

        resource = self.resources[manifest_kind](
            manifest=schema_instance,
            dependencies=dependencies_bucket,
            tools=tools_bucket,
            dry_run=dry_run,
        )
        return resource
