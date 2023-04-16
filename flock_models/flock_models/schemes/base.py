from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field, Extra, validator
from uuid import UUID, uuid4

class BaseModelConfig(BaseModel):
    class Config:
        validate_all = True
        extra = Extra.forbid

class Annotations(BaseModelConfig):
    annotations: Optional[dict] = Field(default=None, description="Annotations are useful for storing additional information")

class Labels(BaseModelConfig):
    labels: Optional[dict] = Field(default=None, description="Labels are useful for filtering and finding objects")

class MetaData(Labels, Annotations):
    name: str = Field(..., description="Name of the object", max_length=63)
    description: str = Field(..., description="Description", max_length=255)

class FlockBaseSchema(BaseModelConfig):
    apiVersion: Literal["flock/v1"] = Field(..., description="API version")
    metadata: MetaData
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp"
    )
    # id: UUID = Field(default_factory=uuid4, description="UUID for the object")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp")
    