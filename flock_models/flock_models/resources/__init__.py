from flock_models.resources.agent import AgentResource
from flock_models.resources.base import Agent, Resource, ToolResource
from flock_models.resources.embedding import EmbeddingResource
from flock_models.resources.embeddings_loader import EmbeddingsLoaderResource
from flock_models.resources.llm import LLMResource
from flock_models.resources.llm_chat import LLMChatResource
from flock_models.resources.llm_tool import LLMToolResource
from flock_models.resources.load_tool import LoadToolResource
from flock_models.resources.prompt_template import PromptTemplateResource
from flock_models.resources.splitter import SplitterResource
from flock_models.resources.vectorstore import VectorStoreResource
from flock_models.resources.vectorstore_qa_tool import VectorStoreQAToolResource

Resources = {
    "Embedding": EmbeddingResource,
    "LLM": LLMResource,
    "LLMChat": LLMChatResource,
    "LoadTool": LoadToolResource,
    "VectorStore": VectorStoreResource,
    "VectorStoreQATool": VectorStoreQAToolResource,
    "Agent": AgentResource,
    "Splitter": SplitterResource,
    "PromptTemplate": PromptTemplateResource,
    "LLMTool": LLMToolResource,
    "EmbeddingsLoader": EmbeddingsLoaderResource,
}


# factory
class ResourceFactory:
    """Factory class for resources."""

    def __init__(self, manifest: dict):
        self.manifest = manifest

    @staticmethod
    def get_resource(manifest):
        """Get resource."""
        resource_kind = manifest.get("kind")
        if resource_kind is None:
            raise ValueError("Resource type is not specified")
        resource_cls = Resources.get(resource_kind)
        if resource_cls is None:
            raise ValueError(f"Resource type {resource_kind} is not supported")
        return resource_cls(manifest, None)
