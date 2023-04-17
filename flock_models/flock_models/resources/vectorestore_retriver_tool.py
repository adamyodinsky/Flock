"""Resource for vectorstore."""

from typing import Any
from flock_models.resources.base import Tool
from flock_models.resources.vectorstore import VectorStoreResource
from flock_models.resources.llm import LLMResource
from langchain.chains.qa_with_sources.base import BaseQAWithSourcesChain
from flock_store.resources.base import ResourceStore
from flock_models.schemes.vectorstore_retriever_tool import VectorStoreQAToolSchema
from langchain.vectorstores.base import VectorStore
from langchain.schema import BaseLanguageModel


class VectorStoreQATool(Tool):
    """Class for vectorstore qa tool."""

    def __init__(self,
            manifest: dict[str, Any],
            retriever: BaseQAWithSourcesChain,
            resource_store: ResourceStore):
        self.manifest = VectorStoreQAToolSchema(**manifest)

        llm_key = f"{self.manifest.kind}/{self.manifest.spec.llm.name}"
        vectorestore_key = f"{self.manifest.kind}/{self.manifest.spec.store.name}"

        vectorestore_resource: VectorStoreResource = resource_store.get_data(vectorestore_key)
        llm_resource: LLMResource = resource_store.get_data(llm_key)

        self.resource = retriever.from_chain_type(
            **self.manifest.spec.options.dict(),
            llm =llm_resource.resource,
            retriever=vectorestore_resource.resource.as_retriever(),
            )



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
    