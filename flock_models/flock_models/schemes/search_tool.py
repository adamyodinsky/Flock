from pydantic import Field
from flock_models.schemes.base import FlockBaseSchema, Labels, BaseModelConfig, Kind


class LLM(Labels):
    name: str = Field(..., description="Name of the Language Model")


class Search(Labels):
    name: str = Field(..., description="Name of the search tool")


class SearchToolSpec(BaseModelConfig):
    llm: LLM
    search: Search


class SearchToolSchema(FlockBaseSchema):
    kind: str = Field(Kind.search_tool.value, const=True)
    spec: SearchToolSpec
