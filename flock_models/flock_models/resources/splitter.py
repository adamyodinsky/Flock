"""Interface for LLM models."""

from typing import Dict, List, Optional

from flock_schemas import SplitterSchema
from langchain.text_splitter import (
    CharacterTextSplitter,
    PythonCodeTextSplitter,
    TextSplitter,
)

from flock_models.resources.base import Resource, ToolResource


class SplitterResource(Resource):
    """Class for Splitter resources."""

    VENDORS = {
        "CharacterTextSplitter": CharacterTextSplitter,
        "PythonCodeTextSplitter": PythonCodeTextSplitter,
    }

    def __init__(
        self,
        manifest: SplitterSchema,
        dependencies: Optional[Dict[str, Resource]],
        tools: Optional[List[ToolResource]] = None,
    ):
        super().__init__(manifest)
        self.vendor_cls: TextSplitter = self.VENDORS[self.vendor]
        self.resource: TextSplitter = self.vendor_cls(**self.options)  # type: ignore
