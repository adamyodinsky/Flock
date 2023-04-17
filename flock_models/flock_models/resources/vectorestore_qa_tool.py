"""Resource for vectorstore."""

from typing import Any
from flock_models.resources.base import ToolResource
from flock_models.resources.vectorstore import VectorStoreResource
from flock_models.resources.llm import LLMResource
from langchain.chains.qa_with_sources.base import BaseQAWithSourcesChain
from flock_store.resources.base import ResourceStore
from flock_models.schemes.vectorstore_qa_tool import VectorStoreQAToolSchema
from flock_models.schemes.base import Kind


class VectorStoreQATool(ToolResource):
    """Class for vectorstore qa tool."""

    def __init__(self,
            manifest: dict[str, Any],
            retriever: BaseQAWithSourcesChain,
            resource_store: ResourceStore):
        self.manifest = VectorStoreQAToolSchema(**manifest)

        llm_key = f"{Kind.llm.value}/{self.manifest.spec.llm.name}"
        vectorestore_key = f"{Kind.vectorstore.value}/{self.manifest.spec.store.name}"

        vectorestore_resource: VectorStoreResource = resource_store.get_resource(vectorestore_key)
        llm_resource: LLMResource = resource_store.get_data(llm_key)

        self.resource = retriever.from_chain_type(
            **self.manifest.spec.options.dict(),
            llm =llm_resource.resource,
            retriever=vectorestore_resource.resource.as_retriever(),
            )

    def get_name(self) -> str:
        """Get name of tool."""
        return self.manifest.metadata.name
    
    def get_description(self) -> str:
        """Get description of tool."""
        return self.manifest.metadata.description
    
    def get_func(self):
        """Get function of tool."""
        return self.resource

# llm=llm,
# chain_type="stuff",
# retriever=git_vectorstore.as_retriever(),
# reduce_k_below_max_tokens=True,


# apiVersion: flock/v1
# kind: VectorStoreRetrieverTool
# metadata:
#   name: langchain-docs
#   description: retrieve docs from langchain docs vector store
#   labels:
#     app: my_app
# spec:
#   options:
#     chain_type: stuff
#     reduce_k_below_max_tokens: true
#   llm:
#     name: openai
#     labels:
#       app: my_app
#   store:
#     name: documentation_vectorstore
#     labels:
#       app: my_app
    