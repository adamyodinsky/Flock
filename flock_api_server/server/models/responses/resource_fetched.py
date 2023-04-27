# coding: utf-8

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from server.models.status_code import Code, Message, Status, ResourceType


class ResourceFetched(BaseModel):
    message: Literal[Message.FETCHED] = Field(
        default=Message.FETCHED, description="Message of the response"
    )
    status: Literal[Status.SUCCESS] = Field(
        default=Status.SUCCESS, description="Status of the response"
    )
    code: Literal[Code.OK] = Field(default=Code.OK, description="HTTP status codes")
    data: ResourceType = Field(..., description="Data of the response")


ResourceFetched.update_forward_refs()
