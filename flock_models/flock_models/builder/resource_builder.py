"""Resource builder."""


from flock_resource_store import ResourceStore
from flock_schemas import SchemasFactory
from flock_models.builder.plugins_loader import load_plugins
from flock_models.resources import Resource, Resources


class ResourceBuilder:
    """Class for building resources."""

    def __init__(self, resource_store: ResourceStore):
        self.resource_store = resource_store
        self.resources = Resources
        self.plugins = load_plugins("plugins")
        self.merged_resources = {**self.plugins, **self.resources}

    def __build_dependencies_recursively(
        self, dependencies_section, dependencies: dict[str, Resource]
    ) -> None:
        """Build resource from manifest. recursively build dependencies."""

        for dependency in dependencies_section:
            dependency_key = (
                f"{dependency['namespace']}/{dependency['kind']}/{dependency['name']}"
            )

            dependency_manifest = self.resource_store.get(dependency_key)
            dependency_resource = self.build_resource(dependency_manifest)
            dependencies[dependency["kind"]] = dependency_resource

    def build_resource(self, manifest: dict) -> Resource:
        """Build resource from manifest. recursively build dependencies."""

        manifest_kind = manifest["kind"]
        dependencies_bucket: dict[str, Resource] = {}
        dependencies_section = manifest["spec"].get("dependencies", [])

        self.__build_dependencies_recursively(dependencies_section, dependencies_bucket)

        tools_bucket: dict[str, Resource] = {}
        tools_section = manifest["spec"].get("tools", [])

        self.__build_dependencies_recursively(tools_section, tools_bucket)

        schema_cls = SchemasFactory.get_schema(manifest_kind)
        schema_instance = schema_cls.validate(manifest)

        resource = self.merged_resources[manifest_kind](
            manifest=schema_instance,
            dependencies=dependencies_bucket,
            tools=list(tools_bucket.values()),
        )
        return resource
