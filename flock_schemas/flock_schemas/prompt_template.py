from enum import Enum
from typing import Literal

from pydantic import Field

from flock_schemas.base import BaseFlockSchema, BaseOptions


class PromptTemplateVendor(str, Enum):
    """Enum for prompt template vendors."""

    PromptTemplate = "PromptTemplate"


class PromptTemplateSpec(BaseOptions):
    vendor: PromptTemplateVendor = Field(..., description="PromptTemplate vendor")


class PromptTemplateSchema(BaseFlockSchema):
    kind: Literal["PromptTemplate"] = Field(..., description="The kind of the object")
    spec: PromptTemplateSpec
