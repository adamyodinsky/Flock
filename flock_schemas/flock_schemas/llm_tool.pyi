from enum import Enum
from flock_schemas.base import BaseFlockSchema as BaseFlockSchema, BaseOptions as BaseOptions
from flock_schemas.dependencies import LLMDependency as LLMDependency, PromptTemplateDependency as PromptTemplateDependency
from typing import Literal, Optional

class LLMToolVendor(str, Enum):
    LLMChain: str

class LLMToolSpec(BaseOptions):
    vendor: LLMToolVendor
    options: Optional[dict]
    dependencies: tuple[PromptTemplateDependency, LLMDependency]

class LLMToolSchema(BaseFlockSchema):
    kind: Literal['LLMTool']
    spec: LLMToolSpec
