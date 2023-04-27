# coding: utf-8

from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, Field

from server.models.status_code import Code, Status


class InternalServerError(BaseModel):
    message: Literal["Internal Server Error"] = Field(
        ..., description="Message of the response"
    )
    status: Literal[Status.ERROR] = Field(..., description="Status of the response")
    code: Literal[Code.INTERNAL_SERVER_ERROR] = Field(
        ..., description="HTTP status codes"
    )
    details: List[str] = Field(..., description="Details of the response")


InternalServerError.update_forward_refs()
