# coding: utf-8

from __future__ import annotations

from flock_schemas.base import BaseSpec
from pydantic import BaseModel, Field


class ResourceDetails(BaseModel):
    """ResourceDetails."""

    id: str = Field(default=None)
    metadata: dict = Field(default=None)
    kind: str = Field(default=None)
    namespace: str = Field(default=None)
    category: str = Field(default=None)
    spec: BaseSpec = Field(default=None)


ResourceDetails.update_forward_refs()
