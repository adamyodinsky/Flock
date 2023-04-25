from datetime import datetime
from enum import Enum
from typing import Any, List, Literal, Mapping, Optional

from pydantic import BaseModel, Extra, Field

# from uuid import UUID, uuid4


class Kind(str, Enum):
    """Enum for all kinds of resources."""

    Embedding = "Embedding"
    VectorStore = "VectorStore"
    VectorStoreQATool = "VectorStoreQATool"
    LLM = "LLM"
    LoadTool = "LoadTool"
    Splitter = "Splitter"
    Agent = "Agent"
    PromptTemplate = "PromptTemplate"
    LLMTool = "LLMTool"
    Custom = "Custom"


class BaseModelConfig(BaseModel):
    class Config:
        validate_all = True
        extra = Extra.forbid


class BaseAnnotations(BaseModelConfig):
    annotations: Optional[dict[str, str]] = Field(
        default=None,
        description="Annotations are useful for storing additional information",
    )


class BaseLabels(BaseModelConfig):
    labels: Optional[dict[str, str]] = Field(
        default=None, description="Labels are useful for filtering and finding objects"
    )


class BaseDependency(BaseLabels):
    name: str = Field(..., description="Name of the dependency")
    kind: Kind = Field(..., description="Kind of the dependency")
    namespace: Optional[str] = Field(
        "default", description="The namespace of the object", max_length=63
    )


class ToolDependency(BaseDependency):
    description: Optional[str] = Field(description="Tool description")


class BaseMetaData(BaseLabels, BaseAnnotations):
    name: str = Field(..., description="Name of the object", max_length=63)
    description: str = Field(..., description="Description", max_length=255)


class BaseNamespace(BaseModelConfig):
    namespace: Optional[str] = Field(
        ..., description="The namespace of the object", max_length=63
    )


class BaseOptions(BaseModelConfig):
    options: Optional[Mapping[str, Any]] = Field({}, description="Resource options")


class BaseSpec(BaseOptions):
    vendor: str = Field(description="The resource class")
    dependencies: Optional[List[BaseDependency]] = Field(
        [], description="Dependencies for the object"
    )
    tools: Optional[List[ToolDependency]] = Field(
        [], description="Tools for the object"
    )


class BaseFlockSchema(BaseNamespace):
    apiVersion: Literal["flock/v1"] = Field(..., description="API version")
    kind: Kind = Field(..., description="Kind of the object")
    metadata: BaseMetaData
    created_at: Optional[datetime] = Field(
        default=None, description="Creation timestamp"
    )
    # id: UUID = Field(default_factory=uuid4, description="UUID for the object")
    updated_at: Optional[datetime] = Field(
        default=None, description="Last update timestamp"
    )
    spec: BaseSpec
