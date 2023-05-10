"""Deployment schema."""

from typing import Any, Dict, List, Literal, Optional

from pydantic import Field, IPvAnyAddress

from flock_schemas.base import (
    BaseMetaData,
    BaseModelConfig,
    BaseToolDependency,
    Category,
)


class ContainerPort(BaseModelConfig):
    """Container port schema."""

    name: str = Field(
        default=None,
        description="The name of the port",
        max_length=15,
    )
    protocol: Literal["tcp", "udp", "TCP", "UDP"] = Field(
        "tcp",
        description="The protocol for the port",
    )
    port: int = Field(
        default=None,
        description="The port number",
    )


class EnvironmentVariable(BaseModelConfig):
    """Environment variable schema."""

    name: str = Field(
        ...,
        description="The name of the environment variable",
    )
    value: Optional[str] = Field(
        description="The value of the environment variable",
    )

    valueFrom: Optional[Dict[str, Any]] = Field(
        description="The value of the environment variable",
    )


class DeploymentContainer(BaseModelConfig):
    """Deployment spec schema."""

    image: str = Field(
        ...,
        description="The container image to be deployed",
    )
    env: List[EnvironmentVariable] = Field(
        default=[],
        description="Environment variables to be set for the deployment",
    )
    ports: List[ContainerPort] = Field(
        default=[],
        description="The ports to be exposed by the container",
    )
    image_pull_policy: Literal["Always", "Never", "IfNotPresent"] = Field(
        "IfNotPresent",
        description="The image pull policy",
    )


class DeploymentTargetResource(BaseToolDependency):
    """Deployment target resource schema."""

    options: Optional[Dict[str, Any]] = Field(
        default={},
        description="Deployment target options",
    )


class DeploymentSpec(BaseModelConfig):
    """Deployment spec schema."""

    targetResource: DeploymentTargetResource = Field(
        ...,
        description="The target resource to be deployed",
    )
    replicas: int = Field(
        1,
        description="The number of replicas to be deployed",
    )
    container: DeploymentContainer = Field(
        ...,
        description="The container specs",
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
