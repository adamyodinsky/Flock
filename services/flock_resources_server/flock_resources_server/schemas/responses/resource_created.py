# coding: utf-8

from __future__ import annotations

from typing import Literal

from flock_schemas import BaseResourceSchema
from pydantic import BaseModel, Field
from flock_resources_server.schemas.status_code import Code, Message, Status


class ResourceCreated(BaseModel):
    """Resource created successfully"""

    message: Literal[Message.CREATED] = Field(
        default=Message.CREATED, description="Message of the response"
    )
    status: Literal[Status.SUCCESS] = Field(
        default=Status.SUCCESS, description="Status of the response"
    )
    code: Literal[Code.OK] = Field(default=Code.OK, description="HTTP status codes")
    data: BaseResourceSchema = Field(..., description="Data of the response")


ResourceCreated.update_forward_refs()
