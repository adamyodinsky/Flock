"""Reusable Dependency Schemas"""

from pydantic import Field

from flock_schemas.base import BaseDependency, Kind


class LLMDependency(BaseDependency):
    """LLM dependency schema."""

    kind: str = Field(Kind.LLM, const=True)


class LLMChatDependency(BaseDependency):
    """LLMChat dependency schema."""

    kind: str = Field(Kind.LLMChat, const=True)


class VectorStoreDependency(BaseDependency):
    """Store dependency schema."""

    kind: str = Field(Kind.VectorStore, const=True)


class EmbeddingDependency(BaseDependency):
    """Embedding dependency schema."""

    kind: str = Field(Kind.Embedding.value, const=True)


class SplitterDependency(BaseDependency):
    """Embedding dependency schema."""

    kind: str = Field(Kind.Splitter.value, const=True)


class PromptTemplateDependency(BaseDependency):
    """Prompt template dependency schema."""

    kind: str = Field(Kind.PromptTemplate.value, const=True)


export = {
    "sub": {
        "LLMDependency": LLMDependency,
        "VectorStoreDependency": VectorStoreDependency,
        "EmbeddingDependency": EmbeddingDependency,
        "PromptTemplateDependency": PromptTemplateDependency,
    },
    "main": {},
}
