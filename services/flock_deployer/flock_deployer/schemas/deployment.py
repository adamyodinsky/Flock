"""Deployment schema."""


from typing import List, Literal, Optional, Union

from flock_schemas.base import (
    BaseMetaData,
    BaseModelConfig,
    BaseToolDependency,
    Category,
)
from pydantic import Field


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


class EnvVar(BaseModelConfig):
    """Environment variable schema."""

    name: str
    value: str


class SecretKeyRefValue(BaseModelConfig):
    """Environment variable schema."""

    name: str
    key: str


class SecretKeyRef(BaseModelConfig):
    secretKeyRef: SecretKeyRefValue


class EnvFrom(BaseModelConfig):
    name: str
    valueFrom: SecretKeyRef


class VolumeMount(BaseModelConfig):
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


class PersistentVolumeClaim(BaseModelConfig):
    """PersistentVolumeClaim schema."""

    claimName: str = Field(..., description="Name of the PersistentVolumeClaim to use.")


class Secret(BaseModelConfig):
    """Secret schema."""

    secretName: str


class VolumeEmptyDir(BaseModelConfig):
    """EmptyDir volume schema."""

    medium: Literal["", "Memory", "HugePages"] = Field(
        "", description="What type of storage medium should back this directory."
    )
    sizeLimit: str = Field(
        None,
        description="Total amount of local storage required for this EmptyDir volume.",
    )


class VolumeHostPath(BaseModelConfig):
    """HostPath volume schema."""

    path: str = Field(..., description="Path of the directory on the host.")
    type: str = Field(None, description="Type for HostPath volume.")


class VolumeSource(BaseModelConfig):
    """Volume source schema."""

    class Config:
        extra = "allow"

    __root__: Union[VolumeEmptyDir, VolumeHostPath, PersistentVolumeClaim]


class Volume(BaseModelConfig):
    """Volume schema."""

    name: str = Field(
        ..., description="Volume name. Must be a DNS_LABEL and unique within the pod."
    )
    # volume_source: VolumeSource = Field(..., description="Volume source specification.")
    persistentVolumeClaim: PersistentVolumeClaim = Field(
        ..., description="PersistentVolumeClaim volume source."
    )
    secret: Optional[Secret] = None
    readOnly: bool = Field(False, description="Whether the volume is read only.")


class ContainerSpec(BaseModelConfig):
    """Deployment spec schema."""

    image: str = Field(
        ...,
        description="The container image to be deployed",
    )
    env: List[Union[EnvVar, EnvFrom]] = Field(
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
    volume_mounts: List[VolumeMount] = Field(
        default=[],
        description="The volume mounts to be mounted in the container",
    )


class TargetResource(BaseToolDependency):
    """Deployment target resource schema."""

    kind: str = Field(..., description="Kind of the target resource")


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
    restart_policy: Literal["Always"] = Field(
        "Always",
        description="The restart policy of the container",
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
        "ContainerPort": ContainerPort,
        "EnvVar": EnvVar,
        "EnvFrom": EnvFrom,
        "VolumeMount": VolumeMount,
        "PersistentVolumeClaim": PersistentVolumeClaim,
        "Secret": Secret,
        "VolumeEmptyDir": VolumeEmptyDir,
        "VolumeHostPath": VolumeHostPath,
        "VolumeSource": VolumeSource,
        "Volume": Volume,
        "ContainerSpec": ContainerSpec,
        "TargetResource": TargetResource,
        "DeploymentSpec": DeploymentSpec,
    },
    "main": {
        "Deployment": DeploymentSchema,
    },
}
