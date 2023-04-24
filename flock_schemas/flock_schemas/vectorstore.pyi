from enum import Enum
from flock_schemas.base import BaseFlockSchema as BaseFlockSchema, BaseOptions as BaseOptions
from flock_schemas.dependencies import EmbeddingDependency as EmbeddingDependency
from typing import Literal

class VectorStoreVendor(str, Enum):
    Chroma: str

class VectorStoreSpec(BaseOptions):
    vendor: str
    dependencies: tuple[EmbeddingDependency]

class VectorStoreSchema(BaseFlockSchema):
    kind: Literal['VectorStore']
    spec: VectorStoreSpec
