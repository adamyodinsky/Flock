# coding: utf-8

from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, Field

from server.models.status_code import Code, Status


class ResourceAlreadyExists(BaseModel):
    message: Literal["A resource with the same unique property already exists"] = Field(
        ..., description="Message of the response"
    )
    status: Literal[Status.ERROR] = Field(..., description="Status of the response")
    code: Literal[Code.CONFLICT] = Field(..., description="HTTP status codes")
    details: List[str] = Field(..., description="Details of the response")


ResourceAlreadyExists.update_forward_refs()
