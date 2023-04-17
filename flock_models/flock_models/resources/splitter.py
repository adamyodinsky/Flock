"""Interface for LLM models."""

from typing import Any
from flock_models.resources.base import Resource
from langchain.text_splitter import TextSplitter
from langchain.text_splitter import CharacterTextSplitter, PythonCodeTextSplitter


class SplitterResource(Resource):
    """Class for Splitter resources."""

    VENDORS = {
        "CharacterTextSplitter": CharacterTextSplitter,
        "PythonCodeTextSplitter": PythonCodeTextSplitter,
    }

    def __init__(
        self,
        vendor: str,
        options: dict[str, Any],
        dependencies: dict[str, Any] = None,
    ):
        splitter_cls: TextSplitter = self.VENDORS[vendor]
        self.resource = splitter_cls(**options)
