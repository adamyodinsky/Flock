from enum import Enum
from typing import Optional

from pydantic import Field

from flock_models.schemes.base import BaseModelConfig, FlockBaseSchema, Kind


class SplitterVendor(str, Enum):
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
        Kind.Splitter, const=True, description="The kind of the object"
    )
    spec: SplitterSpec
