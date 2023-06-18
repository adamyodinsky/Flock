from typing import Literal, Optional

from flock_deployer.schemas.deployment import (
    BaseMetaData,
    BaseModelConfig,
    EnvironmentVariable,
)
from pydantic import Field


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
    env: list[EnvironmentVariable] = []
    image: str = Field("", description="Image to be deployed")


export = {
    "sub": {},
    "main": {
        "DeploymentConfig": DeploymentConfigSchema,
    },
}
