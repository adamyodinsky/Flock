from langchain.text_splitter import TextSplitter

"""Interface for LLM models."""

from typing import Any
from flock_models.schemes.llm import LLMSchema
from flock_models.entities.base import Entity
from langchain.text_splitter import TextSplitter


class SplitterEntity(Entity):
    """Base class for embedding entities."""

    def __init__(self, manifest: dict[str, Any], splitter: TextSplitter):
        super().__init__(manifest, LLMSchema)
        self.resource = splitter(**self.manifest.spec.options.dict())


# ---
# apiVersion: flock/v1
# kind: LLM
# # uuid: b70bb61d-6710-48bd-85b0-f32c91f1eed1
# metadata:
#   name: my-openai-llm
#   description: openai language model
#   labels:
#     app: my_app
# spec:
#   vendor: openai
#   options:
#       model: gpt3.5-turbo
#       token_limit: 1000
#       temperature: 0.5
