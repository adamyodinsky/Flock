# coding: utf-8

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from server.schemas.status_code import Code, Message, Status


class InternalServerError(BaseModel):
    message: Optional[str] = Field(
        default=Message.INTERNAL_SERVER_ERROR, description="Message of the response"
    )
    status: Literal[Status.ERROR] = Field(
        default=Status.ERROR, description="Status of the response"
    )
    code: Literal[Code.INTERNAL_SERVER_ERROR] = Field(
        default=Code.INTERNAL_SERVER_ERROR, description="HTTP status codes"
    )
    details: List[str] = Field(..., description="Details of the response")


InternalServerError.update_forward_refs()
