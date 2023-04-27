# coding: utf-8

from __future__ import annotations

from pydantic import BaseModel, Field  # noqa: F401


class ResourceDetails(BaseModel):
    name: str = Field(alias="name", default=None)
    namespace: str = Field(alias="namespace", default=None)
    kind: str = Field(alias="kind", default=None)


ResourceDetails.update_forward_refs()
