"""Resource for vectorstore."""

from typing import Any
from flock_schemas.base import Kind, BaseFlockSchema
from langchain.agents import Tool as ToolWarperLC
from langchain.experimental import BabyAGI
from langchain.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
import faiss
from langchain.docstore import InMemoryDocstore


from flock_models.resources.base import Resource


class BabyAGIResource(Resource):
    """Class for self ask search agent."""
    
    def __init__(
        self,
        manifest: BaseFlockSchema,
        dependencies: dict[str, Any],
        tools: list[ToolWarperLC],
    ):
        super().__init__(manifest, dependencies, tools)

        # Define your embedding model
        self.embedding: Embeddings = self.dependencies[Kind.Embedding]

        # Initialize the vectorstore as empty
        embedding_size = 1536
        index = faiss.IndexFlatL2(embedding_size)
        vectorstore = FAISS(self.embedding.embed_query, index, InMemoryDocstore({}), {})

        self.resource = BabyAGI.from_llm(
          vectorstore=vectorstore,
          llm=self.dependencies[Kind.LLM],
          task_execution_chain=self.dependencies[Kind.Agent],
          **self.options,
        )