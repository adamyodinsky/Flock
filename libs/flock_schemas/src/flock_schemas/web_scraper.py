"""web-scraper object schemas for Flock."""


from typing import Literal

from flock_schemas.base import BaseOptions, BaseResourceSchema, Category
from flock_schemas.dependencies import VectorStoreDependency
from pydantic import Field


class VectorStoreSpec(BaseOptions):
    """Vectorstore spec."""

    vendor: str = Field(
        ..., description="The vendor of the vector store, e.g. Chroma, Pinecone, etc."
    )
    dependencies: tuple[VectorStoreDependency] = Field(
        ..., description="Vectorstore dependencies"
    )


class WebScraperSchema(BaseResourceSchema):
    """Custom object schema."""

    kind: Literal["WebScraper"] = Field(..., description="The object kind")
    category: Category = Field(
        default=Category.JOB, description="The resource category"
    )
    spec: VectorStoreSpec


export = {
    "sub": {
        "VectorStoreSpec": VectorStoreSpec,
    },
    "main": {
        "WebScraper": WebScraperSchema,
    },
}
