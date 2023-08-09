"""Base schema for all Flock objects."""


from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Mapping, Optional
from uuid import UUID, uuid4

from bson import ObjectId
from pydantic import BaseModel, Extra, Field


def str_uuid():
    return str(uuid4())


class PyObjectId(ObjectId):
    """Custom Type for reading MongoDB IDs"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid object_id")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


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
    EmbeddingsLoader = "EmbeddingsLoader"
    WebScraper = "WebScraper"
    CSVTool = "CSVTool"
    BrowserTool = "BrowserTool"
    Custom = "Custom"


class Category(str, Enum):
    """Enum for all categories of resources."""

    OTHER = "other"
    TOOL = "tool"
    SCRAPER = "scraper"
    MODEL = "model"
    AGENT = "agent"
    DEPLOYMENT = "deployment"
    JOB = "job"
    CRON_JOB = "cronjob"
    STATEFULSET = "statefulset"


class BaseModelConfig(BaseModel):
    """Base model config."""

    class Config:
        """Base model config."""

        validate_all = True
        extra = Extra.forbid


class BaseAnnotations(BaseModelConfig):
    """Base annotations schema."""

    annotations: Dict[str, str] = Field(
        default={},
        description="Annotations are useful for storing additional information",
    )


class BaseLabels(BaseModelConfig):
    """Base labels schema."""

    labels: Optional[Dict[str, str]] = Field(
        default={}, description="Labels are useful for filtering and finding objects"
    )


class BaseDependency(BaseLabels):
    """Base dependency schema."""

    name: str = Field(..., description="Name of the dependency")
    kind: Kind = Field(..., description="Kind of the dependency")
    namespace: str = Field(
        "default", description="The namespace of the object", max_length=63
    )
    options: Dict[str, Any] = Field({}, description="Resource options")


class BaseToolDependency(BaseDependency):
    """Base tool dependency schema."""

    description: Optional[str] = Field(description="Tool description")


class BaseMetaData(BaseLabels, BaseAnnotations):
    """Base metadata schema."""

    name: str = Field(..., description="Name of the object", max_length=63)
    description: str = Field(..., description="Description", max_length=255)


class BaseOptions(BaseModelConfig):
    """Base options schema."""

    options: Dict[str, Any] = Field({}, description="Resource options")


class BaseSpec(BaseOptions):
    """Base spec schema."""

    vendor: str = Field(default="", description="The resource class")
    tools: List[BaseToolDependency] = Field([], description="Tools for the object")
    dependencies: Any = Field([], description="Dependencies for the object")


class BaseResourceSchema(BaseModelConfig):
    """Base schema for all Flock objects."""

    id: str = Field(default_factory=str_uuid, description="String UUID of the object")
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
        "BaseResource": BaseResourceSchema,
    },
}
