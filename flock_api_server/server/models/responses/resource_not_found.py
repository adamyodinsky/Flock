# coding: utf-8

from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, Field

from server.models.status_code import Code, Status


class ResourceNotFound(BaseModel):
    message: Literal["Resource not found"] = Field(
        ..., description="Message of the response"
    )
    status: Literal[Status.ERROR] = Field(..., description="Status of the response")
    code: Literal[Code.NOT_FOUND] = Field(..., description="HTTP status codes")
    details: List[str] = Field(..., description="Details of the response")


ResourceNotFound.update_forward_refs()
