from enum import Enum
from flock_schemas.base import BaseFlockSchema as BaseFlockSchema, BaseOptions as BaseOptions
from typing import Literal

class SplitterVendor(str, Enum):
    CharacterTextSplitter: str
    PythonCodeTextSplitter: str

class SplitterSpec(BaseOptions):
    vendor: SplitterVendor

class SplitterSchema(BaseFlockSchema):
    kind: Literal['Splitter']
    spec: SplitterSpec
