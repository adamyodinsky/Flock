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


class DeploymentConfig(BaseModelConfig):
    apiVersion: str
    kind: Literal["DeploymentConfig"]  # = Field(..., description="Kind of the object")
    metadata: BaseMetaData  # = Field(..., description="Metadata for the object")
    env: list[EnvironmentVariable] = []
