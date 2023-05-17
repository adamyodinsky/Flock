"""LLM Tool schema."""


from typing import Dict, Literal, Optional

from pydantic import Field

from flock_schemas.base import BaseFlockSchema, BaseSpec, Category
from flock_schemas.dependencies import (
    EmbeddingDependency,
    SplitterDependency,
    VectorStoreDependency,
)


class EmbeddingsLoaderSpec(BaseSpec):
    """EmbeddingsLoader spec."""

    vendor: Optional[str] = Field(
        default="v1", description="The class of the tool, e.g, etc."
    )
    dependencies: tuple[
        SplitterDependency, EmbeddingDependency, VectorStoreDependency
    ] = Field(..., description="Tool dependencies")


class EmbeddingsLoaderSchema(BaseFlockSchema):
    """EmbeddingsLoader schema."""

    kind: Literal["EmbeddingsLoader"] = Field(..., description="The kind of the object")
    category: Category = Field(
        default=Category.TOOL, description="The resource category"
    )
    spec: EmbeddingsLoaderSpec


export = {
    "sub": {
        "EmbeddingsLoaderSpec": EmbeddingsLoaderSpec,
    },
    "main": {
        "EmbeddingsLoaderSchema": EmbeddingsLoaderSchema,
    },
}
