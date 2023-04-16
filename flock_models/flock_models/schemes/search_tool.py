from pydantic import BaseModel, Field
from flock_models.schemes.base import FlockBaseSchema, Labels, BaseModelConfig


class LLM(Labels):
    name: str = Field(..., description="Name of the Language Model")

class Search(Labels):
    name: str = Field(..., description="Name of the search tool")
    
class SearchToolSpec(BaseModelConfig):
    llm: LLM
    search: Search

class SearchToolSchema(FlockBaseSchema):
    kind: str = Field("SearchTool", const=True)
    spec: SearchToolSpec
