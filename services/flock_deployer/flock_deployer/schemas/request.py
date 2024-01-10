"""Response schemas for the API"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from flock_deployer.schemas.config import DeploymentConfigSchema


class DeploymentRequest(BaseModel):
    deployment_name: str
    deployment_namespace: str
    deployment_kind: str
    resource_name: str
    resource_namespace: str
    resource_kind: str
    schedule: str = "0 0 * * 0"
    config: DeploymentConfigSchema
    dry_run: bool = False


class ConfigRequest(BaseModel):
    config: DeploymentConfigSchema


class DeleteRequest(BaseModel):
    deployment_name: str
    deployment_namespace: str
    deployment_kind: str = ""
    dry_run: bool = False


class ConfigResponseObj(BaseModel):
    name: str
    description: str
    kind: str
    id: str
    target_kind: Optional[str]


class ConfigResponse(BaseModel):
    items: list[ConfigResponseObj]


DeploymentRequest.update_forward_refs()


DeploymentRequest.update_forward_refs()


export = {
    "sub": {},
    "main": {
        "DeploymentRequest": DeploymentRequest,
        "DeleteRequest": DeleteRequest,
        "ConfigRequest": ConfigRequest,
    },
}
