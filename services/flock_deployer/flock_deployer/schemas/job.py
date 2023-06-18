"""Deployment schema."""

from typing import List, Literal, Optional

from flock_schemas.base import BaseMetaData, BaseModelConfig
from pydantic import Field

from flock_deployer.schemas.deployment import (
    ContainerSpec,
    DeploymentSchema,
    TargetResource,
    Volume,
)


class JobSpec(BaseModelConfig):
    """Job spec schema."""

    targetResource: TargetResource = Field(
        {},
        description="The target resource to be deployed",
    )
    container: ContainerSpec = Field(
        ...,
        description="The container specs",
    )
    backoff_limit: Optional[int] = Field(
        default=6,
        description="The number of times the job will be retried before it is marked as failed",
    )
    completions: Optional[int] = Field(
        default=1,
        description="The desired number of successfully finished pods the job should be run with",
    )
    parallelism: Optional[int] = Field(
        default=1,
        description="The maximum desired number of pods the job should run at any given time",
    )
    volumes: List[Volume] = Field(
        default=[],
        description="The volumes to be mounted in the container",
    )
    restart_policy: Literal["Never", "OnFailure"] = Field(
        "Never",
        description="The restart policy of the container",
    )


class CronJobSpec(JobSpec):
    """CronJob spec schema."""

    schedule: str = Field(
        ...,
        description="The cron schedule",
    )


class JobSchema(DeploymentSchema):
    """Job schema."""

    apiVersion: Literal["flock/v1"] = Field(..., description="API version")
    metadata: BaseMetaData = Field(..., description="The metadata of the object")
    kind: Literal["FlockJob"] = Field(..., description="The kind of the object")
    namespace: str = Field(..., description="The namespace of the object")
    spec: JobSpec = Field(..., description="The spec of the object")


class CronJobSchema(JobSchema):
    """CronJob schema."""

    kind: Literal["FlockCronJob"] = Field(..., description="The kind of the object")
    spec: CronJobSpec = Field(..., description="The spec of the object")


export = {
    "sub": {},
    "main": {
        "Job": JobSchema,
    },
}
