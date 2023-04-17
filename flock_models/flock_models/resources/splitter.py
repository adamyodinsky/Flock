"""Interface for LLM models."""

from typing import Any
from flock_models.schemes.splitter import SplitterSchema
from flock_models.resources.base import Resource
from langchain.text_splitter import TextSplitter


class SplitterResource(Resource):
    """Class for Splitter resources."""

    def __init__(self, manifest: dict[str, Any], splitter: TextSplitter):
        self.manifest = SplitterSchema(**manifest)
        self.resource: TextSplitter = splitter(**self.manifest.spec.options.dict())


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
