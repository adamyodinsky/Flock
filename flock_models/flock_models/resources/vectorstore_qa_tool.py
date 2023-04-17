"""Resource for vectorstore."""

from typing import Any
from flock_models.resources.base import ToolResource
from langchain.chains.qa_with_sources.base import BaseQAWithSourcesChain
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.vectorstores.base import VectorStore as VectorStoreLC
from langchain.schema import BaseLanguageModel as LCBaseLanguageModel
from flock_models.schemes.base import Kind


class VectorStoreQAToolResource(ToolResource):
    """Class for vectorstore qa tool."""

    VENDORS = {"RetrievalQAWithSourcesChain": RetrievalQAWithSourcesChain}

    def __init__(
        self,
        vendor: str,
        options: dict[str, Any],
        dependencies: dict[str, Any],
    ):
        vendor_cls: BaseQAWithSourcesChain = self.VENDORS[vendor]
        llm: LCBaseLanguageModel = dependencies[Kind.llm.value]
        vectorestore: VectorStoreLC = dependencies[Kind.vectorstore.value]

        self.resource = vendor_cls.from_chain_type(
            **options,
            llm=llm,
            retriever=vectorestore.as_retriever(),
        )
