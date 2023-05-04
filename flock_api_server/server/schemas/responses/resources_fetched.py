# coding: utf-8

from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, Field  # noqa: F401

from server.schemas.resource_details import ResourceDetails
from server.schemas.status_code import Code, Message, Status


class ResourcesFetched(BaseModel):
    """Resources retrieved successfully"""

    message: Literal[Message.FETCHED] = Field(
        default=Message.FETCHED, description="Message of the response"
    )
    status: Literal[Status.SUCCESS] = Field(
        default=Status.SUCCESS, description="Status of the response"
    )
    code: Literal[Code.OK] = Field(default=Code.OK, description="HTTP status codes")
    data: List[ResourceDetails] = Field(..., description="Data of the response")


ResourcesFetched.update_forward_refs()
