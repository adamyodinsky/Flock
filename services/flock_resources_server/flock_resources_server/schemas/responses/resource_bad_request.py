# coding: utf-8

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from flock_resources_server.schemas.status_code import Code, Message, Status


class ResourceBadRequest(BaseModel):
    """Resource bad request"""

    message: Optional[str] = Field(
        default=Message.BAD_REQUEST, description="Message of the response"
    )
    status: Literal[Status.ERROR] = Field(
        default=Status.ERROR, description="Status of the response"
    )
    code: Literal[Code.BAD_REQUEST] = Field(
        default=Code.BAD_REQUEST, description="HTTP status codes"
    )
    details: List[str] = Field(..., description="Details of the response")


ResourceBadRequest.update_forward_refs()
