from enum import Enum
from flock_schemas.base import BaseFlockSchema as BaseFlockSchema, BaseOptions as BaseOptions
from flock_schemas.dependencies import LLMDependency as LLMDependency, StoreDependency as StoreDependency
from typing import Literal, Optional

class VectorStoreQAToolVendor(str, Enum):
    RetrievalQAWithSourcesChain: str

class VectorStoreQAToolSpec(BaseOptions):
    vendor: VectorStoreQAToolVendor
    options: Optional[dict]
    dependencies: tuple[StoreDependency, LLMDependency]

class VectorStoreQAToolSchema(BaseFlockSchema):
    kind: Literal['VectorStoreQATool']
    spec: VectorStoreQAToolSpec
