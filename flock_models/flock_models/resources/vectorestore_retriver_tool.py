"""Resource for vectorstore."""

from typing import Any
from flock_models.schemes.llm import LLMSchema
from flock_models.resources.base import Tool
from langchain.chains.qa_with_sources.base import BaseQAWithSourcesChain
from flock_store.resources.base import ResourceStore



class VectorStoreQATool(Tool):
    """Base class for vectorstore qa tools."""

    def __init__(self, manifest: dict[str, Any], retriever: BaseQAWithSourcesChain, resource_store: ResourceStore):
        super().__init__(manifest, LLMSchema)
        self.resource = retriever.from_chain_type(
            **self.manifest.spec.options.dict(),
            llm=resource_store.get_data(self.manifest.spec.llm.name),
            )
    
    
# original_source_base="https://github.com/hwchase17/langchain/tree/master",
# base_path=base_path,
# archive_path=archive_path,
# splitter=python_splitter,
# vectorstore=git_vectorstore,

# apiVersion: flock/v1
# kind: VectorStoreRetrieverTool
# metadata:
#   name: langchain-docs
#   description: retrieve docs from langchain docs vector store
#   labels:
#     app: my_app
# spec:
#   options:
#       chain_type: stuff
#   llm:
#     name: openai
#     labels:
#       app: my_app
#   store:
#     name: documentation_vectorstore
#     labels:
#       app: my_app
    
