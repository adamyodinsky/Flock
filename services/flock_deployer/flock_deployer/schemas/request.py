"""Response schemas for the API"""

from __future__ import annotations

from pydantic import BaseModel
from flock_deployer.schemas.config import DeploymentConfigSchema


class DeploymentRequest(BaseModel):
    """Resource created successfully"""

    deployment_name: str
    deployment_namespace: str
    deployment_kind: str
    resource_name: str
    resource_namespace: str
    resource_kind: str
    config: DeploymentConfigSchema


class ConfigRequest(BaseModel):
    """Resource created successfully"""

    config: DeploymentConfigSchema


class DeleteRequest(BaseModel):
    """Resource created successfully"""

    deployment_name: str
    deployment_namespace: str
    resource_kind: str


DeploymentRequest.update_forward_refs()


DeploymentRequest.update_forward_refs()


export = {
    "sub": {},
    "main": {
        "DeploymentRequest": DeploymentRequest,
        "DeleteRequest": DeleteRequest,
    },
}
