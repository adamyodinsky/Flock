# coding: utf-8

from __future__ import annotations

from pydantic import BaseModel, Field


class ResourceDetails(BaseModel):
    """ResourceDetails."""

    name: str = Field(alias="name", default=None)
    namespace: str = Field(default=None)
    kind: str = Field(alias="kind", default=None)


ResourceDetails.update_forward_refs()
