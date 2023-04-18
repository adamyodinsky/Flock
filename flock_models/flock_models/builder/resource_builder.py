"""Resource builder."""

from flock_store.resources import ResourceStore
from flock_store.secrets import SecretStore
from flock_models.resources import Agent, Resource, Resources
from flock_models import schemes


class ResourceBuilder:
    """Class for building resources."""

    def __init__(self, resource_store: ResourceStore, secret_store: SecretStore = None):
        self.resource_store = resource_store
        self.secret_store = secret_store

    def __build_recursive(
        self, dependencies_section, dependencies: dict[str, Resource]
    ) -> Resource:
        """Build resource from manifest. recursively build dependencies."""

        for dependency in dependencies_section:
            dependency_key = (
                f"{dependency.namespace}/{dependency.kind}/{dependency.name}"
            )

            dependency_manifest: schemes.FlockBaseSchema = self.resource_store.get_model(
                dependency_key, schemes.Schemas[dependency.kind]
            )

            dependency_resource = self.build_resource(dependency_manifest)
            dependencies[dependency.kind] = dependency_resource.resource

    def build_resource(self, manifest: schemes.FlockBaseSchema) -> Resource:
        """Build resource from manifest. recursively build dependencies."""

        dependencies_bucket: dict[str, Resource] = {}
        dependencies_section = getattr(manifest.spec, 'dependencies', [])
        self.__build_recursive(dependencies_section, dependencies_bucket)

        resource: Resource = Resources[manifest.kind]
        resource = Resource(manifest, dependencies_bucket)
        return resource

    def build_agent(self, manifest: schemes.AgentSchema) -> Agent:
        """Build agent from manifest."""

        dependencies_bucket: dict[str, Resource] = {}
        dependencies_list = getattr(manifest.spec, 'dependencies', [])
        self.__build_recursive(dependencies_list, dependencies_bucket)

        tools_list: dict[str, Resource] = {}
        tools_bucket = getattr(manifest.spec, 'tools', [])
        self.__build_recursive(tools_list, tools_bucket)

        agent_resource = schemes.AgentResource(
            vendor=manifest.spec.vendor,
            options=manifest.spec.options,
            dependencies=dependencies_bucket,
            tools=tools_bucket,
        )

        return agent_resource
