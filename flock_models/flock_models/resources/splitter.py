"""Interface for LLM models."""

from typing import Any

from langchain.text_splitter import (
    CharacterTextSplitter,
    PythonCodeTextSplitter,
    TextSplitter,
)

from flock_models.resources.base import Resource
from flock_schemas.base import BaseFlockSchema


class SplitterResource(Resource):
    """Class for Splitter resources."""

    VENDORS = {
        "CharacterTextSplitter": CharacterTextSplitter,
        "PythonCodeTextSplitter": PythonCodeTextSplitter,
    }

    def __init__(
        self,
        manifest: BaseFlockSchema,
        dependencies: dict[str, Any] = None,
    ):
        super().__init__(manifest)
        self.vendor_cls: TextSplitter = self.VENDORS[self.vendor]
        self.resource = self.vendor_cls(**self.options)
