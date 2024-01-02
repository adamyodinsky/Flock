"""web-scraper object schemas for Flock."""


from enum import Enum
from typing import Literal

from flock_schemas.base import BaseResourceSchema, BaseSpec, Category
from flock_schemas.dependencies import VectorStoreDependency
from pydantic import Field


class WebScraperSpec(BaseSpec):
    """WebScraper spec."""

    dependencies: tuple[VectorStoreDependency] = Field(..., description="dependencies")


class WebScraperSchema(BaseResourceSchema):
    """Custom object schema."""

    kind: Literal["WebScraper"] = Field(..., description="The object kind")
    category: Category = Field(
        default=Category.JOB, description="The resource category"
    )
    spec: WebScraperSpec


export = {
    "sub": {},
    "main": {
        "WebScraper": WebScraperSchema,
    },
}
