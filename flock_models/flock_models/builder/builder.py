from flock_store.resources.base import ResourceStore
from flock_store.secrets.base import SecretStore


from flock_models.schemes.base import (
    FlockBaseSchema,
    Dependency as DependencySchema,
    Kind,
)
from flock_models.resources.agent import AgentResource
from flock_models.resources.embedding import EmbeddingResource
from flock_models.resources.llm import LLMResource
from flock_models.resources.splitter import SplitterResource
from flock_models.resources.vectorstore_qa_tool import VectorStoreQAToolResource
from flock_models.resources.vectorstore import VectorStoreResource

from flock_models.resources.base import ToolResource, Resource, Agent
from flock_models.schemes.vectorstore_qa_tool import VectorStoreQAToolSchema
from flock_models.schemes.vectorstore import VectorStoreSchema
from flock_models.schemes.llm import LLMSchema
from flock_models.schemes.splitter import SplitterSchema
from flock_models.schemes.embedding import EmbeddingSchema
from flock_models.schemes.agent import AgentSchema


class Builder:
    """Class for building resources."""

    RESOURCES = {
        Kind.embedding.value: EmbeddingResource,
        Kind.llm.value: LLMResource,
        Kind.splitter.value: SplitterResource,
        Kind.vectorstore.value: VectorStoreResource,
        Kind.vectorstore_qa_tool.value: VectorStoreQAToolResource,
        Kind.agent.value: AgentResource,
    }

    SCHEMAS = {
        Kind.embedding.value: EmbeddingSchema,
        Kind.llm.value: LLMSchema,
        Kind.splitter.value: SplitterSchema,
        Kind.vectorstore.value: VectorStoreSchema,
        Kind.vectorstore_qa_tool.value: VectorStoreQAToolSchema,
        Kind.agent.value: AgentSchema,
    }

    def __init__(self, resource_store: ResourceStore, secret_store: SecretStore = None):
        self.resource_store = resource_store
        self.secret_store = secret_store

    def _build_recursive(
        self, dependencies_manifest: FlockBaseSchema, dependencies: dict[str, Resource]
    ) -> Resource:
        """Build resource from manifest. recursively build dependencies."""

        for dependency in dependencies_manifest:
            dependency = DependencySchema(**dependency)
            dependency_key = (
                f"{dependency.namespace}/{dependency.kind}/{dependency.name}"
            )

            dependency_manifest: FlockBaseSchema = self.resource_store.get(
                dependency_key
            )

            dependency_resource = self.build(dependency_manifest)
            dependencies[dependency.kind] = dependency_resource.resource

    def build(self, manifest: FlockBaseSchema) -> Resource:
        """Build resource from manifest. recursively build dependencies."""

        dependencies: dict[str, Resource] = {}
        self._build_recursive(manifest.spec.dependencies, dependencies)

        resource: Resource = self.RESOURCES[manifest.kind]
        resource = Resource(manifest, dependencies)
        return resource


    def build_agent(self, manifest: AgentSchema) -> Agent:
        """Build agent from manifest."""

        dependencies: dict[str, Resource] = {}
        self._build_recursive(manifest.spec.dependencies, dependencies)

        tools: dict[str, Resource] = {}
        self._build_recursive(manifest.spec.dependencies, tools)

        agent_resource = AgentResource(
            vendor=manifest.spec.vendor,
            options=manifest.spec.options,
            dependencies=dependencies,
            tools=tools,
        )

        return agent_resource
