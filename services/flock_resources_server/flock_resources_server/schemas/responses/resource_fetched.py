# coding: utf-8

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from flock_resources_server.schemas.status_code import Code, Message, Status


class ListData(BaseModel):
    items: list
    count: int
    total: int


class ResourceFetched(BaseModel):
    """Response model for resource fetched"""

    message: Literal[Message.FETCHED] = Field(
        default=Message.FETCHED, description="Message of the response"
    )
    status: Literal[Status.SUCCESS] = Field(
        default=Status.SUCCESS, description="Status of the response"
    )
    code: Literal[Code.OK] = Field(default=Code.OK, description="HTTP status codes")
    data: dict = Field(..., description="Data of the response")


class KindsFetched(ResourceFetched):
    """Response model for kinds fetched"""

    message: Literal[Message.FETCHED] = Field(
        default=Message.FETCHED, description="Message of the response"
    )
    status: Literal[Status.SUCCESS] = Field(
        default=Status.SUCCESS, description="Status of the response"
    )
    code: Literal[Code.OK] = Field(default=Code.OK, description="HTTP status codes")
    data: ListData = Field(..., description="Data of the response")


class SchemasFetched(ResourceFetched):
    """Response model for schema fetched"""

    message: Literal[Message.FETCHED] = Field(
        default=Message.FETCHED, description="Message of the response"
    )
    status: Literal[Status.SUCCESS] = Field(
        default=Status.SUCCESS, description="Status of the response"
    )
    code: Literal[Code.OK] = Field(default=Code.OK, description="HTTP status codes")
    data: ListData = Field(..., description="Data of the response")


ResourceFetched.update_forward_refs()
