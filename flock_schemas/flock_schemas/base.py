"""Base schema for all Flock objects."""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Mapping, Optional

from pydantic import BaseModel, Extra, Field


class Kind(str, Enum):
    """Enum for all kinds of resources."""

    Embedding = "Embedding"
    VectorStore = "VectorStore"
    VectorStoreQATool = "VectorStoreQATool"
    LLM = "LLM"
    LLMChat = "LLMChat"
    LoadTool = "LoadTool"
    Splitter = "Splitter"
    Agent = "Agent"
    PromptTemplate = "PromptTemplate"
    LLMTool = "LLMTool"
    Custom = "Custom"


class Category(str, Enum):
    """Enum for all categories of resources."""

    OTHER = "other"
    TOOL = "tool"
    SCRAPER = "scraper"
    MODEL = "model"
    AGENT = "agent"
    DEPLOYMENT = "deployment"
    STATEFULSET = "statefulset"


class BaseModelConfig(BaseModel):
    """Base model config."""

    class Config:
        """Base model config."""

        validate_all = True
        extra = Extra.forbid


class BaseAnnotations(BaseModelConfig):
    """Base annotations schema."""

    annotations: Optional[Dict[str, str]] = Field(
        default=None,
        description="Annotations are useful for storing additional information",
    )


class BaseLabels(BaseModelConfig):
    """Base labels schema."""

    labels: Optional[Dict[str, str]] = Field(
        default=None, description="Labels are useful for filtering and finding objects"
    )


class BaseDependency(BaseLabels):
    """Base dependency schema."""

    name: str = Field(..., description="Name of the dependency")
    kind: Kind = Field(..., description="Kind of the dependency")
    namespace: Optional[str] = Field(
        "default", description="The namespace of the object", max_length=63
    )
    options: Optional[Dict[str, Any]] = Field({}, description="Resource options")


class BaseToolDependency(BaseDependency):
    """Base tool dependency schema."""

    description: Optional[str] = Field(description="Tool description")


class BaseMetaData(BaseLabels, BaseAnnotations):
    """Base metadata schema."""

    name: str = Field(..., description="Name of the object", max_length=63)
    description: str = Field(..., description="Description", max_length=255)


class BaseOptions(BaseModelConfig):
    """Base options schema."""

    options: Optional[Dict[str, Any]] = Field({}, description="Resource options")


class BaseSpec(BaseOptions):
    """Base spec schema."""

    vendor: str = Field(description="The resource class")
    dependencies: Optional[List[BaseDependency]] = Field(
        [], description="Dependencies for the object"
    )
    tools: Optional[List[BaseToolDependency]] = Field(
        [], description="Tools for the object"
    )


class BaseFlockSchema(BaseModelConfig):
    """Base schema for all Flock objects."""

    # id: Optional[PyObjectId] = Field(None, alias="_id", description="Unique identifier")
    apiVersion: Literal["flock/v1"] = Field(..., description="API version")
    kind: Kind = Field(..., description="Kind of the object")
    category: Optional[Category] = Field(
        default=Category.OTHER, description="The resource category"
    )
    namespace: str = Field(
        ..., description="The namespace of the object", max_length=63
    )
    metadata: BaseMetaData
    created_at: Optional[datetime] = Field(
        default=None, description="Creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="Last update timestamp"
    )
    spec: BaseSpec

    class Config:
        """Base model config."""

        validate_all = True
        extra = Extra.forbid
        collection = "resources"
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


export = {
    "sub": {
        "BaseModelConfig": BaseModelConfig,
        "BaseAnnotations": BaseAnnotations,
        "BaseLabels": BaseLabels,
        "BaseDependency": BaseDependency,
        "BaseToolDependency": BaseToolDependency,
        "BaseMetaData": BaseMetaData,
        "BaseOptions": BaseOptions,
        "BaseSpec": BaseSpec,
    },
    "main": {
        "BaseFlockSchema": BaseFlockSchema,
    },
}
