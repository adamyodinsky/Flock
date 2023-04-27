# coding: utf-8

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from server.models.status_code import Code, Message, Status, ResourceType


class ResourceCreated(BaseModel):
    """Resource created successfully"""

    message: Literal[Message.CREATED] = Field(
        default=Message.CREATED, description="Message of the response"
    )
    status: Literal[Status.SUCCESS] = Field(
        default=Status.SUCCESS, description="Status of the response"
    )
    code: Literal[Code.OK] = Field(default=Code.OK, description="HTTP status codes")
    data: ResourceType = Field(..., description="Data of the response")


ResourceCreated.update_forward_refs()
