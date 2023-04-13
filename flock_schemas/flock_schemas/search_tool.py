from pydantic import BaseModel, Field
from flock_schemas.base import FlockBaseModel, Labels, BaseModelConfig


class LLM(Labels):
    name: str = Field(..., description="Name of the Language Model")

class Search(Labels):
    name: str = Field(..., description="Name of the search tool")
    
class SearchToolSpec(BaseModelConfig):
    llm: LLM
    search: Search

class SearchTool(FlockBaseModel):
    kind: str = Field("SearchTool", const=True)
    spec: SearchToolSpec
