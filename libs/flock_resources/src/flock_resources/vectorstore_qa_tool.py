"""Resource for vectorstore."""

from typing import Dict, List, Optional, cast

from langchain.agents import Tool as ToolWarperLC
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources.base import BaseQAWithSourcesChain
from langchain.chains.qa_with_sources.vector_db import VectorDBQAWithSourcesChain
from langchain.vectorstores.base import VectorStore as VectorStoreLC

from flock_resources.base import Resource, ToolResource
from flock_schemas import Kind
from flock_schemas.vectorstore_qa_tool import VectorStoreQAToolSchema


class VectorStoreQAToolResource(ToolResource):
    """Class for vectorstore qa tool."""

    VENDORS = {
        "RetrievalQAWithSourcesChain": RetrievalQAWithSourcesChain,
        "VectorDBQAWithSourcesChain": VectorDBQAWithSourcesChain,
    }

    def __init__(
        self,
        manifest: VectorStoreQAToolSchema,
        dependencies: Optional[Dict[str, Resource]],
        tools: Optional[List[ToolResource]] = None,
    ):
        super().__init__(manifest, dependencies)

        if tools is None:
            tools = []

        self.vendor_cls: BaseQAWithSourcesChain = cast(
            BaseQAWithSourcesChain, self.VENDORS[self.vendor]
        )
        self.vectorestore: VectorStoreLC = self.dependencies[Kind.VectorStore].resource

        self.llm = self.dependencies.get(Kind.LLM) or self.dependencies.get(
            Kind.LLMChat
        )

        self.tool_function = self.vendor_cls.from_chain_type(
            **self.options,  # type: ignore
            llm=self.llm.resource,  # type: ignore
            retriever=self.vectorestore.as_retriever(),
        )

        self.resource = ToolWarperLC(
            name=self.name,
            description=self.description,
            func=self.tool_function,
        )


export = {
    "VectorStoreQATool": VectorStoreQAToolResource,
}
