from pydantic import Field
from flock_schemas.base import FlockBaseModel, BaseModelConfig

class LLMSpec(BaseModelConfig):
    vendor: str = Field(..., description="Vendor of the LLM")
    model: str = Field(..., description="Name of the LLM model")
    token_limit: int = Field(..., description="Token limit for the LLM")
    
class LLM(FlockBaseModel):
    kind: str = Field("LLM", const=True, description="The kind of the object")
    spec: LLMSpec

