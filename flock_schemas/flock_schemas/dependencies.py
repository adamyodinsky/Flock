"""Reusable Dependency Schemas"""

from typing import Optional

from pydantic import Field

from flock_schemas.base import BaseDependency, Kind


class LLMDependency(BaseDependency):
    kind: str = Field(Kind.LLM, const=True)


class StoreDependency(BaseDependency):
    kind: str = Field(Kind.VectorStore, const=True)


class EmbeddingDependency(BaseDependency):
    kind: str = Field(Kind.Embedding.value, const=True)


class PromptTemplateDependency(BaseDependency):
    kind: str = Field(Kind.PromptTemplate.value, const=True)


class ToolDependency(BaseDependency):
    description: Optional[str] = Field(description="Tool description")
