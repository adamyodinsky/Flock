"""Deployment schema."""

from typing import Dict, Literal, Optional

from pydantic import Field

from flock_schemas.base import (
    BaseMetaData,
    BaseModelConfig,
    BaseToolDependency,
    Category,
)


class DeploymentTargetResource(BaseToolDependency):
    """Deployment target resource schema."""

    env: Optional[Dict[str, str]] = Field(
        default={},
        description="Environment variables to be set for the deployment",
    )


class DeploymentSpec(BaseModelConfig):
    """Deployment spec schema."""

    image: str = Field(
        ...,
        description="The container image to be deployed",
    )
    targetResource: DeploymentTargetResource = Field(
        ...,
        description="The target resource to be deployed",
    )
    replicas: int = Field(
        1,
        description="The number of replicas to be deployed",
    )


class DeploymentSchema(BaseModelConfig):
    """Deployment schema."""

    apiVersion: Literal["flock/v1"] = Field(..., description="API version")
    metadata: BaseMetaData = Field(..., description="The metadata of the object")
    kind: Literal["FlockDeployment"] = Field(..., description="The kind of the object")
    category: Optional[str] = Field(default=Category.DEPLOYMENT)
    namespace: str = Field(..., description="The namespace of the object")
    spec: DeploymentSpec = Field(..., description="The spec of the object")


export = {
    "sub": {
        "DeploymentTargetResource": DeploymentTargetResource,
        "DeploymentSpec": DeploymentSpec,
    },
    "main": {
        "DeploymentSchema": DeploymentSchema,
    },
}
