from pydantic import BaseModel, Field
from base import FlockBaseModel, Labels, BaseModelConfig


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


# kind: SearchTool
# metadata:
#   name: my-google-search
#   description: api for interacting with google search
#   labels:
#     app: my_app
# spec:
#   llm:
#     name: my-llm
#     labels:
#       app: my_app
#   search:
#     name: serpapi
#     labels:
#       app: my_app
