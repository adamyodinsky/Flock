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
    kind: Literal["DeploymentConfig"] = Field(..., description="Kind of the object")
    metadata: BaseMetaData = Field(..., description="Metadata for the object")
    env: list[Union[EnvVar, EnvFrom]] = []
    image: str = Field("", description="Image to be deployed")


class DeploymentGlobalConfigSchema(DeploymentConfigSchema):
    kind: Literal["DeploymentGlobalConfig"] = Field(
        ..., description="Kind of the object"
    )


class DeploymentKindConfigSchema(DeploymentConfigSchema):
    kind: Literal["DeploymentKindConfig"] = Field(
        ..., description="This configuration will apply to all objects of this kind"
    )
    kind_target: Kind = Field(
        ..., description="This configuration will apply to all objects globally"
    )


export = {
    "sub": {},
    "main": {
        "DeploymentConfig": DeploymentConfigSchema,
        "DeploymentGlobalConfig": DeploymentGlobalConfigSchema,
        "DeploymentKindConfig": DeploymentKindConfigSchema,
    },
}
