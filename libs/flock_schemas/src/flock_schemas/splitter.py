"""Splitter schema."""

from enum import Enum
from typing import Literal

from flock_schemas.base import BaseSpec, BaseResourceSchema, Category
from pydantic import Field


class SplitterVendor(str, Enum):
    """Enum for splitter vendors."""

    CharacterTextSplitter = "CharacterTextSplitter"
    PythonCodeTextSplitter = "PythonCodeTextSplitter"


class SplitterSpec(BaseSpec):
    """Splitter spec."""

    vendor: SplitterVendor = Field(
        ..., description="The class of the splitter, e.g. CharacterTextSplitter, etc."
    )


class SplitterSchema(BaseResourceSchema):
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
        "Splitter": SplitterSchema,
    },
}
