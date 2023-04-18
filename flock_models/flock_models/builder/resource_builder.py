"""Resource builder."""

from flock_store.resources import ResourceStore
from flock_store.secrets import SecretStore
from flock_models.resources import Agent, Resource
from flock_models import schemes


class ResourceBuilder:
    """Class for building resources."""

    def __init__(self, resource_store: ResourceStore, secret_store: SecretStore = None):
        self.resource_store = resource_store
        self.secret_store = secret_store

    def __build_recursive(
        self, dependencies_manifest: schemes.FlockBaseSchema, dependencies: dict[str, Resource]
    ) -> Resource:
        """Build resource from manifest. recursively build dependencies."""

        for dependency in dependencies_manifest:
            dependency = schemes.DependencySchema(**dependency)
            dependency_key = (
                f"{dependency.namespace}/{dependency.kind}/{dependency.name}"
            )

            dependency_manifest: schemes.FlockBaseSchema = self.resource_store.get(
                dependency_key
            )

            dependency_resource = self.build(dependency_manifest)
            dependencies[dependency.kind] = dependency_resource.resource

    def build_resource(self, manifest: schemes.FlockBaseSchema) -> Resource:
        """Build resource from manifest. recursively build dependencies."""

        dependencies: dict[str, Resource] = {}
        self.__build_recursive(manifest.spec.dependencies, dependencies)

        resource: Resource = self.RESOURCES[manifest.kind]
        resource = Resource(manifest, dependencies)
        return resource

    def build_agent(self, manifest: schemes.AgentSchema) -> Agent:
        """Build agent from manifest."""

        dependencies: dict[str, Resource] = {}
        self.__build_recursive(manifest.spec.dependencies, dependencies)

        tools: dict[str, Resource] = {}
        self.__build_recursive(manifest.spec.dependencies, tools)

        agent_resource = schemes.AgentResource(
            vendor=manifest.spec.vendor,
            options=manifest.spec.options,
            dependencies=dependencies,
            tools=tools,
        )

        return agent_resource
