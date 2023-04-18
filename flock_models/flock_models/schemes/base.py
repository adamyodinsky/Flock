from datetime import datetime
from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, Extra, Field

# from uuid import UUID, uuid4


class Kind(str, Enum):
    """Enum for all kinds of resources."""

    Embedding = "Embedding"
    VectorStore = "VectorStore"
    VectorStoreQATool = "VectorStoreQATool"
    LLM = "LLM"
    SearchTool = "SearchTool"
    Splitter = "Splitter"
    Agent = "Agent"


class BaseModelConfig(BaseModel):
    class Config:
        validate_all = True
        extra = Extra.forbid


class Annotations(BaseModelConfig):
    annotations: Optional[dict[str, str]] = Field(
        default=None,
        description="Annotations are useful for storing additional information",
    )


class Labels(BaseModelConfig):
    labels: Optional[dict[str, str]] = Field(
        default=None, description="Labels are useful for filtering and finding objects"
    )


class Dependency(Labels):
    name: str = Field(..., description="Name of the dependency")
    kind: Kind = Field(..., description="Kind of the dependency")
    namespace: Optional[str] = Field(
        "default", description="The namespace of the object", max_length=63
    )


class MetaData(Labels, Annotations):
    name: str = Field(..., description="Name of the object", max_length=63)
    description: str = Field(..., description="Description", max_length=255)
    Annotations
    Labels


class Namespace(BaseModelConfig):
    namespace: Optional[str] = Field(
        "default", description="The namespace of the object", max_length=63
    )


class FlockBaseSchema(Namespace):
    apiVersion: Literal["flock/v1"] = Field(..., description="API version")
    metadata: MetaData
    created_at: Optional[datetime] = Field(
        default=None, description="Creation timestamp"
    )
    # id: UUID = Field(default_factory=uuid4, description="UUID for the object")
    updated_at: Optional[datetime] = Field(
        default=None, description="Last update timestamp"
    )
