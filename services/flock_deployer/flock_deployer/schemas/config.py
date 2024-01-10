from typing import Literal, Union
from uuid import uuid4

from flock_schemas.base import Kind
from pydantic import Field

from flock_deployer.schemas.deployment import (
    BaseMetaData,
    BaseModelConfig,
    EnvFrom,
    EnvVar,
)


def str_uuid():
    return str(uuid4())


class BaseDeploymentConfigSchema(BaseModelConfig):
    id: str = Field(default_factory=str_uuid, description="String UUID of the object")
    apiVersion: Literal["flock/v1"] = Field(
        ..., description="API version of the object"
    )
    metadata: BaseMetaData = Field(..., description="Metadata for the object")
    env: list[Union[EnvVar, EnvFrom]] = []
    image: str = Field("", description="Image to be deployed")


class DeploymentConfigSchema(BaseDeploymentConfigSchema):
    kind: Literal["DeploymentConfig"] = Field(..., description="Kind of the object")


class DeploymentGlobalConfigSchema(BaseDeploymentConfigSchema):
    kind: Literal["DeploymentGlobalConfig"] = Field(
        ..., description="Kind of the object"
    )


class DeploymentKindConfigSchema(BaseDeploymentConfigSchema):
    kind: Literal["DeploymentKindConfig"] = Field(
        ..., description="This configuration will apply to all objects of this kind"
    )
    kind_target: Kind = Field(
        ..., description="This configuration will apply to all objects globally"
    )


export = {
    "sub": {},
    "main": {
        "BaseDeploymentConfigSchema": BaseDeploymentConfigSchema,
        "DeploymentConfig": DeploymentConfigSchema,
        "DeploymentGlobalConfig": DeploymentGlobalConfigSchema,
        "DeploymentKindConfig": DeploymentKindConfigSchema,
    },
}
