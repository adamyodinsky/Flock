"""Reusable Dependency Schemas"""

from pydantic import Field
from flock_models.schemes.base import BaseDependency, Kind

class LLMDependency(BaseDependency):
    kind: str = Field(Kind.LLM, const=True)


class StoreDependency(BaseDependency):
    kind: str = Field(Kind.VectorStore, const=True)


class EmbeddingDependency(BaseDependency):
    kind: str = Field(Kind.Embedding.value, const=True)
