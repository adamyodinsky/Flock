# coding: utf-8

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from flock_resources_server.schemas.status_code import Code, Message, ResourceType, Status


class ResourceAccepted(BaseModel):
    """Resource deleted successfully"""

    message: Literal[Message.ACCEPTED] = Field(
        default=Message.ACCEPTED, description="Message of the response"
    )
    status: Literal[Status.SUCCESS] = Field(
        default=Status.SUCCESS, description="Status of the response"
    )
    code: Literal[Code.ACCEPTED] = Field(
        default=Code.ACCEPTED, description="HTTP status codes"
    )
    data: ResourceType = Field(..., description="Data of the response")


ResourceAccepted.update_forward_refs()
