"""Resource for vectorstore."""

from typing import Any

from flock_schemas import VectorStoreQAToolSchema
from flock_schemas import Kind
from langchain.agents import Tool as ToolWarperLC
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources.base import BaseQAWithSourcesChain
from langchain.schema import BaseLanguageModel as LCBaseLanguageModel
from langchain.vectorstores.base import VectorStore as VectorStoreLC

from flock_models.resources.base import ToolResource


class VectorStoreQAToolResource(ToolResource):
    """Class for vectorstore qa tool."""

    VENDORS = {"RetrievalQAWithSourcesChain": RetrievalQAWithSourcesChain}

    def __init__(
        self,
        manifest: VectorStoreQAToolSchema,
        dependencies: dict[str, Any],
        tools: list[Any] = [],
    ):
        super().__init__(manifest, dependencies)
        self.vendor_cls: BaseQAWithSourcesChain = self.VENDORS[self.vendor]
        self.llm: LCBaseLanguageModel = self.dependencies[Kind.LLM].resource
        self.vectorestore: VectorStoreLC = self.dependencies[Kind.VectorStore].resource

        self.tool_function = self.vendor_cls.from_chain_type(
            **self.options,
            llm=self.llm,
            retriever=self.vectorestore.as_retriever(),
        )

        self.resource = ToolWarperLC(
            name=self.name,
            description=self.description,
            func=self.tool_function,
        )
