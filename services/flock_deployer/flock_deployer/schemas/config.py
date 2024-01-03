from typing import Literal, Union

from flock_schemas.base import Kind
from pydantic import Field

from flock_deployer.schemas.deployment import (
    BaseMetaData,
    BaseModelConfig,
    EnvFrom,
    EnvVar,
)


class DeploymentConfigSchema(BaseModelConfig):
    apiVersion: Literal["flock/v1"] = Field(
        ..., description="API version of the object"
    )
    kind: Literal["DeploymentConfigSchema"] = Field(
        ..., description="Kind of the object"
    )
    metadata: BaseMetaData = Field(..., description="Metadata for the object")
    env: list[Union[EnvVar, EnvFrom]] = []
    image: str = Field("", description="Image to be deployed")


class DeploymentGlobalConfigSchema(BaseModelConfig):
    kind: Literal["DeploymentGlobalConfigSchema"] = Field(
        ..., description="Kind of the object"
    )
    kind_target: Kind = Field(
        ..., description="this configuration will apply to all objects of this kind"
    )


class DeploymentKindConfigSchema(BaseModelConfig):
    kind: Literal["DeploymentGlobalConfigSchema"] = Field(
        ..., description="Kind of the object"
    )


export = {
    "sub": {},
    "main": {
        "DeploymentConfig": DeploymentConfigSchema,
        "DeploymentGlobalConfig": DeploymentGlobalConfigSchema,
        "DeploymentKindConfig": DeploymentKindConfigSchema,
    },
}
