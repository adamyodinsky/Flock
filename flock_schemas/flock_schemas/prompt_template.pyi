from enum import Enum
from flock_schemas.base import BaseFlockSchema as BaseFlockSchema, BaseOptions as BaseOptions
from typing import Literal

class PromptTemplateVendor(str, Enum):
    PromptTemplate: str

class PromptTemplateSpec(BaseOptions):
    vendor: PromptTemplateVendor

class PromptTemplateSchema(BaseFlockSchema):
    kind: Literal['PromptTemplate']
    spec: PromptTemplateSpec
