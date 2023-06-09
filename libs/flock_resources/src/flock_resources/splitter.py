"""Interface for LLM models."""

from typing import Dict, List, Optional

from langchain.text_splitter import (
    CharacterTextSplitter,
    PythonCodeTextSplitter,
    TextSplitter,
)

from flock_resources.base import Resource, ToolResource
from flock_schemas.splitter import SplitterSchema


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


export = {
    "Splitter": SplitterResource,
}
