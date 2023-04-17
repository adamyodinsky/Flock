from flock_models.resources.base import ToolResource, Resource, Agent
from flock_models.resources.agent import AgentResource
from flock_models.resources.embedding import EmbeddingResource
from flock_models.resources.llm import LLMResource
from flock_models.resources.splitter import SplitterResource
from flock_models.resources.vectorstore_qa_tool import VectorStoreQAToolResource
from flock_models.resources.vectorstore import VectorStoreResource

from flock_models.schemes.base import FlockBaseSchema, Dependency as DependencySchema
from flock_models.schemes.vectorstore_qa_tool import VectorStoreQAToolSchema
from flock_models.schemes.vectorstore import VectorStoreSchema
from flock_models.schemes.llm import LLMSchema
from flock_models.schemes.splitter import SplitterSchema
from flock_models.schemes.embedding import EmbeddingSchema
from flock_models.schemes.agent import AgentSchema

from flock_models.schemes.base import Kind

from flock_store.resources.base import ResourceStore
from flock_store.secrets.base import SecretStore


class Builder:
    """Class for building resources."""

    resources = {
        Kind.embedding.value: EmbeddingResource,
        Kind.llm.value: LLMResource,
        Kind.splitter.value: SplitterResource,
        Kind.vectorstore.value: VectorStoreResource,
        Kind.vectorstore_qa_tool.value: VectorStoreQAToolResource,
        Kind.agent.value: AgentResource,
    }

    schemas = {
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

    def build(self, manifest: FlockBaseSchema) -> Resource:
        """Build resource from manifest. recursively build dependencies."""

        dependencies: dict[str, Resource] = {}

        for dependency in manifest.spec.dependencies:
            dependency = DependencySchema(**dependency)
            dependency_key = (
                f"{dependency.namespace}/{dependency.kind}/{dependency.name}"
            )

            dependency_manifest: FlockBaseSchema = self.resource_store.get(
                dependency_key
            )

            dependency_resource = self.build(dependency_manifest)
            dependencies[dependency.kind] = dependency_resource.resource

        resource: Resource = self.resources[manifest.kind]
        resource = Resource(manifest.spec.options, dependencies)
        return resource
