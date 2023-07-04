# coding: utf-8

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from flock_resources_server.schemas.status_code import Code, Message, ResourceType, Status


class ResourceUpdated(BaseModel):
    """Resource Updated Response"""

    message: Literal[Message.UPDATED] = Field(
        default=Message.UPDATED, description="Message of the response"
    )
    status: Literal[Status.SUCCESS] = Field(
        default=Status.SUCCESS, description="Status of the response"
    )
    code: Literal[Code.OK] = Field(default=Code.OK, description="HTTP status codes")
    data: ResourceType = Field(..., description="Data of the response")


ResourceUpdated.update_forward_refs()
