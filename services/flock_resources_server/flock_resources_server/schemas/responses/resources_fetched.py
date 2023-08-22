# coding: utf-8

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field  # noqa: F401

from flock_resources_server.schemas.resource_details import ResourceDetails
from flock_resources_server.schemas.responses.resource_fetched import ListData
from flock_resources_server.schemas.status_code import Code, Message, Status


class ResourcesFetched(BaseModel):
    """Resources retrieved successfully"""

    message: Literal[Message.FETCHED] = Field(
        default=Message.FETCHED, description="Message of the response"
    )
    status: Literal[Status.SUCCESS] = Field(
        default=Status.SUCCESS, description="Status of the response"
    )
    code: Literal[Code.OK] = Field(default=Code.OK, description="HTTP status codes")
    data: ListData = Field(..., description="Data of the response")


ResourcesFetched.update_forward_refs()
