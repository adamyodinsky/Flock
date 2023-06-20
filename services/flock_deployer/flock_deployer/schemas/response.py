"""Response schemas for the API"""

from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, Field

from flock_deployer.schemas import (
    CronJobSchema,
    DeploymentConfigSchema,
    DeploymentSchema,
    JobSchema,
)


class HealthResponse(BaseModel):
    """Health response"""

    status: Literal["OK", "ERROR"]
    stores: dict[str, Literal["OK", "ERROR"]]


class ResourceCreated(BaseModel):
    """Resource created successfully"""

    message: Literal["Created successfully"] = Field(
        default="Created successfully", description="Message of the response"
    )
    status: Literal["Success"] = Field(
        default="Success", description="Status of the response"
    )
    code: Literal[200] = Field(default=200, description="HTTP status codes")
    data: Union[DeploymentSchema, CronJobSchema, JobSchema] = Field(
        ..., description="Data of the response"
    )


class ResourceDeleted(BaseModel):
    """Resource deleted successfully"""

    message: Literal["Deleted successfully"] = Field(
        default="Deleted successfully", description="Message of the response"
    )
    status: Literal["Success"] = Field(
        default="Success", description="Status of the response"
    )
    code: Literal[200] = Field(default=200, description="HTTP status codes")


class ConfigCreated(BaseModel):
    """Resource created successfully"""

    message: Literal["Created successfully"] = Field(
        default="Created successfully", description="Message of the response"
    )
    status: Literal["Success"] = Field(
        default="Success", description="Status of the response"
    )
    code: Literal[200] = Field(default=200, description="HTTP status codes")
    data: DeploymentConfigSchema = Field(..., description="Data of the response")


ResourceCreated.update_forward_refs()
ResourceDeleted.update_forward_refs()

export = {
    "sub": {},
    "main": {
        "ResourceCreated": ResourceCreated,
        "ResourceDeleted": ResourceDeleted,
    },
}
