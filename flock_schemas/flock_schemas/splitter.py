from enum import Enum
from typing import Literal, Optional

from pydantic import Field

from flock_schemas.base import BaseFlockSchema, BaseOptions, Kind


class SplitterVendor(str, Enum):
    """Enum for splitter vendors."""

    CharacterTextSplitter = "CharacterTextSplitter"
    PythonCodeTextSplitter = "PythonCodeTextSplitter"


class SplitterSpec(BaseOptions):
    vendor: SplitterVendor = Field(
        ..., description="The class of the splitter, e.g. CharacterTextSplitter, etc."
    )


class SplitterSchema(BaseFlockSchema):
    kind: Literal["Splitter"] = Field(..., description="The kind of the object")
    spec: SplitterSpec
