"""Resource for vectorstore."""

from typing import Any
from flock_models.resources.base import ToolResource
from langchain.chains.qa_with_sources.base import BaseQAWithSourcesChain
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.vectorstores.base import VectorStore as VectorStoreLC
from langchain.agents import Tool as ToolWarperLC
from langchain.schema import BaseLanguageModel as LCBaseLanguageModel
from flock_models.schemes.base import FlockBaseSchema, Kind


class VectorStoreQAToolResource(ToolResource):
    """Class for vectorstore qa tool."""

    VENDORS = {"RetrievalQAWithSourcesChain": RetrievalQAWithSourcesChain}

    def __init__(
        self,
        manifest: FlockBaseSchema,
        dependencies: dict[str, Any]
    ):
        super().__init__(manifest, dependencies)
        vendor_cls: BaseQAWithSourcesChain = self.VENDORS[self.vendor]
        llm: LCBaseLanguageModel = self.dependencies[Kind.llm.value]
        vectorestore: VectorStoreLC = self.dependencies[Kind.vectorstore.value]

        self.tool_function = vendor_cls.from_chain_type(
            **self.options,
            llm=llm,
            retriever=vectorestore.as_retriever(),
        )
        
        self.resource = ToolWarperLC(
            name=self.name,
            description=self.description,
            func=self.tool_function,
        )
