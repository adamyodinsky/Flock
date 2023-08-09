"""BabyAGI agent plugin. example for custom resource plugin."""
from typing import Dict, List, Optional

import faiss
from flock_schemas.base import Kind
from flock_schemas.custom import CustomSchema
from langchain.docstore import InMemoryDocstore
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import FAISS
from langchain_experimental.autonomous_agents import BabyAGI

from flock_resources.base import CustomResource, Resource, ToolResource


class BabyAGIAgent(CustomResource):
    """Class for self ask search agent."""

    def __init__(
        self,
        manifest: CustomSchema,
        dependencies: Optional[Dict[str, Resource]],
        tools: Optional[List[ToolResource]],
        dry_run: bool = False,
    ):
        super().__init__(manifest, dependencies, tools)

        # Define your embedding model and initialize the vectorstore as empty
        embedding: Embeddings = self.dependencies[Kind.Embedding].resource
        embedding_size = 1536
        index = faiss.IndexFlatL2(embedding_size)
        vectorstore = FAISS(embedding.embed_query, index, InMemoryDocstore({}), {})

        llm = self.dependencies.get(Kind.LLMChat)
        self.llm = llm.resource  # type: ignore

        self.resource = BabyAGI.from_llm(
            vectorstore=vectorstore,
            llm=self.llm,
            task_execution_chain=self.dependencies[Kind.Agent].resource,
            **self.options,  # type: ignore
        )
        self.run = self.resource


export = {"BabyAGI": BabyAGIAgent}
