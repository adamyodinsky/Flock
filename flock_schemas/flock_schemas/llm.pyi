from enum import Enum
from flock_schemas.base import BaseFlockSchema as BaseFlockSchema, BaseOptions as BaseOptions
from typing import Literal

class LLMVendor(str, Enum):
    ChatOpenAI: str

class LLMSpec(BaseOptions):
    vendor: LLMVendor

class LLMSchema(BaseFlockSchema):
    kind: Literal['LLM']
    spec: LLMSpec
