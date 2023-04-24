from flock_schemas.base import BaseDependency as BaseDependency, Kind as Kind
from typing import Optional

class LLMDependency(BaseDependency):
    kind: str

class StoreDependency(BaseDependency):
    kind: str

class EmbeddingDependency(BaseDependency):
    kind: str

class PromptTemplateDependency(BaseDependency):
    kind: str

class ToolDependency(BaseDependency):
    description: Optional[str]
