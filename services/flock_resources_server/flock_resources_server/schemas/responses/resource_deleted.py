# coding: utf-8

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from flock_resources_server.schemas.status_code import Code, Message, Status


class ResourceDeleted(BaseModel):
    """Resource Deleted Response"""

    message: Optional[str] = Field(
        default=Message.DELETED, description="Message of the response"
    )
    status: Literal[Status.SUCCESS] = Field(
        default=Status.SUCCESS, description="Status of the response"
    )
    code: Literal[Code.OK] = Field(default=Code.OK, description="HTTP status codes")
    details: List[str] = Field(..., description="Details of the response")


ResourceDeleted.update_forward_refs()
