"""Interface for LLM models."""

from typing import Any

from langchain.text_splitter import (
    CharacterTextSplitter,
    PythonCodeTextSplitter,
    TextSplitter,
)

from flock_models.resources.base import Resource
from flock_models.schemes.base import FlockBaseSchema


class SplitterResource(Resource):
    """Class for Splitter resources."""

    VENDORS = {
        "CharacterTextSplitter": CharacterTextSplitter,
        "PythonCodeTextSplitter": PythonCodeTextSplitter,
    }

    def __init__(
        self,
        manifest: FlockBaseSchema,
    ):
        super().__init__(manifest)
        splitter_cls: TextSplitter = self.VENDORS[self.vendor]
        self.resource = splitter_cls(**self.options)
