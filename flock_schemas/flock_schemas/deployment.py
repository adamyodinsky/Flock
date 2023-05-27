"""Deployment schema."""

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator

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


class VolumeMounts(BaseModelConfig):
    """Volume mount schema."""

    name: str = Field(
        ...,
        description="The name of the volume mount",
    )
    mountPath: str = Field(
        ...,
        description="The path where the volume should be mounted",
    )
    readOnly: bool = Field(
        False,
        description="Whether the volume should be mounted as read-only",
    )


class PersistentVolumeClaim(BaseModel):
    """PersistentVolumeClaim schema."""

    claimName: str


class Secret(BaseModel):
    """Secret schema."""

    secretName: str


class VolumeEmptyDir(BaseModel):
    """EmptyDir volume schema."""

    medium: Literal["", "Memory", "HugePages"] = Field(
        "", description="What type of storage medium should back this directory."
    )
    sizeLimit: str = Field(
        None,
        description="Total amount of local storage required for this EmptyDir volume.",
    )


class VolumeHostPath(BaseModel):
    """HostPath volume schema."""

    path: str = Field(..., description="Path of the directory on the host.")
    type: str = Field(None, description="Type for HostPath volume.")

    # @validator("path")
    # def validate_path(self, path):
    #     """Validate path."""
    #     if not path:
    #         raise ValueError("path cannot be an empty string")
    #     # Here you can add further validation for path format if required.
    #     return path


class VolumePersistentVolumeClaim(BaseModel):
    """PersistentVolumeClaim schema."""

    claimName: str = Field(..., description="Name of the PersistentVolumeClaim to use.")
    readOnly: bool = Field(False, description="Whether the volume is read only.")

    # @validator("claimName")
    # def validate_claim_name(self, claim_name):
    #     """Validate claim_name."""

    #     if not claim_name:
    #         raise ValueError("claimName cannot be an empty string")
    #     # Here you can add further validation for claimName format if required.
    #     return claim_name


class VolumeSource(BaseModel):
    """Volume source schema."""

    class Config:
        extra = "allow"

    __root__: Union[VolumeEmptyDir, VolumeHostPath, VolumePersistentVolumeClaim]


class Volume(BaseModel):
    """Volume schema."""

    name: str = Field(
        ..., description="Volume name. Must be a DNS_LABEL and unique within the pod."
    )
    volume_source: VolumeSource
    persistentVolumeClaim: Optional[PersistentVolumeClaim]
    secret: Optional[Secret]

    # @root_validator
    # def validate_name(self, values):
    #     """Validate name."""

    #     name = values.get("name")
    #     if not name.islower():
    #         raise ValueError("name must be all lower case")
    #     if len(name) > 253:
    #         raise ValueError("name must be 253 characters or less")
    #     return values


class ContainerSpec(BaseModelConfig):
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
    args: List[str] = Field(
        default=[],
        description="The arguments to be passed to the container",
    )
    command: List[str] = Field(
        default=[],
        description="The command to be executed in the container",
    )
    volume_mounts: List[VolumeMounts] = Field(
        default=[],
        description="The volume mounts to be mounted in the container",
    )


class TargetResource(BaseToolDependency):
    """Deployment target resource schema."""


class DeploymentSpec(BaseModelConfig):
    """Deployment spec schema."""

    targetResource: TargetResource = Field(
        default={},
        description="The target resource to be deployed",
    )
    replicas: int = Field(
        1,
        description="The number of replicas to be deployed",
    )
    container: ContainerSpec = Field(
        ...,
        description="The container specs",
    )
    volumes: List[Volume] = Field(
        default=[],
        description="The volumes to be mounted in the container",
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
        "DeploymentTargetResource": TargetResource,
        "DeploymentSpec": DeploymentSpec,
        "ContainerSpec": ContainerSpec,
        "ContainerPort": ContainerPort,
        "EnvironmentVariable": EnvironmentVariable,
    },
    "main": {
        "DeploymentSchema": DeploymentSchema,
    },
}
