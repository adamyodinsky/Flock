from pydantic import Field
from flock_models.schemes.base import (
    FlockBaseSchema,
    Labels,
    BaseModelConfig,
    Kind,
    Dependency,
)


class Search(Labels):
    name: str = Field(..., description="Name of the search tool")


class LLM(Dependency):
    kind: str = Field(Kind.llm.value, const=True)


class Dependencies(Labels):
    LLM


class SearchToolSpec(BaseModelConfig):
    dependencies: Dependencies = Field(..., description="Dependencies for the tool")
    search: Search


class SearchToolSchema(FlockBaseSchema):
    kind: str = Field(Kind.search_tool.value, const=True)
    spec: SearchToolSpec
