"""Response schemas for the API"""

from __future__ import annotations

from typing import Literal

from flock_schemas.deployment import DeploymentSchema
from pydantic import BaseModel, Field


class ResourceCreated(BaseModel):
    """Resource created successfully"""

    message: Literal["Created successfully"] = Field(
        default="Created successfully", description="Message of the response"
    )
    status: Literal["Success"] = Field(
        default="Success", description="Status of the response"
    )
    code: Literal[200] = Field(default=200, description="HTTP status codes")
    data: DeploymentSchema = Field(..., description="Data of the response")


ResourceCreated.update_forward_refs()
