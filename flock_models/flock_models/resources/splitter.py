"""Interface for LLM models."""

from typing import Any
from flock_models.schemes.splitter import SplitterSchema
from flock_models.resources.base import Resource
from langchain.text_splitter import TextSplitter
from langchain.text_splitter import (CharacterTextSplitter,
                                     PythonCodeTextSplitter)


class SplitterResource(Resource):
    """Class for Splitter resources."""

    def __init__(self, manifest: dict[str, Any], splitter: TextSplitter):
        self.manifest = SplitterSchema(**manifest)
        self.resource: TextSplitter = splitter(**self.manifest.spec.options.dict())


# ---
# apiVersion: flock/v1
# kind: Splitter
# metadata:
#   name: my-splitter
#   description: text-splitter
#   labels:
#     app: my_app
# spec:
#   type: python_splitter
#   options:
#     chunk_size: 30
#     chunk_overlap: 0
