from typing import Optional
from pydantic import Field
from flock_models.schemes.base import FlockBaseSchema, BaseModelConfig, Kind

from enum import Enum


class SplitterVendor(Enum):
    """Enum for splitter vendors."""

    CharacterTextSplitter = "CharacterTextSplitter"
    PythonCodeTextSplitter = "PythonCodeTextSplitter"


class SplitterSpec(BaseModelConfig):
    options: Optional[dict] = Field(description="Splitter options")
    vendor: SplitterVendor = Field(
        ..., description="The class of the splitter, e.g. CharacterTextSplitter, etc."
    )


class SplitterSchema(FlockBaseSchema):
    kind: str = Field(
        Kind.splitter.value, const=True, description="The kind of the object"
    )
    spec: SplitterSpec
