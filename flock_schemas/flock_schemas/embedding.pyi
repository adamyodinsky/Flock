from enum import Enum
from flock_schemas.base import BaseFlockSchema as BaseFlockSchema, BaseOptions as BaseOptions
from typing import Literal, Optional

class EmbeddingVendor(str, Enum):
    OpenAIEmbeddings: str

class EmbeddingSpec(BaseOptions):
    vendor: EmbeddingVendor
    options: Optional[dict]

class EmbeddingSchema(BaseFlockSchema):
    kind: Literal['Embedding']
    spec: EmbeddingSpec
