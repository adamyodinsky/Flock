"""Splitter schema."""

from enum import Enum
from typing import Literal

from pydantic import Field

from flock_schemas.base import BaseFlockSchema, BaseOptions, Category


class SplitterVendor(str, Enum):
    """Enum for splitter vendors."""

    CharacterTextSplitter = "CharacterTextSplitter"
    PythonCodeTextSplitter = "PythonCodeTextSplitter"


class SplitterSpec(BaseOptions):
    """Splitter spec."""

    vendor: SplitterVendor = Field(
        ..., description="The class of the splitter, e.g. CharacterTextSplitter, etc."
    )


class SplitterSchema(BaseFlockSchema):
    """Splitter schema."""

    kind: Literal["Splitter"] = Field(..., description="The kind of the object")
    category: Category = Field(
        default=Category.OTHER, description="The resource category"
    )
    spec: SplitterSpec


export = {
    "sub": {
        "SplitterSpec": SplitterSpec,
    },
    "main": {
        "SplitterSchema": SplitterSchema,
    },
}
