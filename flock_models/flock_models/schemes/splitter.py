from enum import Enum
from typing import Optional

from pydantic import Field

from flock_models.schemes.base import FlockBaseSchema, Kind, Options


class SplitterVendor(str, Enum):
    """Enum for splitter vendors."""

    CharacterTextSplitter = "CharacterTextSplitter"
    PythonCodeTextSplitter = "PythonCodeTextSplitter"


class SplitterSpec(Options):
    vendor: SplitterVendor = Field(
        ..., description="The class of the splitter, e.g. CharacterTextSplitter, etc."
    )


class SplitterSchema(FlockBaseSchema):
    kind: str = Field(
        Kind.Splitter, const=True, description="The kind of the object"
    )
    spec: SplitterSpec
