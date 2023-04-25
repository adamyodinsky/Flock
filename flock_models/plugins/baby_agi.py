"""BabyAGI agent plugin. example for custom resource plugin."""
from typing import Optional

import faiss
from flock_schemas import CustomSchema, Kind
from langchain.docstore import InMemoryDocstore
from langchain.embeddings.base import Embeddings
from langchain.experimental import BabyAGI
from langchain.vectorstores import FAISS

from flock_models.resources.base import CustomResource, Resource, ToolResource


class BabyAGIAgent(CustomResource):
    """Class for self ask search agent."""

    def __init__(
        self,
        manifest: CustomSchema,
        dependencies: Optional[dict[str, Resource]],
        tools: Optional[list[ToolResource]],
    ):
        super().__init__(manifest, dependencies, tools)

        # Define your embedding model and initialize the vectorstore as empty
        embedding: Embeddings = self.dependencies[Kind.Embedding].resource
        embedding_size = 1536
        index = faiss.IndexFlatL2(embedding_size)
        vectorstore = FAISS(embedding.embed_query, index, InMemoryDocstore({}), {})

        self.resource = BabyAGI.from_llm(
            vectorstore=vectorstore,
            llm=self.dependencies[Kind.LLM].resource,
            task_execution_chain=self.dependencies[Kind.Agent].resource,
            **self.options,
        )
        self.run = self.resource


export = {"BabyAGI": BabyAGIAgent}
