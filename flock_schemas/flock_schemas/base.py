"""Base schema for all Flock objects."""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Mapping, Optional

from odmantic import Index
from odmantic.bson import BaseBSONModel, ObjectId
from pydantic import Extra, Field


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


class PyObjectId(ObjectId):
    """Pydantic model for ObjectId."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class BaseModelConfig(BaseBSONModel):
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


class BaseToolDependency(BaseDependency):
    """Base tool dependency schema."""

    description: Optional[str] = Field(description="Tool description")


class BaseMetaData(BaseLabels, BaseAnnotations):
    """Base metadata schema."""

    name: str = Field(..., description="Name of the object", max_length=63)
    description: str = Field(..., description="Description", max_length=255)


class BaseNamespace(BaseModelConfig):
    """Base namespace schema."""

    namespace: Optional[str] = Field(
        ..., description="The namespace of the object", max_length=63
    )


class BaseOptions(BaseModelConfig):
    """Base options schema."""

    options: Optional[Mapping[str, Any]] = Field({}, description="Resource options")


class BaseSpec(BaseOptions):
    """Base spec schema."""

    vendor: str = Field(description="The resource class")
    dependencies: Optional[List[BaseDependency]] = Field(
        [], description="Dependencies for the object"
    )
    tools: Optional[List[BaseToolDependency]] = Field(
        [], description="Tools for the object"
    )


class BaseFlockSchema(BaseNamespace):
    """Base schema for all Flock objects."""

    id: Optional[PyObjectId] = Field(None, alias="_id", description="Unique identifier")
    apiVersion: Literal["flock/v1"] = Field(..., description="API version")
    kind: Kind = Field(..., description="Kind of the object")
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

        @staticmethod
        def indexes():
            """Return indexes."""

            yield Index(
                BaseFlockSchema.namespace,
                BaseFlockSchema.kind,
                BaseFlockSchema.metadata.name,
                unique=True,
            )


export = {
    "sub": {
        "BaseModelConfig": BaseModelConfig,
        "BaseAnnotations": BaseAnnotations,
        "BaseLabels": BaseLabels,
        "BaseDependency": BaseDependency,
        "BaseToolDependency": BaseToolDependency,
        "BaseMetaData": BaseMetaData,
        "BaseNamespace": BaseNamespace,
        "BaseOptions": BaseOptions,
        "BaseSpec": BaseSpec,
    },
    "main": {
        "BaseFlockSchema": BaseFlockSchema,
    },
}
