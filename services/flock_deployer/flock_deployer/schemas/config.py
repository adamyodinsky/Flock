from typing import Literal, Union

from pydantic import Field

from flock_deployer.schemas.deployment import (
    BaseMetaData,
    BaseModelConfig,
    EnvFrom,
    EnvVar,
)


class Metadata(BaseModelConfig):
    name: str
    description: str


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


export = {
    "sub": {},
    "main": {
        "DeploymentConfig": DeploymentConfigSchema,
    },
}
