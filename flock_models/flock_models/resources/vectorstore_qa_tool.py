"""Resource for vectorstore."""

from typing import Any
from flock_models.resources.base import ToolResource
from langchain.chains.qa_with_sources.base import BaseQAWithSourcesChain
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.vectorstores.base import VectorStore as LCVectorStore
from langchain.schema import BaseLanguageModel as LCBaseLanguageModel

from flock_models.schemes.vectorstore_qa_tool import VectorStoreQAToolVendor
from flock_models.schemes.base import Kind



class VectorStoreQAToolResource(ToolResource):
    """Class for vectorstore qa tool."""
    
    CHAINS_CLS = {
        "RetrievalQAWithSourcesChain": RetrievalQAWithSourcesChain
    }

    def __init__(
        self,
        options: dict[str, Any],
        dependencies: dict[str, Any],
        vendor: str
    ):
        llm: LCBaseLanguageModel = dependencies[Kind.llm.value]
        vectorestore: LCVectorStore = dependencies[Kind.vectorstore.value]
        vendor_cls: BaseQAWithSourcesChain = self.CHAINS_CLS[VectorStoreQAToolVendor[vendor].value]
        
        self.resource = vendor_cls.from_chain_type(
            **options,
            llm=llm,
            retriever=vectorestore.as_retriever(),
        )
