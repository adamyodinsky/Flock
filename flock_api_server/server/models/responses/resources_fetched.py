# coding: utf-8

from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, Field  # noqa: F401

from server.models.resource_details import ResourceDetails
from server.models.status_code import Code, Status


class ResourcesFetched(BaseModel):
    message: Literal["Resources retrieved successfully"] = Field(
        ..., description="Message of the response"
    )
    status: Literal[Status.SUCCESS] = Field(..., description="Status of the response")
    code: Literal[Code.OK] = Field(..., description="HTTP status codes")
    data: List[ResourceDetails] = Field(..., description="Data of the response")


ResourcesFetched.update_forward_refs()
