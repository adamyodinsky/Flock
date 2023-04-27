# coding: utf-8

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from server.models.resource_data import ResourceData
from server.models.status_code import Code, Status


class ResourceAccepted(BaseModel):
    message: Literal["Resource deleted successfully"] = Field(
        ..., description="Message of the response"
    )
    status: Literal[Status.SUCCESS] = Field(..., description="Status of the response")
    code: Literal[Code.ACCEPTED] = Field(..., description="HTTP status codes")
    data: ResourceData = Field(..., description="Data of the response")


ResourceAccepted.update_forward_refs()
