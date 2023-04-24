from _typeshed import Incomplete
from flock_schemas.base import BaseDependency as BaseDependency, BaseFlockSchema as BaseFlockSchema, BaseOptions as BaseOptions
from flock_schemas.dependencies import ToolDependency as ToolDependency
from typing import List, Optional

class CustomSpec(BaseOptions):
    vendor: Optional[str]
    dependencies: Optional[List[BaseDependency]]
    tools: Optional[List[ToolDependency]]
    class Config:
        extra: Incomplete

class CustomSchema(BaseFlockSchema):
    kind: str
    spec: CustomSpec
