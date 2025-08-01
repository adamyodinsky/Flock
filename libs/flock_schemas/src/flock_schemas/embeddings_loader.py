"""LLM Tool schema."""


from pathlib import Path
from typing import Literal, Optional

from flock_schemas.base import BaseModelConfig, BaseResourceSchema, BaseSpec, Category
from flock_schemas.dependencies import SplitterDependency, VectorStoreDependency
from pydantic import Field


def home_dir():
    """Get the home directory."""

    h_dir = Path.home()
    return str(h_dir)


class EmbeddingsLoaderOptions(BaseModelConfig):
    """Options schema."""

    source_directory: str = Field(
        default=f"{home_dir()}/.flock/data/raw",
        description="The directory containing the data files",
    )
    base_meta_source: str = Field(
        default="", description="The base meta source file name"
    )
    archive_path: str = Field(
        default=f"{home_dir()}/.flock/data/archive",
        description="The path to the archive file containing the data files",
    )
    allowed_extensions: str = Field(
        default="", description="The allowed extensions for the data files"
    )
    deny_extensions: str = Field(
        default="", description="The denied extensions for the data files"
    )


class EmbeddingsLoaderSpec(BaseSpec):
    """EmbeddingsLoader spec."""

    vendor: Optional[str] = Field(default="v1", description="")
    dependencies: tuple[SplitterDependency, VectorStoreDependency] = Field(
        ..., description="dependencies"
    )

    options: EmbeddingsLoaderOptions = Field(
        default_factory=EmbeddingsLoaderOptions,
        description="Options for the embeddings loader",
    )


class EmbeddingsLoaderSchema(BaseResourceSchema):
    """EmbeddingsLoader schema."""

    kind: Literal["EmbeddingsLoader"] = Field(..., description="The kind of the object")
    category: Category = Field(
        default=Category.OTHER, description="The resource category"
    )
    spec: EmbeddingsLoaderSpec


export = {
    "sub": {
        "EmbeddingsLoaderSpec": EmbeddingsLoaderSpec,
        "EmbeddingsLoaderOptions": EmbeddingsLoaderOptions,
    },
    "main": {
        "EmbeddingsLoader": EmbeddingsLoaderSchema,
    },
}
