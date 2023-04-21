"""Interface for LLM models."""

from typing import Any

from flock_schemas import SplitterSchema
from flock_schemas.base import BaseFlockSchema
from langchain.text_splitter import (
    CharacterTextSplitter,
    PythonCodeTextSplitter,
    TextSplitter,
)

from flock_models.resources.base import Resource


class SplitterResource(Resource):
    """Class for Splitter resources."""

    VENDORS = {
        "CharacterTextSplitter": CharacterTextSplitter,
        "PythonCodeTextSplitter": PythonCodeTextSplitter,
    }

    def __init__(
        self,
        manifest: SplitterSchema,
        dependencies: dict[str, Any] = None,
        tools: list[Any] = [],
    ):
        super().__init__(manifest)
        self.vendor_cls: TextSplitter = self.VENDORS[self.vendor]
        self.resource = self.vendor_cls(**self.options)
